
// Generated from JTMLElement.g4 by ANTLR 4.13.0


#include "JTMLElementLexer.h"


using namespace antlr4;



using namespace antlr4;

namespace {

struct JTMLElementLexerStaticData final {
  JTMLElementLexerStaticData(std::vector<std::string> ruleNames,
                          std::vector<std::string> channelNames,
                          std::vector<std::string> modeNames,
                          std::vector<std::string> literalNames,
                          std::vector<std::string> symbolicNames)
      : ruleNames(std::move(ruleNames)), channelNames(std::move(channelNames)),
        modeNames(std::move(modeNames)), literalNames(std::move(literalNames)),
        symbolicNames(std::move(symbolicNames)),
        vocabulary(this->literalNames, this->symbolicNames) {}

  JTMLElementLexerStaticData(const JTMLElementLexerStaticData&) = delete;
  JTMLElementLexerStaticData(JTMLElementLexerStaticData&&) = delete;
  JTMLElementLexerStaticData& operator=(const JTMLElementLexerStaticData&) = delete;
  JTMLElementLexerStaticData& operator=(JTMLElementLexerStaticData&&) = delete;

  std::vector<antlr4::dfa::DFA> decisionToDFA;
  antlr4::atn::PredictionContextCache sharedContextCache;
  const std::vector<std::string> ruleNames;
  const std::vector<std::string> channelNames;
  const std::vector<std::string> modeNames;
  const std::vector<std::string> literalNames;
  const std::vector<std::string> symbolicNames;
  const antlr4::dfa::Vocabulary vocabulary;
  antlr4::atn::SerializedATNView serializedATN;
  std::unique_ptr<antlr4::atn::ATN> atn;
};

::antlr4::internal::OnceFlag jtmlelementlexerLexerOnceFlag;
#if ANTLR4_USE_THREAD_LOCAL_CACHE
static thread_local
#endif
JTMLElementLexerStaticData *jtmlelementlexerLexerStaticData = nullptr;

void jtmlelementlexerLexerInitialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  if (jtmlelementlexerLexerStaticData != nullptr) {
    return;
  }
#else
  assert(jtmlelementlexerLexerStaticData == nullptr);
#endif
  auto staticData = std::make_unique<JTMLElementLexerStaticData>(
    std::vector<std::string>{
      "HASH", "COLON", "COMMA", "BACKSLASH", "EQUALS", "PLUS", "MINUS", 
      "SHOW", "DEFINE", "IDENTIFIER", "STRING_LITERAL", "NUMBER_LITERAL", 
      "WS"
    },
    std::vector<std::string>{
      "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    },
    std::vector<std::string>{
      "DEFAULT_MODE"
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
  	4,0,13,92,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
  	6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,1,0,1,0,1,1,1,
  	1,1,2,1,2,1,3,1,3,1,3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,7,1,7,1,7,1,8,
  	1,8,1,8,1,8,1,8,1,8,1,8,1,9,1,9,5,9,57,8,9,10,9,12,9,60,9,9,1,10,1,10,
  	1,10,1,10,5,10,66,8,10,10,10,12,10,69,9,10,1,10,1,10,1,11,4,11,74,8,11,
  	11,11,12,11,75,1,11,1,11,4,11,80,8,11,11,11,12,11,81,3,11,84,8,11,1,12,
  	4,12,87,8,12,11,12,12,12,88,1,12,1,12,0,0,13,1,1,3,2,5,3,7,4,9,5,11,6,
  	13,7,15,8,17,9,19,10,21,11,23,12,25,13,1,0,5,3,0,65,90,95,95,97,122,4,
  	0,48,57,65,90,95,95,97,122,2,0,34,34,92,92,1,0,48,57,3,0,9,10,13,13,32,
  	32,98,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,
  	1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,
  	0,0,0,23,1,0,0,0,0,25,1,0,0,0,1,27,1,0,0,0,3,29,1,0,0,0,5,31,1,0,0,0,
  	7,33,1,0,0,0,9,36,1,0,0,0,11,38,1,0,0,0,13,40,1,0,0,0,15,42,1,0,0,0,17,
  	47,1,0,0,0,19,54,1,0,0,0,21,61,1,0,0,0,23,73,1,0,0,0,25,86,1,0,0,0,27,
  	28,5,35,0,0,28,2,1,0,0,0,29,30,5,58,0,0,30,4,1,0,0,0,31,32,5,44,0,0,32,
  	6,1,0,0,0,33,34,5,92,0,0,34,35,5,92,0,0,35,8,1,0,0,0,36,37,5,61,0,0,37,
  	10,1,0,0,0,38,39,5,43,0,0,39,12,1,0,0,0,40,41,5,45,0,0,41,14,1,0,0,0,
  	42,43,5,115,0,0,43,44,5,104,0,0,44,45,5,111,0,0,45,46,5,119,0,0,46,16,
  	1,0,0,0,47,48,5,100,0,0,48,49,5,101,0,0,49,50,5,102,0,0,50,51,5,105,0,
  	0,51,52,5,110,0,0,52,53,5,101,0,0,53,18,1,0,0,0,54,58,7,0,0,0,55,57,7,
  	1,0,0,56,55,1,0,0,0,57,60,1,0,0,0,58,56,1,0,0,0,58,59,1,0,0,0,59,20,1,
  	0,0,0,60,58,1,0,0,0,61,67,5,34,0,0,62,66,8,2,0,0,63,64,5,92,0,0,64,66,
  	9,0,0,0,65,62,1,0,0,0,65,63,1,0,0,0,66,69,1,0,0,0,67,65,1,0,0,0,67,68,
  	1,0,0,0,68,70,1,0,0,0,69,67,1,0,0,0,70,71,5,34,0,0,71,22,1,0,0,0,72,74,
  	7,3,0,0,73,72,1,0,0,0,74,75,1,0,0,0,75,73,1,0,0,0,75,76,1,0,0,0,76,83,
  	1,0,0,0,77,79,5,46,0,0,78,80,7,3,0,0,79,78,1,0,0,0,80,81,1,0,0,0,81,79,
  	1,0,0,0,81,82,1,0,0,0,82,84,1,0,0,0,83,77,1,0,0,0,83,84,1,0,0,0,84,24,
  	1,0,0,0,85,87,7,4,0,0,86,85,1,0,0,0,87,88,1,0,0,0,88,86,1,0,0,0,88,89,
  	1,0,0,0,89,90,1,0,0,0,90,91,6,12,0,0,91,26,1,0,0,0,8,0,58,65,67,75,81,
  	83,88,1,6,0,0
  };
  staticData->serializedATN = antlr4::atn::SerializedATNView(serializedATNSegment, sizeof(serializedATNSegment) / sizeof(serializedATNSegment[0]));

  antlr4::atn::ATNDeserializer deserializer;
  staticData->atn = deserializer.deserialize(staticData->serializedATN);

  const size_t count = staticData->atn->getNumberOfDecisions();
  staticData->decisionToDFA.reserve(count);
  for (size_t i = 0; i < count; i++) { 
    staticData->decisionToDFA.emplace_back(staticData->atn->getDecisionState(i), i);
  }
  jtmlelementlexerLexerStaticData = staticData.release();
}

}

JTMLElementLexer::JTMLElementLexer(CharStream *input) : Lexer(input) {
  JTMLElementLexer::initialize();
  _interpreter = new atn::LexerATNSimulator(this, *jtmlelementlexerLexerStaticData->atn, jtmlelementlexerLexerStaticData->decisionToDFA, jtmlelementlexerLexerStaticData->sharedContextCache);
}

JTMLElementLexer::~JTMLElementLexer() {
  delete _interpreter;
}

std::string JTMLElementLexer::getGrammarFileName() const {
  return "JTMLElement.g4";
}

const std::vector<std::string>& JTMLElementLexer::getRuleNames() const {
  return jtmlelementlexerLexerStaticData->ruleNames;
}

const std::vector<std::string>& JTMLElementLexer::getChannelNames() const {
  return jtmlelementlexerLexerStaticData->channelNames;
}

const std::vector<std::string>& JTMLElementLexer::getModeNames() const {
  return jtmlelementlexerLexerStaticData->modeNames;
}

const dfa::Vocabulary& JTMLElementLexer::getVocabulary() const {
  return jtmlelementlexerLexerStaticData->vocabulary;
}

antlr4::atn::SerializedATNView JTMLElementLexer::getSerializedATN() const {
  return jtmlelementlexerLexerStaticData->serializedATN;
}

const atn::ATN& JTMLElementLexer::getATN() const {
  return *jtmlelementlexerLexerStaticData->atn;
}




void JTMLElementLexer::initialize() {
#if ANTLR4_USE_THREAD_LOCAL_CACHE
  jtmlelementlexerLexerInitialize();
#else
  ::antlr4::internal::call_once(jtmlelementlexerLexerOnceFlag, jtmlelementlexerLexerInitialize);
#endif
}
