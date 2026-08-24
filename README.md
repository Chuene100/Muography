<<<<<<< HEAD
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

# Muography — Geant4 + ML underground muon-flux mapping

Simulate cosmic-ray muons travelling through rock overburden with **Geant4**
(`muon-sim/`, the PAUL hodoscope telescope), then use **machine learning** to
do what the detector alone cannot: instead of physically deploying the
telescope at every underground location — which takes months of counting time
— measure a *sparse* set of stations, train a Gaussian-process flux map, and
predict the location with the **fewest muon hits** anywhere on the site.

## Pipeline

```
Geant4 depth scan            transmission curve          GP flux map
(muons through rock)   -->   trained on simulated  -->   from sparse,
depth_0..1000 m .dat         transport, not just the     noisy deployments
                             analytic range-energy model
                                                          --> min-muon location
```

1. `scripts/run_depth_scan.sh` fires Gaisser-spectrum μ± through 0–1000 m of
   rock onto the 3-plane strip telescope and writes PAUL-format `.dat` files.
2. `analysis/predict_flux_map.py` builds a transmission curve from those
   simulated samples (falls back to the analytic model if absent), creates a
   synthetic site with uneven overburden, simulates sparse detector
   deployments (Poisson counts over days), fits a GP over log-rate, and uses
   active learning to pick each next station where uncertainty is largest.
3. Outputs: `results/flux_prediction.json` + `analysis/figures/flux_map_prediction.png`
   (true vs predicted maps, uncertainty map, convergence of the predicted
   minimum location).

## Docker (recommended)

The image builds Geant4 11.3.0 from source (first build takes ~30–60 min),
compiles `paulsim`, and ships the Python ML stack:

```bash
docker build -t muography .
docker run --rm -v "$PWD/results:/opt/muography/results" \
             -v "$PWD/analysis/figures:/opt/muography/analysis/figures" muography
```

Useful knobs and variants:

```bash
docker run --rm -e PAUL_EVENTS=50000 muography      # events per depth point
docker run --rm -it muography bash                   # interactive shell
docker run --rm muography ./build/paulsim macros/run_open.mac   # custom command
```

## Native (macOS) workflow

```bash
source Geant4-11.3.0-Darwin/bin/geant4.sh
cmake --build muon-sim/build -j                      # paulsim already configured
muon-sim/scripts/run_depth_scan.sh 20000
.venv/bin/python analysis/predict_flux_map.py
```

## Layout

| Path | Purpose |
| --- | --- |
| `muon-sim/` | Geant4 application (`paulsim`) + macros + depth-scan script |
| `muography/survey.py` | site model, transmission curve, Poisson station simulation, GP fit, active learning, minimum search |
| `muography/ml_models.py` | existing surrogates/classifiers for real PAUL data |
| `analysis/predict_flux_map.py` | end-to-end flux-mapping driver |
| `results/`, `analysis/figures/` | JSON summaries and figures |
>>>>>>> 44846461 (Added predict_flux_map.py, dockerfile)
