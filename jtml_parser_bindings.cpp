// jtml_parser_bindings.cpp
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "JTMLVisitor.h"
#include "JTMLElementParser/JTMLElementParserBaseVisitor.h"
#include "antlr4-runtime.h"
#include <memory>
#include <stdexcept>

namespace py = pybind11;

class ParserWrapper {
public:
    std::shared_ptr<ASTNode> parse(const std::string& input) {
        antlr4::ANTLRInputStream stream(input);
        JTMLElementLexer lexer(&stream);
        antlr4::CommonTokenStream tokens(&lexer);
        JTMLElementParser parser(&tokens);
        
        try {
            auto tree = parser.jtmlElement();
            JTMLVisitor visitor;
            auto result = visitor.visit(tree);
            return result.as<std::shared_ptr<ASTNode>>();
        } catch (const std::exception& e) {
            throw std::runtime_error(e.what());
        }
    }
};

PYBIND11_MODULE(jtmlparser, m) {
    py::class_<ParserWrapper>(m, "ParserWrapper")
        .def(py::init<>())
        .def("parse", &ParserWrapper::parse, "Parse a JTML element and return the AST node");
    
    // Expose ASTNode and derived classes
    py::class_<ASTNode, std::shared_ptr<ASTNode>>(m, "ASTNode")
        .def("to_dict", &ASTNode::to_dict);
    
    // Similarly, expose other AST node classes if needed
}
