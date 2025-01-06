#pragma once

#include <string>
#include <vector>
#include <memory>

// Identify node types in the AST
enum class ASTNodeType {
    JtmlElement,
    ShowStatement,
    DefineStatement
};

// Holds a key:value attribute (e.g. style, onclick, class, etc.)
struct JtmlAttribute {
    std::string key;
    std::string value;
};

// Base class for all AST nodes
struct ASTNode {
    virtual ~ASTNode() = default;
    virtual ASTNodeType getType() const = 0;
};

// ------------------- ShowStatementNode -------------------
struct ShowStatementNode : public ASTNode {
    std::string message;  // The text to display

    ASTNodeType getType() const override {
        return ASTNodeType::ShowStatement;
    }
};

// ------------------- DefineStatementNode -------------------
struct DefineStatementNode : public ASTNode {
    std::string identifier;
    std::string expression; // could be identifier or string literal

    ASTNodeType getType() const override {
        return ASTNodeType::DefineStatement;
    }
};

// ------------------- JtmlElementNode -------------------
struct JtmlElementNode : public ASTNode {
    std::string tagName;                          // e.g. "div", "h1", or custom
    std::vector<JtmlAttribute> attributes;        // e.g. [("style", "color:red;"), ("onclick", "alert('hi')")]
    std::vector<std::unique_ptr<ASTNode>> content; // child nodes: show/define statements or nested elements

    ASTNodeType getType() const override {
        return ASTNodeType::JtmlElement;
    }
};
