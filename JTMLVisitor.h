// JTMLVisitor.h
#pragma once
#include "JTMLElementParserBaseVisitor.h"
#include "ASTNodes.h" // Define your AST node structures

class JTMLVisitor : public JTMLElementParserBaseVisitor {
public:
    virtual antlrcpp::Any visitJtmlElement(JTMLElementParser::JtmlElementContext *ctx) override;
    virtual antlrcpp::Any visitShowStatement(JTMLElementParser::ShowStatementContext *ctx) override;
    virtual antlrcpp::Any visitDefineStatement(JTMLElementParser::DefineStatementContext *ctx) override;
    // ... implement other visit methods as needed
};
