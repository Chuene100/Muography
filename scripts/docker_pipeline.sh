#!/usr/bin/env bash
# Container entrypoint.
#
#   no arguments        -> full pipeline:
#                          1) Geant4 depth-scan (muons through rock)
#                          2) transmission curve from simulated data
#                          3) adaptive sparse survey + GP flux map + minimum search
#   "bash"/other cmd    -> interactive shell / arbitrary command
set -euo pipefail

source /opt/geant4/bin/geant4.sh

if [ "$#" -gt 0 ]; then
    exec "$@"
fi

EVENTS="${PAUL_EVENTS:-20000}"

echo "== [1/2] Geant4 muon transport: depth scan (${EVENTS} events per depth) =="
cd /opt/muography/muon-sim
./scripts/run_depth_scan.sh "${EVENTS}"

echo "== [2/2] ML flux-map prediction from sparse survey =="
cd /opt/muography
python3 analysis/predict_flux_map.py

echo "Done. Figures: analysis/figures/, summary: results/flux_prediction.json"
