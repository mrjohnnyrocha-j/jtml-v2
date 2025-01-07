cmake_minimum_required(VERSION 3.14)
project(jtml_elements LANGUAGES CXX)

# Set C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Include FetchContent module
include(FetchContent)

# Fetch pybind11
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.13.6  # Specify the desired version
)
FetchContent_MakeAvailable(pybind11)

# Build your python module named "jtml_engine"
add_library(jtml_engine MODULE
    jtml_bindings.cpp      # The Pybind11 file
    # Add any additional .cpp files here if necessary
)

# Link to pybind11
target_link_libraries(jtml_engine PRIVATE pybind11::module)

# Link to httplib.h
include_directories(/usr/local/include)

# Set appropriate properties based on the platform
set_target_properties(jtml_engine PROPERTIES PREFIX "")
if(WIN32)
    set_target_properties(jtml_engine PROPERTIES SUFFIX ".pyd")
elseif(APPLE)
    set_target_properties(jtml_engine PROPERTIES SUFFIX ".so")
else()
    set_target_properties(jtml_engine PROPERTIES SUFFIX ".so")
endif()

# CLI-oriented main
add_executable(jtml
    main.cpp
    jtml_ast.cpp
    jtml_lexer.cpp
    jtml_parser.cpp
    jtml_interpreter.cpp
    jtml_transpiler.cpp
)


# Test-oriented main
add_executable(jtml_tests
    main_tests.cpp
    jtml_ast.cpp
    jtml_lexer.cpp
    jtml_parser.cpp
    jtml_interpreter.cpp
    jtml_transpiler.cpp
)

