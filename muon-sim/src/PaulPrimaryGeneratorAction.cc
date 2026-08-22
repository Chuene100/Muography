#include "PaulPrimaryGeneratorAction.hh"

#include <CLHEP/Random/Random.h>
#include <G4Event.hh>
#include <G4ParticleGun.hh>
#include <G4ParticleTable.hh>
#include <G4SystemOfUnits.hh>
#include <G4UIcmdWithADoubleAndUnit.hh>
#include <G4UIcmdWithAString.hh>
#include <G4UIdirectory.hh>

#include "PaulDetectorConstruction.hh"

namespace
{
G4double gaisserShape(G4double E_GeV, G4double c)
{
    return std::pow(E_GeV, -2.7) *
           (1.0 / (1.0 + 1.1 * E_GeV * c / 115.0) +
            0.054 / (1.0 + 1.1 * E_GeV * c / 850.0));
}
}

PaulPrimaryGeneratorAction::PaulPrimaryGeneratorAction(PaulDetectorConstruction* det)
    : fDet(det)
{
    auto* particleTable = G4ParticleTable::GetParticleTable();
    fGun = new G4ParticleGun(1);
    fGun->SetParticleDefinition(particleTable->FindParticle("mu-"));

    fDir = new G4UIdirectory("/paul/gen/");
    fDir->SetGuidance("Cosmic muon generator");

    fEMinCmd = new G4UIcmdWithADoubleAndUnit("/paul/gen/eMin", this);
    fEMinCmd->SetUnitCategory("Energy");
    fEMaxCmd = new G4UIcmdWithADoubleAndUnit("/paul/gen/eMax", this);
    fEMaxCmd->SetUnitCategory("Energy");
    fThetaMaxCmd = new G4UIcmdWithADoubleAndUnit("/paul/gen/thetaMax", this);
    fThetaMaxCmd->SetUnitCategory("Angle");
    fSpectrumCmd = new G4UIcmdWithAString("/paul/gen/spectrum", this);
    fMonoCmd = new G4UIcmdWithADoubleAndUnit("/paul/gen/monoEnergy", this);
    fMonoCmd->SetUnitCategory("Energy");
}

PaulPrimaryGeneratorAction::~PaulPrimaryGeneratorAction()
{
    delete fGun;
}

void PaulPrimaryGeneratorAction::GeneratePrimaries(G4Event* event)
{
    G4double cosTheta = SampleCosTheta();
    G4double theta = std::acos(std::max(-1.0, std::min(1.0, cosTheta)));
    G4double phi = CLHEP::HepRandom::getTheEngine()->flat() * 2.0 * CLHEP::pi;
    G4double energy = SampleEnergy(cosTheta);

    if (fDet) {
        const G4double gap = 3.0 * m + 2.0 * 300.0 * mm;
        G4double margin = gap * std::tan(theta) + 1.0 * m;
        G4double half = std::min(0.64 * m + margin, fDet->GetWorldHalfXY());
        G4double x = (2.0 * CLHEP::HepRandom::getTheEngine()->flat() - 1.0) * half;
        G4double y = (2.0 * CLHEP::HepRandom::getTheEngine()->flat() - 1.0) * half;
        fGun->SetParticlePosition(G4ThreeVector(x, y, fDet->GetGenPlaneZ()));
    } else {
        fGun->SetParticlePosition(G4ThreeVector(0, 0, 3.0 * m));
    }

    G4ThreeVector dir(std::sin(theta) * std::cos(phi),
                      std::sin(theta) * std::sin(phi),
                      -std::cos(theta));
    fGun->SetParticleMomentumDirection(dir);
    fGun->SetParticleEnergy(energy);

    if (CLHEP::HepRandom::getTheEngine()->flat() > 0.54)
        fGun->SetParticleDefinition(
            G4ParticleTable::GetParticleTable()->FindParticle("mu+"));
    else
        fGun->SetParticleDefinition(
            G4ParticleTable::GetParticleTable()->FindParticle("mu-"));

    fGun->GeneratePrimaryVertex(event);
}

G4double PaulPrimaryGeneratorAction::SampleCosTheta()
{
    for (int i = 0; i < 10000; ++i) {
        G4double u = CLHEP::HepRandom::getTheEngine()->flat();
        G4double c = 1.0 - u * (1.0 - std::cos(fThetaMax));
        if (CLHEP::HepRandom::getTheEngine()->flat() < c * c)
            return c;
    }
    return 1.0;
}

G4double PaulPrimaryGeneratorAction::SampleEnergy(G4double cosTheta)
{
    if (fMode == "mono") return fMonoE;
    G4double logEmin = std::log10(fEMin / GeV);
    G4double logEmax = std::log10(fEMax / GeV);
    G4double peak = gaisserShape(fEMin / GeV, cosTheta);
    for (int i = 0; i < 100000; ++i) {
        G4double logE = logEmin +
                        CLHEP::HepRandom::getTheEngine()->flat() * (logEmax - logEmin);
        G4double E = std::pow(10.0, logE);
        G4double val = gaisserShape(E, cosTheta);
        if (CLHEP::HepRandom::getTheEngine()->flat() * peak <= val)
            return E * GeV;
    }
    return fEMin;
}

void PaulPrimaryGeneratorAction::SetNewValue(G4UIcommand* cmd, G4String value)
{
    if (cmd == fEMinCmd)
        fEMin = fEMinCmd->GetNewDoubleValue(value);
    else if (cmd == fEMaxCmd)
        fEMax = fEMaxCmd->GetNewDoubleValue(value);
    else if (cmd == fThetaMaxCmd)
        fThetaMax = fThetaMaxCmd->GetNewDoubleValue(value);
    else if (cmd == fSpectrumCmd)
        fMode = value;
    else if (cmd == fMonoCmd)
        fMonoE = fMonoCmd->GetNewDoubleValue(value);
}
