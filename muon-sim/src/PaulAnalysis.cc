#include "PaulAnalysis.hh"

#include <filesystem>
#include <iostream>

PaulAnalysis* PaulAnalysis::fgInstance = nullptr;

void PaulAnalysis::OpenFile(const G4String& name)
{
    CloseFile();
    std::filesystem::path p(static_cast<const char*>(name));
    if (p.has_parent_path())
        std::filesystem::create_directories(p.parent_path());
    fFile.open(name, std::ios::out | std::ios::trunc);
    if (!fFile.is_open())
        std::cerr << "PAUL WARNING: cannot open output file '" << name << "'\n";
}

void PaulAnalysis::CloseFile()
{
    if (fFile.is_open()) fFile.close();
}

void PaulAnalysis::WriteRow(const std::string& row)
{
    if (!fFile.is_open()) return;
    fFile << row << "\n";
    ++fRows;
}
