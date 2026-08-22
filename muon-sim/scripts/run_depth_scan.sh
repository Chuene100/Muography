#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
mkdir -p output

NEVENTS=${1:-50000}

for T in 0 100 250 500 750 1000; do
  MAC="output/_depth_${T}.mac"
  cat > "$MAC" <<EOF
/run/initialize
/paul/gen/eMin 0.5 GeV
/paul/gen/eMax 2000 GeV
/paul/gen/spectrum gaisser
/paul/rock/enabled $( [ "$T" -gt 0 ] && echo true || echo false )
$( [ "$T" -gt 0 ] && echo "/paul/rock/setThickness $T m" )
/paul/output/file output/depth_${T}m.dat
/run/beamOn $NEVENTS
/paul/output/close
exit
EOF
  echo "=== depth ${T} m rock ==="
  ./build/paulsim "$MAC"
done
echo "Depth scan complete: muon-sim/output/depth_*m.dat"
