// jtml_bindings.cpp
#include <pybind11/pybind11.h>
#include "jtml_parser.cpp"       
#include "jtml_interpreter.cpp"  

namespace py = pybind11;

void interpret_string(const std::string& code) {
    Interpreter interp;
    interp.interpret(code);
}

PYBIND11_MODULE(jtml_engine, m) {
    m.doc() = "JTML engine Python bindings";
    m.def("interpret_string", &interpret_string, "Interpret a jtml snippet");
}
