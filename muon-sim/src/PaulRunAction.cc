#include "PaulRunAction.hh"

#include <iostream>
#include <G4Run.hh>

#include "PaulAnalysis.hh"

void PaulRunAction::EndOfRunAction(const G4Run* run)
{
    G4cout << "PaulRun: events=" << run->GetNumberOfEvent()
           << " rows written=" << PaulAnalysis::Instance()->RowsWritten()
           << G4endl;
}
