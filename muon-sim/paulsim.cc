#include <G4RunManagerFactory.hh>
#include <G4UIExecutive.hh>
#include <G4UImanager.hh>
#include <G4VisExecutive.hh>
#include <G4VModularPhysicsList.hh>
#include <G4EmStandardPhysics.hh>
#include <FTFP_BERT.hh>

#include "PaulAnalysis.hh"
#include "PaulDetectorConstruction.hh"
#include "PaulEventAction.hh"
#include "PaulPrimaryGeneratorAction.hh"
#include "PaulRunAction.hh"
#include "PaulSteppingAction.hh"

class PaulPhysicsEM : public G4VModularPhysicsList
{
  public:
    PaulPhysicsEM()
    {
        RegisterPhysics(new G4EmStandardPhysics());
        SetCutValue(1.0 * CLHEP::mm, "gamma");
        SetCutValue(1.0 * CLHEP::mm, "e-");
        SetCutValue(1.0 * CLHEP::mm, "e+");
    }
};

int main(int argc, char** argv)
{
    PaulOutputMessenger outputMessenger;
    auto* runManager = G4RunManagerFactory::CreateRunManager(G4RunManagerType::SerialOnly);

    const char* fullPhys = std::getenv("PAUL_FULL_PHYSICS");
    if (fullPhys) {
        runManager->SetUserInitialization(new FTFP_BERT);
    } else {
        runManager->SetUserInitialization(new PaulPhysicsEM);
    }

    auto* det = new PaulDetectorConstruction();
    runManager->SetUserInitialization(det);
    auto* gen = new PaulPrimaryGeneratorAction();
    gen->SetDetector(det);
    runManager->SetUserAction(gen);

    auto* runAction = new PaulRunAction();
    auto* stepAction = new PaulSteppingAction();
    auto* eventAction = new PaulEventAction(stepAction);
    runManager->SetUserAction(runAction);
    runManager->SetUserAction(eventAction);
    runManager->SetUserAction(stepAction);

    G4VisManager* visManager = nullptr;

    G4UImanager* UImanager = G4UImanager::GetUIpointer();
    if (argc == 1) {
        visManager = new G4VisExecutive;
        visManager->Initialize();
        G4UIExecutive exec(argc, argv);
        UImanager->ApplyCommand("/control/execute macros/vis.mac");
        exec.SessionStart();
    } else {
        G4String command = "/control/execute ";
        UImanager->ApplyCommand(command + argv[1]);
    }

    delete visManager;
    delete runManager;
    return 0;
}
