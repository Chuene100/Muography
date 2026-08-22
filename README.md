# paulsim — Geant4 simulation of the PAUL hodoscope

Simulates the 3-plane, 64-strip-per-view scintillator telescope used in the
Huguenot Tunnel muography campaign and writes data in the **exact PAUL .dat
format** consumed by the `muography` Python pipeline.

## Geometry

- 3 scintillator planes (X, Y, X views), 64 strips/plane, 10 mm pitch,
  640 mm active width, default plane spacing 300 mm (`/paul/det/planeSpacing`).
- Optional rock overburden slab (settable thickness/density) placed above the
  muon generation plane to simulate underground attenuation:
  `/paul/rock/enabled true`, `/paul/rock/setThickness 500 m`,
  `/paul/rock/setDensity 2.65 g/cm3`.
- Physics list: FTFP_BERT. Primary: cosmic μ± with cos²θ zenith distribution
  and a Gaisser-like energy spectrum (0.5 GeV – 2 TeV, rejection-sampled),
  configurable via `/paul/gen/*`.

## Output format (identical to PAUL_DATA FORMAT.pdf)

One row per connected plane with ≥2 strips above threshold:
`unix evt fine tdc1 tdc2 plane qc1 qc2 nhits (chan adc)...`
ADC = energy deposit × 50 / MeV, capped at 4095.

## Build

```bash
source Geant4-11.3.0-Darwin/bin/geant4.sh        # or geant4.csh
cd muon-sim
cmake -B build -DGeant4_DIR="$PWD/../Geant4-11.3.0-Darwin/lib/cmake/Geant4"
cmake --build build -j
```

## Run

```bash
mkdir -p output
./build/paulsim macros/run_open.mac              # open-sky reference sample
./scripts/run_depth_scan.sh 50000                # depth scan for ML training
./build/paulsim                                  # interactive + visualization
```

## Feeding the ML pipeline

The Python parser reads these files unchanged:

```python
from muography.dataio import parse_paul_dat
rows = parse_paul_dat("output/open_sky.dat")
```

Use `depth_*m.dat` as labelled muon samples across overburden thicknesses to
retrain the transmission surrogate on simulated transport instead of the
analytic model (`muography/ml_models.py`), and `open_sky.dat` as a pure-muon
positive class for the muon/noise classifier.
