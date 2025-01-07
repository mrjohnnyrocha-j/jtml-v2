#pragma once

#include "jtml_ast.cpp"
#include <sstream>
#include <string>
#include <unordered_map>

/**
 * JtmlTranspiler:
 *  - Takes a JtmlElementNode AST
 *  - Produces an HTML string with variable substitution
 * 
 * Enhancements:
 *  - Supports replacing variables in attribute values
 */
class JtmlTranspiler {
public:
    // Transpile an entire JtmlElementNode to an HTML string
    // Pass the symbol table for variable substitution
    std::string transpileHTML(const JtmlElementNode& root) {
        std::unordered_map<std::string, std::string> emptySymbols;
        return transpileHTML(root, emptySymbols);
    }

    // Overload #2: with symbol table
    std::string transpileHTML(
        const JtmlElementNode& root,
        const std::unordered_map<std::string, std::string>& symbols
    ) {
        std::ostringstream oss;
        transpileElement(root, oss, symbols);
        return oss.str();
    }

private:
    void transpileElement(const JtmlElementNode& elem, std::ostringstream& oss, const std::unordered_map<std::string, std::string>& symbols) {
        // 1) Open tag
        oss << "<" << mapTagName(elem.tagName);

        // 2) Attributes with variable substitution
        for (auto& attr : elem.attributes) {
            std::string value = substituteVariables(attr.value, symbols);
            oss << " " << attr.key << "=\""
                << escapeForHTML(value) << "\"";
        }
        oss << ">";

        // 3) Content
        for (auto& child : elem.content) {
            switch (child->getType()) {
                case ASTNodeType::JtmlElement: {
                    auto& cElem = static_cast<const JtmlElementNode&>(*child);
                    transpileElement(cElem, oss, symbols);
                    break;
                }
                case ASTNodeType::ShowStatement: {
                    auto& showStmt = static_cast<const ShowStatementNode&>(*child);
                    std::string message = substituteVariables(showStmt.message, symbols);
                    oss << escapeForHTML(message);
                    break;
                }
                case ASTNodeType::DefineStatement: {
                    auto& defStmt = static_cast<const DefineStatementNode&>(*child);
                    // Optionally, generate JS variables or skip
                    // For now, skip or comment
                    oss << "<!-- define " << defStmt.identifier 
                        << " = " << defStmt.expression << " -->";
                    break;
                }
            }
        }

        // 4) Close tag
        oss << "</" << mapTagName(elem.tagName) << ">";
    }

    // Substitute variables in the form of identifiers within the string
    std::string substituteVariables(const std::string& input, const std::unordered_map<std::string, std::string>& symbols) {
        std::string output;
        size_t pos = 0;
        while (pos < input.size()) {
            if (input[pos] == '{' && pos + 1 < input.size()) { // Assuming variables are wrapped like {var}
                size_t end = input.find('}', pos);
                if (end != std::string::npos) {
                    std::string varName = input.substr(pos + 1, end - pos - 1);
                    auto it = symbols.find(varName);
                    if (it != symbols.end()) {
                        output += it->second;
                    } else {
                        // If variable not found, keep it as is or replace with empty string
                        output += "";
                    }
                    pos = end + 1;
                } else {
                    // No closing brace found, treat as normal character
                    output += input[pos];
                    pos++;
                }
            } else {
                output += input[pos];
                pos++;
            }
        }
        return output;
    }

    // Map tag names if necessary
    std::string mapTagName(const std::string& tag) const {
        return tag;
    }

    // Minimal HTML escaping
    std::string escapeForHTML(const std::string& raw) const {
        std::string out;
        out.reserve(raw.size());
        for (char c : raw) {
            switch (c) {
                case '&':  out += "&amp;";  break;
                case '<':  out += "&lt;";   break;
                case '>':  out += "&gt;";   break;
                case '"':  out += "&quot;"; break;
                default:   out.push_back(c); break;
            }
        }
        return out;
    }
};
