# -------------------------------------------------------------------------------------- #
# package initialization
#

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was PTLConfig.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

cmake_minimum_required(VERSION 3.8...3.27)

# -------------------------------------------------------------------------------------- #
# basic paths
#
set_and_check(PTL_INCLUDE_DIR "${PACKAGE_PREFIX_DIR}/include/Geant4")
set_and_check(PTL_LIB_DIR "${PACKAGE_PREFIX_DIR}/lib")

# -------------------------------------------------------------------------------------- #
# available components
#
set(PTL_shared_FOUND ON)
set(PTL_static_FOUND OFF)
set(PTL_TBB_FOUND OFF)

# Early check so later setup doesn't need to check REQUIRED status
check_required_components(PTL)

# -------------------------------------------------------------------------------------- #
# refind needed dependencies/targets
#
include(CMakeFindDependencyMacro)

if(NOT Threads_FOUND)
    set(CMAKE_THREAD_PREFER_PTHREAD ON)
    set(THREADS_PREFER_PTHREAD_FLAG ON)
    find_dependency(Threads REQUIRED)
endif()

if(NOT TBB_FOUND AND PTL_TBB_FOUND)
    list(INSERT CMAKE_MODULE_PATH 0 "${PACKAGE_PREFIX_DIR}/lib/cmake/Geant4/PTL/Modules")
    find_dependency(TBB  REQUIRED)
    list(REMOVE_AT CMAKE_MODULE_PATH 0)
endif()

# -------------------------------------------------------------------------------------- #
# Include our targets file(s)
#
include("${CMAKE_CURRENT_LIST_DIR}/PTLTargets.cmake")

# Set the default component based on what's available
if(PTL_shared_FOUND)
    set(_ptl_preferred_link "shared")
else()
    set(_ptl_preferred_link "static")
endif()

# Override if user has specified "static" alone as a component. Earlier check handles case
# that components are REQUIRED. Only change preferred link only changed if available to
# cover OPTIONAL case
if(("static" IN_LIST PTL_FIND_COMPONENTS) AND NOT ("shared" IN_LIST PTL_FIND_COMPONENTS))
    if(PTL_static_FOUND)
        set(_ptl_preferred_link "static")
    endif()
endif()

# -------------------------------------------------------------------------------------- #
# Set old style variables for include/linking
#
set(PTL_INCLUDE_DIRS ${PTL_INCLUDE_DIR})
set(PTL_LIBRARIES PTL::ptl-${_ptl_preferred_link})

# -------------------------------------------------------------------------------------- #
# Create "transparent" link target that interfaces to shared/static on basis of
# availability or requested linking option
#
if(NOT TARGET PTL::ptl)
    add_library(PTL::ptl INTERFACE IMPORTED)
    target_link_libraries(PTL::ptl INTERFACE ${PTL_LIBRARIES})
    # Needed to distinguish DLL/Lib, but symbol never used in code. Should also be a
    # public symbol of ptl-static
    if(WIN32)
        target_compile_definitions(PTL::ptl INTERFACE _PTL_ARCHIVE)
    endif()
endif()
