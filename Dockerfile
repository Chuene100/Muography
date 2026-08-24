# syntax=docker/dockerfile:1
#
# Muography pipeline: Geant4 muon transport through rock + ML flux prediction.
#
#   Stage 1 (geant4)  : build Geant4 11.3.0 from source, headless, with datasets
#   Stage 2 (sim)     : build the paulsim application against that Geant4
#   Stage 3 (runtime) : slim Ubuntu + Python ML stack + paulsim binary
#
# Build:  docker build -t muography .
# Run:    docker run --rm -v "$PWD/results:/opt/muography/results" muography

###############################################################################
# Stage 1 — Geant4 (headless build, ~20-40 min the first time)
###############################################################################
FROM ubuntu:24.04 AS geant4

ARG GEANT4_VERSION=11.3.0
ARG NPROC=2
ENV DATA_PREFIX=/opt/geant4/share/Geant4-${GEANT4_VERSION}/data

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        ca-certificates \
        wget \
        libexpat1-dev \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q "https://github.com/Geant4/geant4/archive/refs/tags/v${GEANT4_VERSION}.tar.gz" \
        -O /tmp/geant4.tar.gz \
    && mkdir /tmp/geant4-src \
    && tar -xzf /tmp/geant4.tar.gz -C /tmp/geant4-src --strip-components=1 \
    && rm /tmp/geant4.tar.gz

RUN cmake -S /tmp/geant4-src -B /tmp/geant4-build \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_INSTALL_PREFIX=/opt/geant4 \
        -DGEANT4_INSTALL_DATA=OFF \
        -DGEANT4_BUILD_MULTITHREADED=ON \
        -DGEANT4_USE_OPENGL_X11=OFF \
        -DGEANT4_USE_QT=OFF \
        -DGEANT4_USE_XM=OFF \
        -DGEANT4_USE_RAYTRACER_X11=OFF \
    && cmake --build /tmp/geant4-build -j "${NPROC}" \
    && cmake --install /tmp/geant4-build \
    && rm -rf /tmp/geant4-src /tmp/geant4-build

# Physics datasets: fetched with resumable downloads (wget -c + retries) since
# the CERN mirror tends to drop very long transfers. Tarballs are
# <FILENAME>.<VERSION>.tar.gz and extract to <NAME><VERSION>/ directories,
# matching the catalog in cmake/Modules/G4DatasetDefinitions.cmake of the tag.
RUN set -eux; \
    mkdir -p "${DATA_PREFIX}"; cd "${DATA_PREFIX}"; \
    for spec in \
        "G4EMLOW|8.6.1|G4EMLOW" \
        "PhotonEvaporation|6.1|G4PhotonEvaporation" \
        "RadioactiveDecay|6.1.2|G4RadioactiveDecay" \
        "G4ENSDFSTATE|3.0|G4ENSDFSTATE" \
        "G4NDL|4.7.1|G4NDL" \
        "G4PARTICLEXS|4.1|G4PARTICLEXS" \
        "G4PII|1.3|G4PII" \
        "G4ABLA|3.3|G4ABLA" \
        "G4INCL|1.2|G4INCL" \
        "RealSurface|2.2|G4RealSurface" \
        "G4CHANNELING|1.0|G4CHANNELING" \
        "G4NUDEXLIB|1.0|G4NUDEXLIB"; do \
        name="${spec%%|*}"; rest="${spec#*|}"; ver="${rest%%|*}"; file="${rest#*|}"; \
        tgz="${file}.${ver}.tar.gz"; \
        tries=0; \
        until wget -c -nv --timeout=60 --tries=3 \
              "https://cern.ch/geant4-data/datasets/${tgz}" -O "${tgz}"; do \
            tries=$((tries + 1)); [ "${tries}" -ge 15 ] && { echo "download failed: ${tgz}" >&2; exit 1; }; \
            sleep 3; \
        done; \
        tar -xzf "${tgz}"; rm -f "${tgz}"; \
    done; \
    ls "${DATA_PREFIX}"

# geant4.sh resolves GEANT4_DATA_DIR as <prefix>/share/Geant4/data, so place
# the datasets there regardless of the versioned download prefix.
RUN mkdir -p /opt/geant4/share/Geant4 \
    && if [ -d "${DATA_PREFIX}" ] && [ ! -d /opt/geant4/share/Geant4/data ]; then \
           mv "${DATA_PREFIX}" /opt/geant4/share/Geant4/data; \
       fi

###############################################################################
# Stage 2 — paulsim (Geant4 application)
###############################################################################
FROM ubuntu:24.04 AS sim-builder

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libexpat1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=geant4 /opt/geant4 /opt/geant4
ENV Geant4_DIR=/opt/geant4/lib/cmake/Geant4

WORKDIR /src/muon-sim
COPY muon-sim/ ./

RUN cmake -B build -DCMAKE_BUILD_TYPE=Release -DGeant4_DIR="${Geant4_DIR}" \
    && cmake --build build -j "$(nproc)"

###############################################################################
# Stage 3 — runtime: Python ML stack + simulation binary
###############################################################################
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        libexpat1 \
        zlib1g \
        libgomp1 \
        bash \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN python3 -m venv /opt/venv \
    && /opt/venv/bin/pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt
ENV PATH="/opt/venv/bin:${PATH}"

COPY --from=geant4 /opt/geant4 /opt/geant4
COPY --from=sim-builder /src/muon-sim/build/paulsim /opt/muography/muon-sim/build/paulsim

WORKDIR /opt/muography
COPY . /opt/muography
RUN chmod +x muon-sim/build/paulsim scripts/*.sh muon-sim/scripts/*.sh 2>/dev/null || true

ENV LD_LIBRARY_PATH=/opt/geant4/lib \
    G4INSTALL=/opt/geant4

# Default: full pipeline (Geant4 depth scan -> sim-trained surrogate ->
# sparse survey -> GP flux map -> min-muon location). Override with bash.
ENTRYPOINT ["/bin/bash", "/opt/muography/scripts/docker_pipeline.sh"]
CMD []
