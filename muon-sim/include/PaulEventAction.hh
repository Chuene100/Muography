#ifndef PaulEventAction_h
#define PaulEventAction_h

#include <G4UserEventAction.hh>
#include <globals.hh>

class PaulSteppingAction;

class PaulEventAction : public G4UserEventAction
{
  public:
    explicit PaulEventAction(PaulSteppingAction* stepAction)
        : fStepAction(stepAction) {}
    void BeginOfEventAction(const G4Event* event) override;
    void EndOfEventAction(const G4Event* event) override;

  private:
    PaulSteppingAction* fStepAction = nullptr;
    static constexpr G4double fAdcPerMeV = 50.0;
    static constexpr G4int fStartUnix = 1712934934;
};

#endif
