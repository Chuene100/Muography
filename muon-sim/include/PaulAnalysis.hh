#ifndef PaulAnalysis_h
#define PaulAnalysis_h

#include <fstream>
#include <G4String.hh>
#include <G4UImessenger.hh>
#include <G4UIcmdWithAString.hh>
#include <G4UIcmdWithoutParameter.hh>

class PaulAnalysis
{
  public:
    static PaulAnalysis* Instance()
    {
        if (!fgInstance) fgInstance = new PaulAnalysis();
        return fgInstance;
    }

    void OpenFile(const G4String& name);
    void CloseFile();
    void WriteRow(const std::string& row);
    G4bool IsOpen() const { return fFile.is_open(); }
    G4int RowsWritten() const { return fRows; }
    void ResetCounter() { fRows = 0; }

  private:
    PaulAnalysis() = default;
    static PaulAnalysis* fgInstance;
    std::ofstream fFile;
    G4int fRows = 0;
};

class PaulOutputMessenger : public G4UImessenger
{
  public:
    PaulOutputMessenger()
    {
        fDir = new G4UIdirectory("/paul/output/");
        fDir->SetGuidance("PAUL data file output");
        fCmd = new G4UIcmdWithAString("/paul/output/file", this);
        fCmd->SetGuidance("Set output .dat file and start writing");
        fClose = new G4UIcmdWithoutParameter("/paul/output/close", this);
    }

    void SetNewValue(G4UIcommand* command, G4String value) override
    {
        auto* analysis = PaulAnalysis::Instance();
        if (command == fClose) {
            analysis->CloseFile();
            return;
        }

        if (command == fCmd) {
            analysis->CloseFile();
            analysis->ResetCounter();
            if (!value.empty()) analysis->OpenFile(value);
        }
    }

  private:
    G4UIdirectory* fDir = nullptr;
    G4UIcmdWithAString* fCmd = nullptr;
    G4UIcmdWithoutParameter* fClose = nullptr;
};

#endif
