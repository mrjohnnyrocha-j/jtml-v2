
// Generated from JTMLElement.g4 by ANTLR 4.13.0

#pragma once


#include "antlr4-runtime.h"
#include "JTMLElementParser.h"


/**
 * This interface defines an abstract listener for a parse tree produced by JTMLElementParser.
 */
class  JTMLElementListener : public antlr4::tree::ParseTreeListener {
public:

  virtual void enterJtmlElement(JTMLElementParser::JtmlElementContext *ctx) = 0;
  virtual void exitJtmlElement(JTMLElementParser::JtmlElementContext *ctx) = 0;

  virtual void enterAttributes(JTMLElementParser::AttributesContext *ctx) = 0;
  virtual void exitAttributes(JTMLElementParser::AttributesContext *ctx) = 0;

  virtual void enterContent(JTMLElementParser::ContentContext *ctx) = 0;
  virtual void exitContent(JTMLElementParser::ContentContext *ctx) = 0;

  virtual void enterStatement(JTMLElementParser::StatementContext *ctx) = 0;
  virtual void exitStatement(JTMLElementParser::StatementContext *ctx) = 0;

  virtual void enterShowStatement(JTMLElementParser::ShowStatementContext *ctx) = 0;
  virtual void exitShowStatement(JTMLElementParser::ShowStatementContext *ctx) = 0;

  virtual void enterDefineStatement(JTMLElementParser::DefineStatementContext *ctx) = 0;
  virtual void exitDefineStatement(JTMLElementParser::DefineStatementContext *ctx) = 0;

  virtual void enterExpression(JTMLElementParser::ExpressionContext *ctx) = 0;
  virtual void exitExpression(JTMLElementParser::ExpressionContext *ctx) = 0;


};

