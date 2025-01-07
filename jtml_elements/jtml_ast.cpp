#pragma once

#include <string>
#include <vector>
#include <memory>

/**
 * Identify node types for statements/markup in the AST. 
 *  - JtmlElement is the markup-like node (#div, #p, etc.).
 *  - ShowStatement, DefineStatement, DeriveStatement, etc. are statements.
 *  - We also have control-flow (If, While, For) and error-handling (TryExceptThen).
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
    TryExceptThen

    // etc. if needed
};

/**
 * For expression parsing, we define a separate ExpressionStatementNode hierarchy 
 * (Binary, Unary, Variable, etc.). This is not part of ASTNodeType 
 * because it's only used inside statements or expressions, 
 * not top-level statements themselves.
 */
enum class ExpressionStatementNodeType {
    Binary,
    Unary,
    Variable,
    StringLiteral,
    NumberLiteral
    // ... you could add BooleanLiteral, etc.
};

// ------------------- Expression Nodes -------------------
struct ExpressionStatementNode {
    virtual ~ExpressionStatementNode() = default;
    virtual ExpressionStatementNodeType getExprType() const = 0;
};

/** 
 * A binary operation (left op right), 
 * e.g. (a + b), (x * 2), (x == y).
 */
struct BinaryExpressionStatementNode : public ExpressionStatementNode {
    // The operator token (PLUS, MINUS, MULTIPLY, DIVIDE, EQ, NEQ, etc.)
    // You can store e.g. Token op if you want direct token reference,
    // or a simple enum describing the operator.
    // We'll store a text-based operator for simplicity.
    std::string op; 

    std::unique_ptr<ExpressionStatementNode> left;
    std::unique_ptr<ExpressionStatementNode> right;

    BinaryExpressionStatementNode(std::string operatorText,
                   std::unique_ptr<ExpressionStatementNode> l,
                   std::unique_ptr<ExpressionStatementNode> r)
        : op(std::move(operatorText)), left(std::move(l)), right(std::move(r)) {}

    ExpressionStatementNodeType getExprType() const override {
        return ExpressionStatementNodeType::Binary;
    }
};

/**
 * A unary operation, e.g. -x, !x
 */
struct UnaryExpressionStatementNode : public ExpressionStatementNode {
    std::string op;  // e.g. "-", "!"

    std::unique_ptr<ExpressionStatementNode> right;

    UnaryExpressionStatementNode(std::string operatorText, std::unique_ptr<ExpressionStatementNode> r)
        : op(std::move(operatorText)), right(std::move(r)) {}

    ExpressionStatementNodeType getExprType() const override {
        return ExpressionStatementNodeType::Unary;
    }
};

/**
 * A variable reference, e.g. "myVar".
 */
struct VariableExpressionStatementNode : public ExpressionStatementNode {
    std::string name;

    VariableExpressionStatementNode(std::string varName)
        : name(std::move(varName)) {}

    ExpressionStatementNodeType getExprType() const override {
        return ExpressionStatementNodeType::Variable;
    }
};

/**
 * A string literal, e.g. "Hello world".
 */
struct StringLiteralExpressionStatementNode : public ExpressionStatementNode {
    std::string value;

    explicit StringLiteralExpressionStatementNode(std::string val)
        : value(std::move(val)) {}

    ExpressionStatementNodeType getExprType() const override {
        return ExpressionStatementNodeType::StringLiteral;
    }
};

/**
 * A numeric literal, e.g. 42, 3.14
 * If you prefer, store them as double or string.
 */
struct NumberLiteralExpressionStatementNode : public ExpressionStatementNode {
    std::string value; // or double numericValue

    explicit NumberLiteralExpressionStatementNode(std::string val)
        : value(std::move(val)) {}

    ExpressionStatementNodeType getExprType() const override {
        return ExpressionStatementNodeType::NumberLiteral;
    }
};

/** 
 * For booleans or other literal types, you can add more nodes 
 * (BoolLiteralExpressionStatementNode, etc.) if needed.
 */

// ----------------------------------------------------------------
//  Now the main ASTNode hierarchy for statements and markup
// ----------------------------------------------------------------

// Holds a key:value attribute (e.g. style, class, onclick, etc.)
struct JtmlAttribute {
    std::string key;
    std::string value;
};

// ------------------- Base AST Node (Statement-Level) -------------------
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
    // Before we only had "message" as a string,
    // now you can consider using an expression node if you want advanced logic
    // but let's keep it as a string for simple usage:
    std::string message;

    ASTNodeType getType() const override {
        return ASTNodeType::ShowStatement;
    }
};

// -- DefineStatementNode --
struct DefineStatementNode : public ASTNode {
    std::string identifier;

    // Replaces old `std::string expression` with a real expression node:
    std::unique_ptr<ExpressionStatementNode> expression;

    ASTNodeType getType() const override {
        return ASTNodeType::DefineStatement;
    }
};

// -- DeriveStatementNode (reactive variables) --
struct DeriveStatementNode : public ASTNode {
    std::string identifier;
    std::string declaredType; // optional, might be empty

    // a real expression node for "a + b"
    std::unique_ptr<ExpressionStatementNode> expression; 

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
    std::string targetScope;  // e.g. "main" or a function/class name
    std::string variableName; // the variable being stored

    ASTNodeType getType() const override {
        return ASTNodeType::StoreStatement;
    }
};


// -- ReturnStatementNode --
struct ReturnStatementNode : public ASTNode {
    // optional expression
    std::unique_ptr<ExpressionStatementNode> expression; 

    ASTNodeType getType() const override {
        return ASTNodeType::ReturnStatement;
    }
};

// -- ThrowStatementNode --
struct ThrowStatementNode : public ASTNode {
    // an expression representing the error or exception data
    std::unique_ptr<ExpressionStatementNode> expression;

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
 * We'll store the condition as an expression node,
 * plus two lists of statements for then-block and else-block.
 */
struct IfStatementNode : public ASTNode {
    std::unique_ptr<ExpressionStatementNode> condition; 
    std::vector<std::unique_ptr<ASTNode>> thenStatements;
    std::vector<std::unique_ptr<ASTNode>> elseStatements; // empty if no else

    ASTNodeType getType() const override {
        return ASTNodeType::IfStatement;
    }
};

// -- WhileStatementNode --
struct WhileStatementNode : public ASTNode {
    std::unique_ptr<ExpressionStatementNode> condition;
    std::vector<std::unique_ptr<ASTNode>> body; // statements

    ASTNodeType getType() const override {
        return ASTNodeType::WhileStatement;
    }
};

// -- ForStatementNode --
/**
 * for (iterator in expression) BLOCK
 * We'll store 'iteratorName' plus expression describing the list/range, 
 * plus the body statements
 */
struct ForStatementNode : public ASTNode {
    std::string iteratorName;
    std::unique_ptr<ExpressionStatementNode> iterableExpression;
    std::vector<std::unique_ptr<ASTNode>> body;

    ASTNodeType getType() const override {
        return ASTNodeType::ForStatement;
    }
};

// -- TryExceptThenNode --
/**
 * try BLOCK
 * except (errVar) BLOCK
 * then BLOCK
 *
 * Each block is a vector of statements, the catch variable is optional
 * 'hasCatch' means we have an except block, 'hasFinally' means we have a 'then' block.
 *
 * If you want a typical "catch/finally", rename them accordingly. 
 * The grammar can vary from your original references, but here's a structure:
 */
struct TryExceptThenNode : public ASTNode {
    std::vector<std::unique_ptr<ASTNode>> tryBlock;

    bool hasCatch = false;
    std::string catchIdentifier; // e.g. "err"
    std::vector<std::unique_ptr<ASTNode>> catchBlock;

    bool hasFinally = false;     // or hasThen if you prefer
    std::vector<std::unique_ptr<ASTNode>> finallyBlock;

    ASTNodeType getType() const override {
        return ASTNodeType::TryExceptThen;
    }
};

