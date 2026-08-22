#ifndef PaulDetectorConstruction_h
#define PaulDetectorConstruction_h

#include <globals.hh>
#include <G4VUserDetectorConstruction.hh>
#include <G4UImessenger.hh>
#include <G4SystemOfUnits.hh>

class G4VPhysicalVolume;
class G4UIcmdWithADoubleAndUnit;
class G4UIcmdWithABool;
class G4UIdirectory;
class PaulDetectorMessenger;

class PaulDetectorConstruction : public G4VUserDetectorConstruction
{
  public:
    PaulDetectorConstruction();
    ~PaulDetectorConstruction() override;
    G4VPhysicalVolume* Construct() override;

    void SetPlaneSpacing(G4double v) { fPlaneSpacing = v; }
    void SetRockThickness(G4double v) { fRockThickness = v; }
    void SetRockDensity(G4double v) { fRockDensity = v; }
    void SetRockEnabled(G4bool v) { fRockEnabled = v; }
    G4double GetGenPlaneZ() const { return fGenZ; }
    G4double GetWorldHalfXY() const { return fWorldHalfXY; }

  private:
    G4double fPlaneSpacing = 300.0 * mm;
    G4double fRockThickness = 0.0;
    G4double fRockDensity = 2.65 * g / cm3;
    G4bool fRockEnabled = false;
    G4double fGenZ = 3.0 * m + 2.0 * 300.0 * mm + 10.0 * cm;
    G4double fWorldHalfXY = 1.5 * m;
    PaulDetectorMessenger* fMessenger = nullptr;

    friend class PaulDetectorMessenger;
};

class PaulDetectorMessenger : public G4UImessenger
{
  public:
    explicit PaulDetectorMessenger(PaulDetectorConstruction* det);
    ~PaulDetectorMessenger() override;
    void SetNewValue(G4UIcommand* cmd, G4String value) override;

  private:
    PaulDetectorConstruction* fDet = nullptr;
    G4UIdirectory* fDir = nullptr;
    G4UIdirectory* fRockDir = nullptr;
    G4UIcmdWithADoubleAndUnit* fSpacingCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fThickCmd = nullptr;
    G4UIcmdWithADoubleAndUnit* fDensCmd = nullptr;
    G4UIcmdWithABool* fRockOnCmd = nullptr;
};

#endif
