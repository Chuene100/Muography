#!/bin/zsh
SCRIPT_DIR="${0:A:h}"
export G4ROOT="$SCRIPT_DIR/../Geant4-11.3.0-Darwin"
export G4ENSDFSTATEDATA="$G4ROOT/share/Geant4/data/G4ENSDFSTATE3.0"
export G4LEVELGAMMADATA="$G4ROOT/share/Geant4/data/PhotonEvaporation6.1"
export G4LEDATA="$G4ROOT/share/Geant4/data/G4EMLOW8.6.1"
exec "$SCRIPT_DIR/../muon-sim/build/paulsim" "$@"
