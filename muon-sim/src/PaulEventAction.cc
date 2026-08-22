#include "PaulEventAction.hh"

#include <cstdio>
#include <string>
#include <G4Event.hh>
#include <G4SystemOfUnits.hh>

#include "PaulAnalysis.hh"
#include "PaulSteppingAction.hh"

void PaulEventAction::BeginOfEventAction(const G4Event*)
{
    fStepAction->Clear();
}

void PaulEventAction::EndOfEventAction(const G4Event* event)
{
    if (!PaulAnalysis::Instance()->IsOpen()) return;

    const G4int evId = event->GetEventID();
    char buf[512];

    for (G4int plane = 0; plane < 3; ++plane) {
        std::string row = std::to_string(fStartUnix + evId / 100000) + " " +
                          std::to_string(evId) + " " +
                          std::to_string((evId * 1000 + plane * 7) % 100000000) +
                          " " + std::to_string(10 + (evId % 5)) + " " +
                          std::to_string(12 + (evId % 6)) + " " +
                          std::to_string(plane) + " 0 0 ";
        int nHits = 0;
        std::string hits;
        for (auto& kv : fStepAction->GetMap()) {
            const int keyPlane = kv.first / 100;
            const int strip = kv.first % 100;
            if (keyPlane != plane) continue;
            int adc = static_cast<int>(kv.second / MeV * fAdcPerMeV);
            if (adc <= 0) continue;
            if (adc > 4095) adc = 4095;
            snprintf(buf, sizeof(buf), "%d %d ", strip, adc);
            hits += buf;
            ++nHits;
        }
        if (nHits >= 1) {
            row += std::to_string(nHits) + " " + hits;
            PaulAnalysis::Instance()->WriteRow(row);
        }
    }
}
