cmake_minimum_required(VERSION 3.10)
project(jtml_elements LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# If you rely on httplib:
include_directories("/opt/homebrew/opt/cpp-httplib/include")

# 1) Find pybind11
find_package(pybind11 REQUIRED)

# 2) Build your python module named "jtml_engine"
add_library(jtml_engine MODULE
    jtml_bindings.cpp      # The Pybind11 file
    # plus any .cpp that implement the rest:
    # If your code is purely in .hpp, you can skip .cpp references, 
    # or create minimal .cpp files for them
)

# 3) Link to pybind11
target_link_libraries(jtml_engine PRIVATE pybind11::module)

# 4) Avoid "lib" prefix and ensure .so is the extension
#    (Typically, 'MODULE' sets .so on macOS/Linux, .pyd on Windows)
set_target_properties(jtml_engine PROPERTIES PREFIX "")
# Optionally: set_target_properties(jtml_engine PROPERTIES SUFFIX ".so")

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
