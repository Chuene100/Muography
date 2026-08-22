#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "PTL::ptl-shared" for configuration "Release"
set_property(TARGET PTL::ptl-shared APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(PTL::ptl-shared PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libG4ptl.3.0.0.dylib"
  IMPORTED_SONAME_RELEASE "@rpath/libG4ptl.3.dylib"
  )

list(APPEND _cmake_import_check_targets PTL::ptl-shared )
list(APPEND _cmake_import_check_files_for_PTL::ptl-shared "${_IMPORT_PREFIX}/lib/libG4ptl.3.0.0.dylib" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
