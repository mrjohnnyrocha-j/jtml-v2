// JTMLVisitor.cpp
#include "JTMLVisitor.h"
#include <string>

antlrcpp::Any JTMLVisitor::visitJtmlElement(JTMLElementParser::JtmlElementContext *ctx) {
    std::string tagName = ctx->IDENTIFIER(0)->getText();
    std::map<std::string, std::string> attributes;
    if (ctx->attributes()) {
        for (auto attrCtx : ctx->attributes()->attribute()) {
            std::string key = attrCtx->IDENTIFIER()->getText();
            std::string value = attrCtx->STRING_LITERAL()->getText();
            // Remove surrounding quotes
            value = value.substr(1, value.length() - 2);
            attributes[key] = value;
        }
    }

    std::vector<std::shared_ptr<ASTNode>> content;
    if (ctx->content()) {
        for (auto stmtCtx : ctx->content()->statement()) {
            auto stmt = visit(stmtCtx);
            if (stmt.is<std::shared_ptr<ASTNode>>()) {
                content.push_back(stmt.as<std::shared_ptr<ASTNode>>());
            }
        }
    }

    return std::make_shared<JTMLElementNode>(tagName, attributes, content);
}

antlrcpp::Any JTMLVisitor::visitShowStatement(JTMLElementParser::ShowStatementContext *ctx) {
    std::string message = ctx->STRING_LITERAL()->getText();
    message = message.substr(1, message.length() - 2); // Remove quotes
    return std::make_shared<ShowStatementNode>(message);
}

antlrcpp::Any JTMLVisitor::visitDefineStatement(JTMLElementParser::DefineStatementContext *ctx) {
    std::string varName = ctx->IDENTIFIER()->getText();
    std::string expr = ctx->expression()->getText();
    return std::make_shared<VariableDeclarationNode>(varName, "", expr);
}

// ... implement other visit methods similarly
