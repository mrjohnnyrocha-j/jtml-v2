
// Generated from JTMLElement.g4 by ANTLR 4.13.0


#include "JTMLElementListener.h"
#include "JTMLElementVisitor.h"

#include "JTMLElementParser.h"


using namespace antlrcpp;

using namespace antlr4;

namespace {

struct JTMLElementParserStaticData final {
  JTMLElementParserStaticData(std::vector<std::string> ruleNames,
                        std::vector<std::string> literalNames,
                        std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  JTMLElementParserStaticData(const JTMLElementParserStaticData&) = delete;
  JTMLElementParserStaticData(JTMLElementParserStaticData&&) = delete;
  JTMLElementParserStaticData& operator=(const JTMLElementParserStaticData&) = delete;
  JTMLElementParserStaticData& operator=(JTMLElementParserStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag jtmlelementParserOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
JTMLElementParserStaticData *jtmlelementParserStaticData = nullptr;

void jtmlelementParserInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (jtmlelementParserStaticData != nullptr) {
    return;
  }
#else
  assert(jtmlelementParserStaticData == nullptr);
#endif
  auto staticData = std::make_unique<JTMLElementParserStaticData>(
    std::vector<std::string>{
      "jtmlElement", "attributes", "content", "statement", "showStatement", 
      "defineStatement", "expression"
    },
    std::vector<std::string>{
      "", "'#'", "':'", "','", "'\\\\'", "'='", "'+'", "'-'", "'show'", 
      "'define'"
    },
    std::vector<std::string>{
      "", "HASH", "COLON", "COMMA", "BACKSLASH", "EQUALS", "PLUS", "MINUS", 
      "SHOW", "DEFINE", "IDENTIFIER", "STRING_LITERAL", "NUMBER_LITERAL", 
      "WS"
    }
  );
  static const int32_t serializedATNSegment[] = {
  	4,1,13,78,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,6,1,0,
  	1,0,1,0,3,0,18,8,0,1,0,1,0,3,0,22,8,0,1,0,1,0,3,0,26,8,0,1,1,1,1,1,1,
  	1,1,1,1,1,1,1,1,5,1,35,8,1,10,1,12,1,38,9,1,1,2,1,2,5,2,42,8,2,10,2,12,
  	2,45,9,2,1,3,1,3,1,3,3,3,50,8,3,1,4,1,4,1,4,1,5,1,5,1,5,1,5,1,5,1,6,1,
  	6,1,6,1,6,1,6,3,6,65,8,6,1,6,1,6,1,6,1,6,1,6,1,6,5,6,73,8,6,10,6,12,6,
  	76,9,6,1,6,0,1,12,7,0,2,4,6,8,10,12,0,0,82,0,14,1,0,0,0,2,27,1,0,0,0,
  	4,39,1,0,0,0,6,49,1,0,0,0,8,51,1,0,0,0,10,54,1,0,0,0,12,64,1,0,0,0,14,
  	15,5,1,0,0,15,17,5,10,0,0,16,18,3,2,1,0,17,16,1,0,0,0,17,18,1,0,0,0,18,
  	19,1,0,0,0,19,21,5,4,0,0,20,22,3,4,2,0,21,20,1,0,0,0,21,22,1,0,0,0,22,
  	23,1,0,0,0,23,25,5,1,0,0,24,26,5,10,0,0,25,24,1,0,0,0,25,26,1,0,0,0,26,
  	1,1,0,0,0,27,28,5,10,0,0,28,29,5,2,0,0,29,36,5,11,0,0,30,31,5,3,0,0,31,
  	32,5,10,0,0,32,33,5,2,0,0,33,35,5,11,0,0,34,30,1,0,0,0,35,38,1,0,0,0,
  	36,34,1,0,0,0,36,37,1,0,0,0,37,3,1,0,0,0,38,36,1,0,0,0,39,43,3,6,3,0,
  	40,42,5,4,0,0,41,40,1,0,0,0,42,45,1,0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,
  	44,5,1,0,0,0,45,43,1,0,0,0,46,50,3,8,4,0,47,50,3,10,5,0,48,50,1,0,0,0,
  	49,46,1,0,0,0,49,47,1,0,0,0,49,48,1,0,0,0,50,7,1,0,0,0,51,52,5,8,0,0,
  	52,53,5,11,0,0,53,9,1,0,0,0,54,55,5,9,0,0,55,56,5,10,0,0,56,57,5,5,0,
  	0,57,58,3,12,6,0,58,11,1,0,0,0,59,60,6,6,-1,0,60,65,5,10,0,0,61,65,5,
  	12,0,0,62,65,5,11,0,0,63,65,1,0,0,0,64,59,1,0,0,0,64,61,1,0,0,0,64,62,
  	1,0,0,0,64,63,1,0,0,0,65,74,1,0,0,0,66,67,10,3,0,0,67,68,5,6,0,0,68,73,
  	3,12,6,4,69,70,10,2,0,0,70,71,5,7,0,0,71,73,3,12,6,3,72,66,1,0,0,0,72,
  	69,1,0,0,0,73,76,1,0,0,0,74,72,1,0,0,0,74,75,1,0,0,0,75,13,1,0,0,0,76,
  	74,1,0,0,0,9,17,21,25,36,43,49,64,72,74
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  jtmlelementParserStaticData = staticData.release();
}

}

JTMLElementParser::JTMLElementParser(TokenStream *input) : JTMLElementParser(input, antlr4::atn::ParserATNSimulatorOptions()) {}

JTMLElementParser::JTMLElementParser(TokenStream *input, const antlr4::atn::ParserATNSimulatorOptions &options) : Parser(input) {
  JTMLElementParser::initialize();
  _interpreter = new atn::ParserATNSimulator(this, *jtmlelementParserStaticData->atn, jtmlelementParserStaticData->decisionToDFA, jtmlelementParserStaticData->sharedContextCache, options);
}

JTMLElementParser::~JTMLElementParser() {
  delete _interpreter;
}

const atn::ATN& JTMLElementParser::getATN() const {
  return *jtmlelementParserStaticData->atn;
}

std::string JTMLElementParser::getGrammarFileName() const {
  return "JTMLElement.g4";
}

const std::vector<std::string>& JTMLElementParser::getRuleNames() const {
  return jtmlelementParserStaticData->ruleNames;
}

const dfa::Vocabulary& JTMLElementParser::getVocabulary() const {
  return jtmlelementParserStaticData->vocabulary;
}

antlr4::atn::SerializedATNView JTMLElementParser::getSerializedATN() const {
  return jtmlelementParserStaticData->serializedATN;
}


//----------------- JtmlElementContext ------------------------------------------------------------------

JTMLElementParser::JtmlElementContext::JtmlElementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JTMLElementParser::JtmlElementContext::HASH() {
  return getTokens(JTMLElementParser::HASH);
}

tree::TerminalNode* JTMLElementParser::JtmlElementContext::HASH(size_t i) {
  return getToken(JTMLElementParser::HASH, i);
}

std::vector<tree::TerminalNode *> JTMLElementParser::JtmlElementContext::IDENTIFIER() {
  return getTokens(JTMLElementParser::IDENTIFIER);
}

tree::TerminalNode* JTMLElementParser::JtmlElementContext::IDENTIFIER(size_t i) {
  return getToken(JTMLElementParser::IDENTIFIER, i);
}

tree::TerminalNode* JTMLElementParser::JtmlElementContext::BACKSLASH() {
  return getToken(JTMLElementParser::BACKSLASH, 0);
}

JTMLElementParser::AttributesContext* JTMLElementParser::JtmlElementContext::attributes() {
  return getRuleContext<JTMLElementParser::AttributesContext>(0);
}

JTMLElementParser::ContentContext* JTMLElementParser::JtmlElementContext::content() {
  return getRuleContext<JTMLElementParser::ContentContext>(0);
}


size_t JTMLElementParser::JtmlElementContext::getRuleIndex() const {
  return JTMLElementParser::RuleJtmlElement;
}

void JTMLElementParser::JtmlElementContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterJtmlElement(this);
}

void JTMLElementParser::JtmlElementContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitJtmlElement(this);
}


std::any JTMLElementParser::JtmlElementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitJtmlElement(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::JtmlElementContext* JTMLElementParser::jtmlElement() {
  JtmlElementContext *_localctx = _tracker.createInstance<JtmlElementContext>(_ctx, getState());
  enterRule(_localctx, 0, JTMLElementParser::RuleJtmlElement);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(14);
    match(JTMLElementParser::HASH);
    setState(15);
    match(JTMLElementParser::IDENTIFIER);
    setState(17);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JTMLElementParser::IDENTIFIER) {
      setState(16);
      attributes();
    }
    setState(19);
    match(JTMLElementParser::BACKSLASH);
    setState(21);
    _errHandler->sync(this);

    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 1, _ctx)) {
    case 1: {
      setState(20);
      content();
      break;
    }

    default:
      break;
    }
    setState(23);
    match(JTMLElementParser::HASH);
    setState(25);
    _errHandler->sync(this);

    _la = _input->LA(1);
    if (_la == JTMLElementParser::IDENTIFIER) {
      setState(24);
      match(JTMLElementParser::IDENTIFIER);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- AttributesContext ------------------------------------------------------------------

JTMLElementParser::AttributesContext::AttributesContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

std::vector<tree::TerminalNode *> JTMLElementParser::AttributesContext::IDENTIFIER() {
  return getTokens(JTMLElementParser::IDENTIFIER);
}

tree::TerminalNode* JTMLElementParser::AttributesContext::IDENTIFIER(size_t i) {
  return getToken(JTMLElementParser::IDENTIFIER, i);
}

std::vector<tree::TerminalNode *> JTMLElementParser::AttributesContext::COLON() {
  return getTokens(JTMLElementParser::COLON);
}

tree::TerminalNode* JTMLElementParser::AttributesContext::COLON(size_t i) {
  return getToken(JTMLElementParser::COLON, i);
}

std::vector<tree::TerminalNode *> JTMLElementParser::AttributesContext::STRING_LITERAL() {
  return getTokens(JTMLElementParser::STRING_LITERAL);
}

tree::TerminalNode* JTMLElementParser::AttributesContext::STRING_LITERAL(size_t i) {
  return getToken(JTMLElementParser::STRING_LITERAL, i);
}

std::vector<tree::TerminalNode *> JTMLElementParser::AttributesContext::COMMA() {
  return getTokens(JTMLElementParser::COMMA);
}

tree::TerminalNode* JTMLElementParser::AttributesContext::COMMA(size_t i) {
  return getToken(JTMLElementParser::COMMA, i);
}


size_t JTMLElementParser::AttributesContext::getRuleIndex() const {
  return JTMLElementParser::RuleAttributes;
}

void JTMLElementParser::AttributesContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterAttributes(this);
}

void JTMLElementParser::AttributesContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitAttributes(this);
}


std::any JTMLElementParser::AttributesContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitAttributes(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::AttributesContext* JTMLElementParser::attributes() {
  AttributesContext *_localctx = _tracker.createInstance<AttributesContext>(_ctx, getState());
  enterRule(_localctx, 2, JTMLElementParser::RuleAttributes);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(27);
    match(JTMLElementParser::IDENTIFIER);
    setState(28);
    match(JTMLElementParser::COLON);
    setState(29);
    match(JTMLElementParser::STRING_LITERAL);
    setState(36);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JTMLElementParser::COMMA) {
      setState(30);
      match(JTMLElementParser::COMMA);
      setState(31);
      match(JTMLElementParser::IDENTIFIER);
      setState(32);
      match(JTMLElementParser::COLON);
      setState(33);
      match(JTMLElementParser::STRING_LITERAL);
      setState(38);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ContentContext ------------------------------------------------------------------

JTMLElementParser::ContentContext::ContentContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JTMLElementParser::StatementContext* JTMLElementParser::ContentContext::statement() {
  return getRuleContext<JTMLElementParser::StatementContext>(0);
}

std::vector<tree::TerminalNode *> JTMLElementParser::ContentContext::BACKSLASH() {
  return getTokens(JTMLElementParser::BACKSLASH);
}

tree::TerminalNode* JTMLElementParser::ContentContext::BACKSLASH(size_t i) {
  return getToken(JTMLElementParser::BACKSLASH, i);
}


size_t JTMLElementParser::ContentContext::getRuleIndex() const {
  return JTMLElementParser::RuleContent;
}

void JTMLElementParser::ContentContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterContent(this);
}

void JTMLElementParser::ContentContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitContent(this);
}


std::any JTMLElementParser::ContentContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitContent(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::ContentContext* JTMLElementParser::content() {
  ContentContext *_localctx = _tracker.createInstance<ContentContext>(_ctx, getState());
  enterRule(_localctx, 4, JTMLElementParser::RuleContent);
  size_t _la = 0;

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(39);
    statement();
    setState(43);
    _errHandler->sync(this);
    _la = _input->LA(1);
    while (_la == JTMLElementParser::BACKSLASH) {
      setState(40);
      match(JTMLElementParser::BACKSLASH);
      setState(45);
      _errHandler->sync(this);
      _la = _input->LA(1);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- StatementContext ------------------------------------------------------------------

JTMLElementParser::StatementContext::StatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

JTMLElementParser::ShowStatementContext* JTMLElementParser::StatementContext::showStatement() {
  return getRuleContext<JTMLElementParser::ShowStatementContext>(0);
}

JTMLElementParser::DefineStatementContext* JTMLElementParser::StatementContext::defineStatement() {
  return getRuleContext<JTMLElementParser::DefineStatementContext>(0);
}


size_t JTMLElementParser::StatementContext::getRuleIndex() const {
  return JTMLElementParser::RuleStatement;
}

void JTMLElementParser::StatementContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterStatement(this);
}

void JTMLElementParser::StatementContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitStatement(this);
}


std::any JTMLElementParser::StatementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitStatement(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::StatementContext* JTMLElementParser::statement() {
  StatementContext *_localctx = _tracker.createInstance<StatementContext>(_ctx, getState());
  enterRule(_localctx, 6, JTMLElementParser::RuleStatement);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    setState(49);
    _errHandler->sync(this);
    switch (_input->LA(1)) {
      case JTMLElementParser::SHOW: {
        enterOuterAlt(_localctx, 1);
        setState(46);
        showStatement();
        break;
      }

      case JTMLElementParser::DEFINE: {
        enterOuterAlt(_localctx, 2);
        setState(47);
        defineStatement();
        break;
      }

      case JTMLElementParser::HASH:
      case JTMLElementParser::BACKSLASH: {
        enterOuterAlt(_localctx, 3);

        break;
      }

    default:
      throw NoViableAltException(this);
    }
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ShowStatementContext ------------------------------------------------------------------

JTMLElementParser::ShowStatementContext::ShowStatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JTMLElementParser::ShowStatementContext::SHOW() {
  return getToken(JTMLElementParser::SHOW, 0);
}

tree::TerminalNode* JTMLElementParser::ShowStatementContext::STRING_LITERAL() {
  return getToken(JTMLElementParser::STRING_LITERAL, 0);
}


size_t JTMLElementParser::ShowStatementContext::getRuleIndex() const {
  return JTMLElementParser::RuleShowStatement;
}

void JTMLElementParser::ShowStatementContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterShowStatement(this);
}

void JTMLElementParser::ShowStatementContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitShowStatement(this);
}


std::any JTMLElementParser::ShowStatementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitShowStatement(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::ShowStatementContext* JTMLElementParser::showStatement() {
  ShowStatementContext *_localctx = _tracker.createInstance<ShowStatementContext>(_ctx, getState());
  enterRule(_localctx, 8, JTMLElementParser::RuleShowStatement);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(51);
    match(JTMLElementParser::SHOW);
    setState(52);
    match(JTMLElementParser::STRING_LITERAL);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- DefineStatementContext ------------------------------------------------------------------

JTMLElementParser::DefineStatementContext::DefineStatementContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JTMLElementParser::DefineStatementContext::DEFINE() {
  return getToken(JTMLElementParser::DEFINE, 0);
}

tree::TerminalNode* JTMLElementParser::DefineStatementContext::IDENTIFIER() {
  return getToken(JTMLElementParser::IDENTIFIER, 0);
}

tree::TerminalNode* JTMLElementParser::DefineStatementContext::EQUALS() {
  return getToken(JTMLElementParser::EQUALS, 0);
}

JTMLElementParser::ExpressionContext* JTMLElementParser::DefineStatementContext::expression() {
  return getRuleContext<JTMLElementParser::ExpressionContext>(0);
}


size_t JTMLElementParser::DefineStatementContext::getRuleIndex() const {
  return JTMLElementParser::RuleDefineStatement;
}

void JTMLElementParser::DefineStatementContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterDefineStatement(this);
}

void JTMLElementParser::DefineStatementContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitDefineStatement(this);
}


std::any JTMLElementParser::DefineStatementContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitDefineStatement(this);
  else
    return visitor->visitChildren(this);
}

JTMLElementParser::DefineStatementContext* JTMLElementParser::defineStatement() {
  DefineStatementContext *_localctx = _tracker.createInstance<DefineStatementContext>(_ctx, getState());
  enterRule(_localctx, 10, JTMLElementParser::RuleDefineStatement);

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    exitRule();
  });
  try {
    enterOuterAlt(_localctx, 1);
    setState(54);
    match(JTMLElementParser::DEFINE);
    setState(55);
    match(JTMLElementParser::IDENTIFIER);
    setState(56);
    match(JTMLElementParser::EQUALS);
    setState(57);
    expression(0);
   
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }

  return _localctx;
}

//----------------- ExpressionContext ------------------------------------------------------------------

JTMLElementParser::ExpressionContext::ExpressionContext(ParserRuleContext *parent, size_t invokingState)
  : ParserRuleContext(parent, invokingState) {
}

tree::TerminalNode* JTMLElementParser::ExpressionContext::IDENTIFIER() {
  return getToken(JTMLElementParser::IDENTIFIER, 0);
}

tree::TerminalNode* JTMLElementParser::ExpressionContext::NUMBER_LITERAL() {
  return getToken(JTMLElementParser::NUMBER_LITERAL, 0);
}

tree::TerminalNode* JTMLElementParser::ExpressionContext::STRING_LITERAL() {
  return getToken(JTMLElementParser::STRING_LITERAL, 0);
}

std::vector<JTMLElementParser::ExpressionContext *> JTMLElementParser::ExpressionContext::expression() {
  return getRuleContexts<JTMLElementParser::ExpressionContext>();
}

JTMLElementParser::ExpressionContext* JTMLElementParser::ExpressionContext::expression(size_t i) {
  return getRuleContext<JTMLElementParser::ExpressionContext>(i);
}

tree::TerminalNode* JTMLElementParser::ExpressionContext::PLUS() {
  return getToken(JTMLElementParser::PLUS, 0);
}

tree::TerminalNode* JTMLElementParser::ExpressionContext::MINUS() {
  return getToken(JTMLElementParser::MINUS, 0);
}


size_t JTMLElementParser::ExpressionContext::getRuleIndex() const {
  return JTMLElementParser::RuleExpression;
}

void JTMLElementParser::ExpressionContext::enterRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->enterExpression(this);
}

void JTMLElementParser::ExpressionContext::exitRule(tree::ParseTreeListener *listener) {
  auto parserListener = dynamic_cast<JTMLElementListener *>(listener);
  if (parserListener != nullptr)
    parserListener->exitExpression(this);
}


std::any JTMLElementParser::ExpressionContext::accept(tree::ParseTreeVisitor *visitor) {
  if (auto parserVisitor = dynamic_cast<JTMLElementVisitor*>(visitor))
    return parserVisitor->visitExpression(this);
  else
    return visitor->visitChildren(this);
}


JTMLElementParser::ExpressionContext* JTMLElementParser::expression() {
   return expression(0);
}

JTMLElementParser::ExpressionContext* JTMLElementParser::expression(int precedence) {
  ParserRuleContext *parentContext = _ctx;
  size_t parentState = getState();
  JTMLElementParser::ExpressionContext *_localctx = _tracker.createInstance<ExpressionContext>(_ctx, parentState);
  JTMLElementParser::ExpressionContext *previousContext = _localctx;
  (void)previousContext; // Silence compiler, in case the context is not used by generated code.
  size_t startState = 12;
  enterRecursionRule(_localctx, 12, JTMLElementParser::RuleExpression, precedence);

    

#if __cplusplus > 201703L
  auto onExit = finally([=, this] {
#else
  auto onExit = finally([=] {
#endif
    unrollRecursionContexts(parentContext);
  });
  try {
    size_t alt;
    enterOuterAlt(_localctx, 1);
    setState(64);
    _errHandler->sync(this);
    switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 6, _ctx)) {
    case 1: {
      setState(60);
      match(JTMLElementParser::IDENTIFIER);
      break;
    }

    case 2: {
      setState(61);
      match(JTMLElementParser::NUMBER_LITERAL);
      break;
    }

    case 3: {
      setState(62);
      match(JTMLElementParser::STRING_LITERAL);
      break;
    }

    case 4: {
      break;
    }

    default:
      break;
    }
    _ctx->stop = _input->LT(-1);
    setState(74);
    _errHandler->sync(this);
    alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx);
    while (alt != 2 && alt != atn::ATN::INVALID_ALT_NUMBER) {
      if (alt == 1) {
        if (!_parseListeners.empty())
          triggerExitRuleEvent();
        previousContext = _localctx;
        setState(72);
        _errHandler->sync(this);
        switch (getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 7, _ctx)) {
        case 1: {
          _localctx = _tracker.createInstance<ExpressionContext>(parentContext, parentState);
          pushNewRecursionContext(_localctx, startState, RuleExpression);
          setState(66);

          if (!(precpred(_ctx, 3))) throw FailedPredicateException(this, "precpred(_ctx, 3)");
          setState(67);
          match(JTMLElementParser::PLUS);
          setState(68);
          expression(4);
          break;
        }

        case 2: {
          _localctx = _tracker.createInstance<ExpressionContext>(parentContext, parentState);
          pushNewRecursionContext(_localctx, startState, RuleExpression);
          setState(69);

          if (!(precpred(_ctx, 2))) throw FailedPredicateException(this, "precpred(_ctx, 2)");
          setState(70);
          match(JTMLElementParser::MINUS);
          setState(71);
          expression(3);
          break;
        }

        default:
          break;
        } 
      }
      setState(76);
      _errHandler->sync(this);
      alt = getInterpreter<atn::ParserATNSimulator>()->adaptivePredict(_input, 8, _ctx);
    }
  }
  catch (RecognitionException &e) {
    _errHandler->reportError(this, e);
    _localctx->exception = std::current_exception();
    _errHandler->recover(this, _localctx->exception);
  }
  return _localctx;
}

bool JTMLElementParser::sempred(RuleContext *context, size_t ruleIndex, size_t predicateIndex) {
  switch (ruleIndex) {
    case 6: return expressionSempred(antlrcpp::downCast<ExpressionContext *>(context), predicateIndex);

  default:
    break;
  }
  return true;
}

bool JTMLElementParser::expressionSempred(ExpressionContext *_localctx, size_t predicateIndex) {
  switch (predicateIndex) {
    case 0: return precpred(_ctx, 3);
    case 1: return precpred(_ctx, 2);

  default:
    break;
  }
  return true;
}

void JTMLElementParser::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  jtmlelementParserInitialize();
#else
  ::antlr4::internal::call_once(jtmlelementParserOnceFlag, jtmlelementParserInitialize);
#endif
}
