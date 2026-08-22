#include "PaulDetectorConstruction.hh"

#include <G4NistManager.hh>
#include <G4Box.hh>
#include <G4LogicalVolume.hh>
#include <G4PVPlacement.hh>
#include <G4SystemOfUnits.hh>
#include <G4VisAttributes.hh>
#include <G4Colour.hh>
#include <G4RunManager.hh>
#include <G4UIcmdWithADoubleAndUnit.hh>
#include <G4UIcmdWithABool.hh>
#include <G4Material.hh>

#include <map>

namespace
{
G4Material* MakeRockMaterial(G4double density)
{
    static std::map<G4double, G4Material*> cache;
    auto it = cache.find(density);
    if (it != cache.end()) return it->second;

    auto* SiO2 = G4NistManager::Instance()->FindOrBuildMaterial("G4_SILICON_DIOXIDE");
    auto* rock = new G4Material("PaulRock", density, 1);
    rock->AddMaterial(SiO2, 100.0 * perCent);
    cache[density] = rock;
    return rock;
}
}

PaulDetectorConstruction::PaulDetectorConstruction()
{
    fMessenger = new PaulDetectorMessenger(this);
}

PaulDetectorConstruction::~PaulDetectorConstruction()
{
    delete fMessenger;
}

G4VPhysicalVolume* PaulDetectorConstruction::Construct()
{
    auto* nist = G4NistManager::Instance();
    auto* air = nist->FindOrBuildMaterial("G4_AIR");
    auto* scint = nist->FindOrBuildMaterial("G4_PLASTIC_SC_VINYLTOLUENE");
    auto* alu = nist->FindOrBuildMaterial("G4_Al");

    const G4int nStrips = 64;
    const G4double pitch = 10.0 * mm;
    const G4double stripL = nStrips * pitch;
    const G4double stripT = 10.0 * mm;
    const G4double gap = 3.0 * m;

    // Layout (z up): bottom plane at local z=0, top plane at 2*fPlaneSpacing,
    // generation plane at top+gap; an optional rock slab sits ABOVE the
    // generation plane and primaries start on its top face so every muon
    // traverses the full overburden before reaching the hodoscope.
    const G4double zTopPlane = 2.0 * fPlaneSpacing;
    const G4double rockT =
        (fRockEnabled && fRockThickness > 0) ? fRockThickness : 0.0;
    const G4double zGenLocal = zTopPlane + gap + rockT;

    const G4double zWorldBot = -stripT / 2.0 - 10.0 * cm;
    const G4double zWorldTop = zGenLocal + stripT / 2.0 + 10.0 * cm;
    const G4double worldZ = zWorldTop - zWorldBot;
    const G4double zC = (zWorldTop + zWorldBot) / 2.0;

    const G4double worldHalfXY = std::max(3.0 * m, stripL / 2.0 + 0.5 * m);
    fWorldHalfXY = worldHalfXY;

    auto* worldSolid =
        new G4Box("world", worldHalfXY, worldHalfXY, worldZ / 2);
    auto* worldLV = new G4LogicalVolume(worldSolid, air, "world");
    // World must be centered on the origin: offset all contents instead.
    const G4double zO = -zC;
    auto* worldPV = new G4PVPlacement(nullptr, G4ThreeVector(), worldLV,
                                      "world", nullptr, false, 0);

    fGenZ = zGenLocal + zO;

    for (G4int p = 0; p < 3; ++p) {
        G4double zPos = p * fPlaneSpacing + zO;
        auto* planeBox =
            new G4Box("planeBox", stripL / 2, stripL / 2, stripT / 2);
        auto* planeLV =
            new G4LogicalVolume(planeBox, air, "planeLV" + std::to_string(p));
        new G4PVPlacement(nullptr, G4ThreeVector(0, 0, zPos), planeLV,
                          "planePV" + std::to_string(p), worldLV, false, p);

        for (G4int s = 0; s < nStrips; ++s) {
            G4double offset = (s - (nStrips - 1) / 2.0) * pitch;
            G4Box* stripSolid;
            if (p == 1)
                stripSolid = new G4Box("strip", pitch / 2, stripL / 2, stripT / 2);
            else
                stripSolid = new G4Box("strip", stripL / 2, pitch / 2, stripT / 2);

            auto* stripLV = new G4LogicalVolume(
                stripSolid, scint, "stripLV" + std::to_string(p));
            G4ThreeVector pos = (p == 1)
                                    ? G4ThreeVector(offset, 0, 0)
                                    : G4ThreeVector(0, offset, 0);
            new G4PVPlacement(nullptr, pos, stripLV,
                              "stripPV_" + std::to_string(p) + "_" +
                                  std::to_string(s),
                              planeLV, false, s);

            G4VisAttributes vis(G4Colour(0.2 + 0.3 * p, 0.4, 0.8 - 0.25 * p));
            vis.SetForceWireframe(true);
            stripLV->SetVisAttributes(vis);
        }

        // Aluminium support plate directly beneath each plane (touching,
        // not overlapping): spans [zPos-9mm, zPos-5mm].
        auto* frameSolid =
            new G4Box("frame", stripL / 2, stripL / 2, 2.0 * mm);
        auto* frameLV = new G4LogicalVolume(frameSolid, alu, "frameLV");
        new G4PVPlacement(nullptr, G4ThreeVector(0, 0, zPos - 7.0 * mm),
                          frameLV, "framePV" + std::to_string(p), worldLV,
                          false, p);
    }

    if (rockT > 0) {
        auto* rockMat = MakeRockMaterial(fRockDensity);
        auto* rockSolid =
            new G4Box("rock", worldHalfXY, worldHalfXY, rockT / 2);
        auto* rockLV = new G4LogicalVolume(rockSolid, rockMat, "rockLV");
        // Slab spans local [zTopPlane+gap, zTopPlane+gap+rockT]; primaries
        // start on its upper face at fGenZ.
        new G4PVPlacement(nullptr,
                          G4ThreeVector(0, 0, zTopPlane + gap + rockT / 2 + zO),
                          rockLV, "rockPV", worldLV, false, 0);
        G4VisAttributes rv(G4Colour(0.45, 0.35, 0.25));
        rv.SetForceSolid(true);
        rockLV->SetVisAttributes(rv);
    }

    worldLV->SetVisAttributes(G4VisAttributes::GetInvisible());
    return worldPV;
}

PaulDetectorMessenger::PaulDetectorMessenger(PaulDetectorConstruction* det)
    : fDet(det)
{
    fDir = new G4UIdirectory("/paul/det/");
    fDir->SetGuidance("PAUL detector parameters");

    fSpacingCmd =
        new G4UIcmdWithADoubleAndUnit("/paul/det/planeSpacing", this);
    fSpacingCmd->SetUnitCategory("Length");

    fRockDir = new G4UIdirectory("/paul/rock/");
    fRockDir->SetGuidance("Overburden rock slab configuration");

    fThickCmd = new G4UIcmdWithADoubleAndUnit("/paul/rock/setThickness", this);
    fThickCmd->SetUnitCategory("Length");

    fDensCmd = new G4UIcmdWithADoubleAndUnit("/paul/rock/setDensity", this);
    fDensCmd->SetUnitCategory("Volumic Mass");

    fRockOnCmd = new G4UIcmdWithABool("/paul/rock/enabled", this);
}

PaulDetectorMessenger::~PaulDetectorMessenger() = default;

void PaulDetectorMessenger::SetNewValue(G4UIcommand* cmd, G4String value)
{
    G4bool changed = true;
    if (cmd == fSpacingCmd)
        fDet->SetPlaneSpacing(fSpacingCmd->GetNewDoubleValue(value));
    else if (cmd == fThickCmd)
        fDet->SetRockThickness(fThickCmd->GetNewDoubleValue(value));
    else if (cmd == fDensCmd)
        fDet->SetRockDensity(fDensCmd->GetNewDoubleValue(value));
    else if (cmd == fRockOnCmd)
        fDet->SetRockEnabled(fRockOnCmd->GetNewBoolValue(value));
    else
        changed = false;
    if (changed)
        G4RunManager::GetRunManager()->ReinitializeGeometry(true);
}
