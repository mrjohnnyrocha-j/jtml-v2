#pragma once

#include <string>
#include <vector>
#include <memory>

/**
 * Identify node types in the AST. 
 *  - JtmlElement is the markup-like node (#div, #p, etc.).
 *  - ShowStatement, DefineStatement, DeriveStatement, etc. are statements.
 *  - We also have control-flow (If, While, For) and error-handling (TryCatchFinally).
 */
enum class ASTNodeType {
    // Markup / structural
    JtmlElement,

    // Simple statements
    ShowStatement,
    DefineStatement,
    DeriveStatement,
    UnbindStatement,
    StoreStatement,
    ExpressionStatement,
    ReturnStatement,
    ThrowStatement,

    // Control flow
    IfStatement,
    WhileStatement,
    ForStatement,
    TryCatchFinally
    // etc. if needed
};

// Holds a key:value attribute (e.g. style, class, onclick, etc.)
struct JtmlAttribute {
    std::string key;
    std::string value;
};

// ------------------- Base AST Node -------------------
struct ASTNode {
    virtual ~ASTNode() = default;
    virtual ASTNodeType getType() const = 0;
};

// ========================================================================
// 1) Markup Node
// ========================================================================
struct JtmlElementNode : public ASTNode {
    std::string tagName;                           
    std::vector<JtmlAttribute> attributes;          
    std::vector<std::unique_ptr<ASTNode>> content;  // child nodes: statements or nested elements

    ASTNodeType getType() const override {
        return ASTNodeType::JtmlElement;
    }
};

// ========================================================================
// 2) Simple Statement Nodes
// ========================================================================

// -- ShowStatementNode --
struct ShowStatementNode : public ASTNode {
    std::string message;  // The text to display or a partial expression

    ASTNodeType getType() const override {
        return ASTNodeType::ShowStatement;
    }
};

// -- DefineStatementNode --
struct DefineStatementNode : public ASTNode {
    std::string identifier;
    std::string expression; // could be identifier or literal or bigger expression

    ASTNodeType getType() const override {
        return ASTNodeType::DefineStatement;
    }
};

// -- DeriveStatementNode (reactive variables) --
struct DeriveStatementNode : public ASTNode {
    std::string identifier;
    std::string declaredType; // optional, might be empty
    std::string expression;   // e.g. "a + b"

    ASTNodeType getType() const override {
        return ASTNodeType::DeriveStatement;
    }
};

// -- UnbindStatementNode --
struct UnbindStatementNode : public ASTNode {
    std::string identifier; // the variable to freeze/unbind from reactivity

    ASTNodeType getType() const override {
        return ASTNodeType::UnbindStatement;
    }
};

// -- StoreStatementNode (move variable to a different scope) --
struct StoreStatementNode : public ASTNode {
    std::string targetScope; // e.g. "main" or a function/class name
    std::string variableName; // the variable being stored

    ASTNodeType getType() const override {
        return ASTNodeType::StoreStatement;
    }
};

// -- ExpressionStatementNode --
/**
 * e.g. "x++", or "someFunc(42)" as a standalone statement
 * This can hold a more complex expression structure if you have an Expression AST.
 * For now, we might store it as a string or separate expression node pointer.
 */
struct ExpressionStatementNode : public ASTNode {
    std::string expression;

    ASTNodeType getType() const override {
        return ASTNodeType::ExpressionStatement;
    }
};

// -- ReturnStatementNode --
struct ReturnStatementNode : public ASTNode {
    std::string expression; // optional expression

    ASTNodeType getType() const override {
        return ASTNodeType::ReturnStatement;
    }
};

// -- ThrowStatementNode --
struct ThrowStatementNode : public ASTNode {
    std::string expression; // the error or exception message

    ASTNodeType getType() const override {
        return ASTNodeType::ThrowStatement;
    }
};

// ========================================================================
// 3) Control-Flow Statements
// ========================================================================

// -- IfStatementNode --
/**
 * if (condition) BLOCK else BLOCK
 * We'll store the condition as a string or an expression pointer, 
 * plus two lists of statements for then-block and else-block.
 */
struct IfStatementNode : public ASTNode {
    std::string condition; // naive approach, or a separate expression node
    std::vector<std::unique_ptr<ASTNode>> thenStatements;
    std::vector<std::unique_ptr<ASTNode>> elseStatements; // empty if no else

    ASTNodeType getType() const override {
        return ASTNodeType::IfStatement;
    }
};

// -- WhileStatementNode --
struct WhileStatementNode : public ASTNode {
    std::string condition;
    std::vector<std::unique_ptr<ASTNode>> body; // statements

    ASTNodeType getType() const override {
        return ASTNodeType::WhileStatement;
    }
};

// -- ForStatementNode --
/**
 * for (iterator in expression) BLOCK
 * or for( i in 0..10 ) if you do range
 * We'll store 'iteratorName' plus the expression describing the list/range, 
 * plus the body statements
 */
struct ForStatementNode : public ASTNode {
    std::string iteratorName;
    std::string iterableExpression;
    std::vector<std::unique_ptr<ASTNode>> body;

    ASTNodeType getType() const override {
        return ASTNodeType::ForStatement;
    }
};

// -- TryCatchFinallyNode --
/**
 * try BLOCK
 * catch (errVar) BLOCK
 * finally BLOCK
 * Each block is a vector of statements, the catch variable is optional
 */
struct TryCatchFinallyNode : public ASTNode {
    std::vector<std::unique_ptr<ASTNode>> tryBlock;
    bool hasCatch = false;
    std::string catchIdentifier; // e.g. "e" or "error"
    std::vector<std::unique_ptr<ASTNode>> catchBlock;
    bool hasFinally = false;
    std::vector<std::unique_ptr<ASTNode>> finallyBlock;

    ASTNodeType getType() const override {
        return ASTNodeType::TryCatchFinally;
    }
};

