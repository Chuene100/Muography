#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "Geant4::G4clhep" for configuration "Release"
set_property(TARGET Geant4::G4clhep APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4clhep PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4clhep.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4clhep.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4clhep )
list(APPEND _cmake_import_check_files_for_Geant4::G4clhep "${_IMPORT_PREFIX}/lib/libG4clhep.dylib" )

# Import target "Geant4::G4zlib" for configuration "Release"
set_property(TARGET Geant4::G4zlib APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4zlib PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4zlib.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4zlib.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4zlib )
list(APPEND _cmake_import_check_files_for_Geant4::G4zlib "${_IMPORT_PREFIX}/lib/libG4zlib.dylib" )

# Import target "Geant4::G4analysis" for configuration "Release"
set_property(TARGET Geant4::G4analysis APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4analysis PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4analysis.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4analysis.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4analysis )
list(APPEND _cmake_import_check_files_for_Geant4::G4analysis "${_IMPORT_PREFIX}/lib/libG4analysis.dylib" )

# Import target "Geant4::G4digits_hits" for configuration "Release"
set_property(TARGET Geant4::G4digits_hits APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4digits_hits PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4graphics_reps;Geant4::G4materials"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4digits_hits.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4digits_hits.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4digits_hits )
list(APPEND _cmake_import_check_files_for_Geant4::G4digits_hits "${_IMPORT_PREFIX}/lib/libG4digits_hits.dylib" )

# Import target "Geant4::G4error_propagation" for configuration "Release"
set_property(TARGET Geant4::G4error_propagation APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4error_propagation PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4event"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4error_propagation.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4error_propagation.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4error_propagation )
list(APPEND _cmake_import_check_files_for_Geant4::G4error_propagation "${_IMPORT_PREFIX}/lib/libG4error_propagation.dylib" )

# Import target "Geant4::G4event" for configuration "Release"
set_property(TARGET Geant4::G4event APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4event PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4graphics_reps;Geant4::G4materials;Geant4::G4processes"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4event.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4event.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4event )
list(APPEND _cmake_import_check_files_for_Geant4::G4event "${_IMPORT_PREFIX}/lib/libG4event.dylib" )

# Import target "Geant4::G3toG4" for configuration "Release"
set_property(TARGET Geant4::G3toG4 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G3toG4 PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4graphics_reps;Geant4::G4processes"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG3toG4.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG3toG4.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G3toG4 )
list(APPEND _cmake_import_check_files_for_Geant4::G3toG4 "${_IMPORT_PREFIX}/lib/libG3toG4.dylib" )

# Import target "Geant4::G4geometry" for configuration "Release"
set_property(TARGET Geant4::G4geometry APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4geometry PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4materials"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4geometry.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4geometry.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4geometry )
list(APPEND _cmake_import_check_files_for_Geant4::G4geometry "${_IMPORT_PREFIX}/lib/libG4geometry.dylib" )

# Import target "Geant4::G4global" for configuration "Release"
set_property(TARGET Geant4::G4global APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4global PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4global.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4global.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4global )
list(APPEND _cmake_import_check_files_for_Geant4::G4global "${_IMPORT_PREFIX}/lib/libG4global.dylib" )

# Import target "Geant4::G4graphics_reps" for configuration "Release"
set_property(TARGET Geant4::G4graphics_reps APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4graphics_reps PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4intercoms"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4graphics_reps.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4graphics_reps.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4graphics_reps )
list(APPEND _cmake_import_check_files_for_Geant4::G4graphics_reps "${_IMPORT_PREFIX}/lib/libG4graphics_reps.dylib" )

# Import target "Geant4::G4intercoms" for configuration "Release"
set_property(TARGET Geant4::G4intercoms APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4intercoms PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4intercoms.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4intercoms.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4intercoms )
list(APPEND _cmake_import_check_files_for_Geant4::G4intercoms "${_IMPORT_PREFIX}/lib/libG4intercoms.dylib" )

# Import target "Geant4::G4interfaces" for configuration "Release"
set_property(TARGET Geant4::G4interfaces APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4interfaces PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4interfaces.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4interfaces.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4interfaces )
list(APPEND _cmake_import_check_files_for_Geant4::G4interfaces "${_IMPORT_PREFIX}/lib/libG4interfaces.dylib" )

# Import target "Geant4::G4materials" for configuration "Release"
set_property(TARGET Geant4::G4materials APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4materials PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4zlib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4materials.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4materials.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4materials )
list(APPEND _cmake_import_check_files_for_Geant4::G4materials "${_IMPORT_PREFIX}/lib/libG4materials.dylib" )

# Import target "Geant4::G4parmodels" for configuration "Release"
set_property(TARGET Geant4::G4parmodels APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4parmodels PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4graphics_reps"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4parmodels.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4parmodels.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4parmodels )
list(APPEND _cmake_import_check_files_for_Geant4::G4parmodels "${_IMPORT_PREFIX}/lib/libG4parmodels.dylib" )

# Import target "Geant4::G4particles" for configuration "Release"
set_property(TARGET Geant4::G4particles APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4particles PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4particles.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4particles.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4particles )
list(APPEND _cmake_import_check_files_for_Geant4::G4particles "${_IMPORT_PREFIX}/lib/libG4particles.dylib" )

# Import target "Geant4::G4geomtext" for configuration "Release"
set_property(TARGET Geant4::G4geomtext APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4geomtext PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4graphics_reps"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4geomtext.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4geomtext.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4geomtext )
list(APPEND _cmake_import_check_files_for_Geant4::G4geomtext "${_IMPORT_PREFIX}/lib/libG4geomtext.dylib" )

# Import target "Geant4::G4mctruth" for configuration "Release"
set_property(TARGET Geant4::G4mctruth APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4mctruth PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4mctruth.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4mctruth.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4mctruth )
list(APPEND _cmake_import_check_files_for_Geant4::G4mctruth "${_IMPORT_PREFIX}/lib/libG4mctruth.dylib" )

# Import target "Geant4::G4physicslists" for configuration "Release"
set_property(TARGET Geant4::G4physicslists APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4physicslists PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4track"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4physicslists.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4physicslists.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4physicslists )
list(APPEND _cmake_import_check_files_for_Geant4::G4physicslists "${_IMPORT_PREFIX}/lib/libG4physicslists.dylib" )

# Import target "Geant4::G4processes" for configuration "Release"
set_property(TARGET Geant4::G4processes APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4processes PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4analysis;Geant4::G4zlib"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4processes.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4processes.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4processes )
list(APPEND _cmake_import_check_files_for_Geant4::G4processes "${_IMPORT_PREFIX}/lib/libG4processes.dylib" )

# Import target "Geant4::G4readout" for configuration "Release"
set_property(TARGET Geant4::G4readout APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4readout PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4event;Geant4::G4run"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4readout.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4readout.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4readout )
list(APPEND _cmake_import_check_files_for_Geant4::G4readout "${_IMPORT_PREFIX}/lib/libG4readout.dylib" )

# Import target "Geant4::G4run" for configuration "Release"
set_property(TARGET Geant4::G4run APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4run PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4geometry;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4materials;Geant4::G4track"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4run.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4run.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4run )
list(APPEND _cmake_import_check_files_for_Geant4::G4run "${_IMPORT_PREFIX}/lib/libG4run.dylib" )

# Import target "Geant4::G4track" for configuration "Release"
set_property(TARGET Geant4::G4track APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4track PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4track.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4track.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4track )
list(APPEND _cmake_import_check_files_for_Geant4::G4track "${_IMPORT_PREFIX}/lib/libG4track.dylib" )

# Import target "Geant4::G4tracking" for configuration "Release"
set_property(TARGET Geant4::G4tracking APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4tracking PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4graphics_reps"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4tracking.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4tracking.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4tracking )
list(APPEND _cmake_import_check_files_for_Geant4::G4tracking "${_IMPORT_PREFIX}/lib/libG4tracking.dylib" )

# Import target "Geant4::G4FR" for configuration "Release"
set_property(TARGET Geant4::G4FR APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4FR PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4modeling"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4FR.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4FR.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4FR )
list(APPEND _cmake_import_check_files_for_Geant4::G4FR "${_IMPORT_PREFIX}/lib/libG4FR.dylib" )

# Import target "Geant4::G4visHepRep" for configuration "Release"
set_property(TARGET Geant4::G4visHepRep APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4visHepRep PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4geometry;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4materials;Geant4::G4modeling;Geant4::G4tracking"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4visHepRep.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4visHepRep.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4visHepRep )
list(APPEND _cmake_import_check_files_for_Geant4::G4visHepRep "${_IMPORT_PREFIX}/lib/libG4visHepRep.dylib" )

# Import target "Geant4::G4RayTracer" for configuration "Release"
set_property(TARGET Geant4::G4RayTracer APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4RayTracer PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4event;Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4modeling;Geant4::G4particles;Geant4::G4processes;Geant4::G4run;Geant4::G4track;Geant4::G4tracking"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4RayTracer.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4RayTracer.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4RayTracer )
list(APPEND _cmake_import_check_files_for_Geant4::G4RayTracer "${_IMPORT_PREFIX}/lib/libG4RayTracer.dylib" )

# Import target "Geant4::G4Tree" for configuration "Release"
set_property(TARGET Geant4::G4Tree APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4Tree PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4materials;Geant4::G4modeling"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4Tree.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4Tree.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4Tree )
list(APPEND _cmake_import_check_files_for_Geant4::G4Tree "${_IMPORT_PREFIX}/lib/libG4Tree.dylib" )

# Import target "Geant4::G4VRML" for configuration "Release"
set_property(TARGET Geant4::G4VRML APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4VRML PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4modeling"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4VRML.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4VRML.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4VRML )
list(APPEND _cmake_import_check_files_for_Geant4::G4VRML "${_IMPORT_PREFIX}/lib/libG4VRML.dylib" )

# Import target "Geant4::G4GMocren" for configuration "Release"
set_property(TARGET Geant4::G4GMocren APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4GMocren PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4digits_hits;Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4materials;Geant4::G4modeling;Geant4::G4tracking"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4GMocren.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4GMocren.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4GMocren )
list(APPEND _cmake_import_check_files_for_Geant4::G4GMocren "${_IMPORT_PREFIX}/lib/libG4GMocren.dylib" )

# Import target "Geant4::G4vis_management" for configuration "Release"
set_property(TARGET Geant4::G4vis_management APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4vis_management PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4event;Geant4::G4geometry;Geant4::G4interfaces;Geant4::G4materials;Geant4::G4particles;Geant4::G4run;Geant4::G4tracking"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4vis_management.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4vis_management.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4vis_management )
list(APPEND _cmake_import_check_files_for_Geant4::G4vis_management "${_IMPORT_PREFIX}/lib/libG4vis_management.dylib" )

# Import target "Geant4::G4modeling" for configuration "Release"
set_property(TARGET Geant4::G4modeling APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4modeling PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4event;Geant4::G4materials;Geant4::G4run"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4modeling.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4modeling.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4modeling )
list(APPEND _cmake_import_check_files_for_Geant4::G4modeling "${_IMPORT_PREFIX}/lib/libG4modeling.dylib" )

# Import target "Geant4::G4ToolsSG" for configuration "Release"
set_property(TARGET Geant4::G4ToolsSG APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4ToolsSG PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4geometry;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4modeling"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4ToolsSG.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4ToolsSG.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4ToolsSG )
list(APPEND _cmake_import_check_files_for_Geant4::G4ToolsSG "${_IMPORT_PREFIX}/lib/libG4ToolsSG.dylib" )

# Import target "Geant4::G4OpenGL" for configuration "Release"
set_property(TARGET Geant4::G4OpenGL APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(Geant4::G4OpenGL PROPERTIES
  IMPORTED_LINK_DEPENDENT_LIBRARIES_RELEASE "Geant4::G4geometry;Geant4::G4global;Geant4::G4graphics_reps;Geant4::G4intercoms;Geant4::G4modeling;Geant4::G4run"
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4OpenGL.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4OpenGL.dylib"
  )

list(APPEND _cmake_import_check_targets Geant4::G4OpenGL )
list(APPEND _cmake_import_check_files_for_Geant4::G4OpenGL "${_IMPORT_PREFIX}/lib/libG4OpenGL.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
