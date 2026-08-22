#ifndef PaulRunAction_h
#define PaulRunAction_h

#include <G4UserRunAction.hh>
#include <globals.hh>

class PaulRunAction : public G4UserRunAction
{
  public:
    PaulRunAction() = default;
    void EndOfRunAction(const G4Run* run) override;
};

#endif
