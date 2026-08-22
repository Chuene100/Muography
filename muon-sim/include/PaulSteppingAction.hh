#ifndef PaulSteppingAction_h
#define PaulSteppingAction_h

#include <map>
#include <G4UserSteppingAction.hh>
#include <globals.hh>

class G4Event;

class PaulSteppingAction : public G4UserSteppingAction
{
  public:
    void UserSteppingAction(const G4Step* step) override;
    void Clear() { fEdep.clear(); }
    const std::map<G4int, G4double>& GetMap() const { return fEdep; }

  private:
    std::map<G4int, G4double> fEdep;
};

#endif
