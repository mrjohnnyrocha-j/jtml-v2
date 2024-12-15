
// Generated from JTMLElement.g4 by ANTLR 4.13.0

#pragma once


#include "antlr4-runtime.h"
#include "JTMLElementVisitor.h"


/**
 * This class provides an empty implementation of JTMLElementVisitor, which can be
 * extended to create a visitor which only needs to handle a subset of the available methods.
 */
class  JTMLElementBaseVisitor : public JTMLElementVisitor {
public:

  virtual std::any visitJtmlElement(JTMLElementParser::JtmlElementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitAttributes(JTMLElementParser::AttributesContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitContent(JTMLElementParser::ContentContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitStatement(JTMLElementParser::StatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitShowStatement(JTMLElementParser::ShowStatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitDefineStatement(JTMLElementParser::DefineStatementContext *ctx) override {
    return visitChildren(ctx);
  }

  virtual std::any visitExpression(JTMLElementParser::ExpressionContext *ctx) override {
    return visitChildren(ctx);
  }


};

