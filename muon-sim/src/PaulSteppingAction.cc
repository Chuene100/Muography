#include "PaulSteppingAction.hh"

#include <G4Step.hh>
#include <G4TouchableHistory.hh>

void PaulSteppingAction::UserSteppingAction(const G4Step* step)
{
    auto* vol = step->GetPreStepPoint()->GetTouchable()->GetVolume();
    if (!vol) return;
    const G4String& lvName = vol->GetLogicalVolume()->GetName();
    if (lvName.find("stripLV") == G4String::npos) return;

    const G4double edep = step->GetTotalEnergyDeposit();
    if (edep <= 0.) return;

    const G4VTouchable* touch = step->GetPreStepPoint()->GetTouchable();
    G4int strip = touch->GetCopyNumber(0);
    G4int plane = touch->GetCopyNumber(1);
    fEdep[plane * 100 + strip] += edep;
}
