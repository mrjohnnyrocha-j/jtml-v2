#pragma once

#include "jtml_ast.cpp"
#include "jtml_lexer.cpp"
#include "jtml_parser.cpp"
#include <iostream>
#include <unordered_map>

/**
 * A simple tree-walk interpreter for jtml:
 *  - Maintains a symbol table for 'define'
 *  - "show" prints the message
 *  - Recursively interprets nested jtmlElements
 * 
 * Web-centric attributes (style, event handlers) are not heavily used here.
 * The main purpose is server-side usage or debugging.
 */
class Interpreter {
public:
    Interpreter() = default;

    void interpret(const JtmlElementNode& root) {
        interpretElement(root);
    }

    void interpret(const std::string& code) {
        try {
            Lexer lexer(code);
            auto tokens = lexer.tokenize();

            Parser parser(std::move(tokens));
            std::unique_ptr<JtmlElementNode> root = parser.parseJtmlElement();

            interpret(*root);
        }
        catch (const std::exception& e) {
            std::cerr << "Interpretation error: " << e.what() << "\n";
        }
    }

private:
    std::unordered_map<std::string, std::string> m_symbols; // symbol table

    void interpretNode(const ASTNode& node) {
        switch (node.getType()) {
            case ASTNodeType::JtmlElement:
                interpretElement(static_cast<const JtmlElementNode&>(node));
                break;
            case ASTNodeType::ShowStatement:
                interpretShow(static_cast<const ShowStatementNode&>(node));
                break;
            case ASTNodeType::DefineStatement:
                interpretDefine(static_cast<const DefineStatementNode&>(node));
                break;
        }
    }

    void interpretElement(const JtmlElementNode& elem) {
        std::cout << "Entering element <" << elem.tagName << ">\n";
        for (auto& attr : elem.attributes) {
            std::cout << "  [Attribute] " << attr.key << " = " << attr.value << "\n";
        }
        // Interpret child statements/elements
        for (auto& child : elem.content) {
            interpretNode(*child);
        }
        std::cout << "Exiting element <" << elem.tagName << ">\n";
    }

    void interpretShow(const ShowStatementNode& showStmt) {
        std::cout << "[SHOW] " << showStmt.message << "\n";
    }

    void interpretDefine(const DefineStatementNode& defStmt) {
        // If the expression is a known symbol, expand it
        std::string value = defStmt.expression;
        if (m_symbols.find(value) != m_symbols.end()) {
            value = m_symbols[value];
        }
        m_symbols[defStmt.identifier] = value;
        std::cout << "[DEFINE] " << defStmt.identifier << " = " << value << "\n";
    }
};
