#!/bin/zsh
set -e
cd "$(dirname "$0")/.."
export GEANT4MAKE="$PWD/../Geant4-11.3.0-Darwin/share/Geant4/geant4make"
if [ ! -d "$GEANT4MAKE" ]; then
  echo "geant4make not found at $GEANT4MAKE"
  exit 1
fi

G4ROOT="$(cd "$GEANT4MAKE/../../.." && pwd)"
G4INC="$G4ROOT/include/Geant4"
G4LIB="$G4ROOT/lib"

echo "Using includes: $G4INC"
echo "Using libs:     $G4LIB"

mkdir -p ../build_sim
LIBS=("$G4LIB"/libG4*.dylib(N))
clang++ -std=c++17 -O2 -Wall \
  -I"$G4INC" \
  -Iinclude \
  paulsim.cc src/*.cc \
  "${LIBS[@]}" \
  -Wl,-rpath,"$G4LIB" \
  -o ../build_sim/paulsim

echo "Built ../build_sim/paulsim"
