cmake_minimum_required(VERSION 3.16...3.27)
project(paulsim LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Geant4 REQUIRED ui_all)

# This bundled Geant4 build records the SDK used when it was built in the
# public include path of its system Expat dependency.  On newer Xcode/CLT
# versions that makes libc++ combine headers from two SDK releases, which
# prevents even standard headers such as <cstring> from compiling.  This
# application does not include Expat headers directly, so do not propagate
# Geant4's stale SDK include path to this target.
if(TARGET EXPAT::EXPAT)
    set_property(TARGET EXPAT::EXPAT PROPERTY INTERFACE_INCLUDE_DIRECTORIES "")
endif()

include(${Geant4_USE_FILE})
include_directories(${PROJECT_SOURCE_DIR}/include ${Geant4_INCLUDE_DIRS})

file(GLOB SOURCES ${PROJECT_SOURCE_DIR}/src/*.cc)
add_executable(paulsim paulsim.cc ${SOURCES})
target_link_libraries(paulsim ${Geant4_LIBRARIES})

install(TARGETS paulsim DESTINATION bin)
