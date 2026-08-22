#ifndef PaulPrimaryGeneratorAction_h
#define PaulPrimaryGeneratorAction_h

#include <G4VUserPrimaryGeneratorAction.hh>
#include <G4UImessenger.hh>
#include <G4SystemOfUnits.hh>

class G4ParticleGun;
class G4UIdirectory;
class G4UIcmdWithADoubleAndUnit;
class G4UIcmdWithAString;
class PaulDetectorConstruction;

class PaulPrimaryGeneratorAction : public G4VUserPrimaryGeneratorAction,
                                   public G4UImessenger
{
  public:
    explicit PaulPrimaryGeneratorAction(PaulDetectorConstruction* det = nullptr);
    ~PaulPrimaryGeneratorAction() override;
    void GeneratePrimaries(G4Event* event) override;
    void SetNewValue(G4UIcommand* cmd, G4String value) override;

  private:
    G4double SampleEnergy(G4double cosTheta);
    G4double SampleCosTheta();
    G4ParticleGun* fGun = nullptr;
    PaulDetectorConstruction* fDet = nullptr;
    G4UIdirectory* fDir = nullptr;
    G4UIcmdWithADoubleAndUnit* fEMinCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fEMaxCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fThetaMaxCmd = nullptr;
    G4UIcmdWithAString* fSpectrumCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fMonoCmd = nullptr;
    G4double fEMin = 0.5 * GeV;
    G4double fEMax = 2000.0 * GeV;
    G4double fThetaMax = 70.0 * deg;
    G4String fMode = "gaisser";
    G4double fMonoE = 10.0 * GeV;

  public:
    void SetDetector(PaulDetectorConstruction* det) { fDet = det; }
};

#endif
