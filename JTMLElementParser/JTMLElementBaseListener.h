
// Generated from JTMLElement.g4 by ANTLR 4.13.0

#pragma once


#include "antlr4-runtime.h"
#include "JTMLElementListener.h"


/**
 * This class provides an empty implementation of JTMLElementListener,
 * which can be extended to create a listener which only needs to handle a subset
 * of the available methods.
 */
class  JTMLElementBaseListener : public JTMLElementListener {
public:

  virtual void enterJtmlElement(JTMLElementParser::JtmlElementContext * /*ctx*/) override { }
  virtual void exitJtmlElement(JTMLElementParser::JtmlElementContext * /*ctx*/) override { }

  virtual void enterAttributes(JTMLElementParser::AttributesContext * /*ctx*/) override { }
  virtual void exitAttributes(JTMLElementParser::AttributesContext * /*ctx*/) override { }

  virtual void enterContent(JTMLElementParser::ContentContext * /*ctx*/) override { }
  virtual void exitContent(JTMLElementParser::ContentContext * /*ctx*/) override { }

  virtual void enterStatement(JTMLElementParser::StatementContext * /*ctx*/) override { }
  virtual void exitStatement(JTMLElementParser::StatementContext * /*ctx*/) override { }

  virtual void enterShowStatement(JTMLElementParser::ShowStatementContext * /*ctx*/) override { }
  virtual void exitShowStatement(JTMLElementParser::ShowStatementContext * /*ctx*/) override { }

  virtual void enterDefineStatement(JTMLElementParser::DefineStatementContext * /*ctx*/) override { }
  virtual void exitDefineStatement(JTMLElementParser::DefineStatementContext * /*ctx*/) override { }

  virtual void enterExpression(JTMLElementParser::ExpressionContext * /*ctx*/) override { }
  virtual void exitExpression(JTMLElementParser::ExpressionContext * /*ctx*/) override { }


  virtual void enterEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void exitEveryRule(antlr4::ParserRuleContext * /*ctx*/) override { }
  virtual void visitTerminal(antlr4::tree::TerminalNode * /*node*/) override { }
  virtual void visitErrorNode(antlr4::tree::ErrorNode * /*node*/) override { }

};

