
// Generated from JTMLElement.g4 by ANTLR 4.13.0

#pragma once


#include "antlr4-runtime.h"
#include "JTMLElementParser.h"



/**
 * This class defines an abstract visitor for a parse tree
 * produced by JTMLElementParser.
 */
class  JTMLElementVisitor : public antlr4::tree::AbstractParseTreeVisitor {
public:

  /**
   * Visit parse trees produced by JTMLElementParser.
   */
    virtual std::any visitJtmlElement(JTMLElementParser::JtmlElementContext *context) = 0;

    virtual std::any visitAttributes(JTMLElementParser::AttributesContext *context) = 0;

    virtual std::any visitContent(JTMLElementParser::ContentContext *context) = 0;

    virtual std::any visitStatement(JTMLElementParser::StatementContext *context) = 0;

    virtual std::any visitShowStatement(JTMLElementParser::ShowStatementContext *context) = 0;

    virtual std::any visitDefineStatement(JTMLElementParser::DefineStatementContext *context) = 0;

    virtual std::any visitExpression(JTMLElementParser::ExpressionContext *context) = 0;


};

