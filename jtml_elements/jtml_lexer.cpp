#pragma once

#include <string>
#include <vector>
#include <stdexcept>
#include <cctype>

enum class TokenType {
    HASH,            
    BACKSLASH_HASH,   
    PLUS,
    PLUSEQ,
    MINUSEQ,
    MULTIPLYEQ,
    DIVIDEEQ,
    MODULUSEQ,
    POWEREQ,
    NOT,
    LT,
    GT,
    LTEQ,
    GTEQ,
    EQ,
    NEQ,
    ASSIGN,       
    MINUS,
    MULTIPLY,
    DIVIDE,
    MODULUS,
    POWER,
    LPAREN,
    RPAREN,
    COMMA,
    COLON,
    STMT_TERMINATOR,  
    AND,
    OR,
    SHOW,             
    DEFINE,           
    DERIVE,
    UNBIND,
    STORE,
    FOR,
    IF,
    CONST,
    IN,
    BREAK,
    CONTINUE,
    THROW,
    ELSE,
    WHILE,
    TRY,
    EXCEPT,
    THEN,
    RETURN,
    FUNCTION,
    OBJECT,
    THIS,
    ASYNC,
    IMPORT,
    MAIN,
    IDENTIFIER,
    STRING_LITERAL,
    END_OF_FILE,
    ERROR
};

struct Token {
    TokenType type;
    std::string text;
    int position; 
    int line;
    int column;
};

class Lexer {
public:
    explicit Lexer(const std::string& input)
        : m_input(input), m_pos(0), m_line(1), m_column(1) {}

    std::vector<Token> tokenize() {
        std::vector<Token> tokens;
        
        while (!isEOF()) {
            char c = peek();
            if (std::isspace(static_cast<unsigned char>(c))) {
                advance();
                continue;
            }

            if (matchSequence("\\\\")) {
                tokens.push_back(makeToken(TokenType::STMT_TERMINATOR, "\\\\"));
                m_pos += 2;
                continue;
            }
          
            if (matchSequence("\\#")) {
                tokens.push_back(makeToken(TokenType::BACKSLASH_HASH, "\\#"));
                m_pos += 2;
                continue;
            }

            if (matchSequence("-=")) {
                tokens.push_back(makeToken(TokenType::MINUSEQ, "-="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("+=")) {
                tokens.push_back(makeToken(TokenType::PLUSEQ, "+="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("*=")) {
                tokens.push_back(makeToken(TokenType::MULTIPLYEQ, "*="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("/=")) {
                tokens.push_back(makeToken(TokenType::DIVIDEEQ, "/="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("%=")) {
                tokens.push_back(makeToken(TokenType::MODULUSEQ, "%="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("^=")) {
                tokens.push_back(makeToken(TokenType::POWEREQ, "^="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("==")) {
                tokens.push_back(makeToken(TokenType::EQ, "=="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("<=")) {
                tokens.push_back(makeToken(TokenType::LTEQ, "<="));
                m_pos += 2;
                continue;
            }
            if (matchSequence(">=")) {
                tokens.push_back(makeToken(TokenType::GTEQ, ">="));
                m_pos += 2;
                continue;
            }
            if (matchSequence("!=")) {
                tokens.push_back(makeToken(TokenType::NEQ, "!="));
                m_pos += 2;
                continue;
            }
  
            switch (c) {
                case '#':
                    tokens.push_back(makeToken(TokenType::HASH, "#"));
                    advance();
                    break;
                case '(':
                    tokens.push_back(makeToken(TokenType::LPAREN, "("));
                    advance();
                    break;
                case ')':
                    tokens.push_back(makeToken(TokenType::RPAREN, ")"));
                    advance();
                    break;
                case '+':
                    tokens.push_back(makeToken(TokenType::PLUS, "+"));
                    advance();
                    break;
                case '*':
                    tokens.push_back(makeToken(TokenType::MULTIPLY, "*"));
                    advance();
                    break;
                case '-':
                    tokens.push_back(makeToken(TokenType::MINUS, "-"));
                    advance();
                    break;
                case '/':
                    tokens.push_back(makeToken(TokenType::DIVIDE, "/"));
                    advance();
                    break;
                case '%':
                    tokens.push_back(makeToken(TokenType::MODULUS, "%"));
                    advance();
                    break;
                case '<':
                    tokens.push_back(makeToken(TokenType::LT, "<"));
                    advance();
                    break;
                case '>':
                    tokens.push_back(makeToken(TokenType::GT, ">"));
                    advance();
                    break;
                case '!':
                    tokens.push_back(makeToken(TokenType::NOT, "!"));
                    advance();
                    break;
                case ',':
                    tokens.push_back(makeToken(TokenType::COMMA, ","));
                    advance();
                    break;
                case ':':
                    tokens.push_back(makeToken(TokenType::COLON, ":"));
                    advance();
                    break;
                case '=':
                    tokens.push_back(makeToken(TokenType::ASSIGN, "="));
                    advance();
                    break;
                case '"':
                    tokens.push_back(consumeStringLiteral(c));
                    break;
                case '\'':
                    tokens.push_back(consumeStringLiteral(c));
                    break;
                default:
                    if (std::isalpha(static_cast<unsigned char>(c)) || c == '_') {
                        Token tk = consumeIdentifier();
                        if (tk.text == "show")   tk.type = TokenType::SHOW;
                        if (tk.text == "define") tk.type = TokenType::DEFINE;
                        if (tk.text == "unbind") tk.type = TokenType::UNBIND;
                        if (tk.text == "store") tk.type = TokenType::STORE;
                        if (tk.text == "and") tk.type = TokenType::AND;
                        if (tk.text == "or") tk.type = TokenType::OR;
                        if (tk.text == "for") tk.type = TokenType::FOR;
                        if (tk.text == "if") tk.type = TokenType::IF;
                        if (tk.text == "const") tk.type = TokenType::CONST;
                        if (tk.text == "in") tk.type = TokenType::IN;
                        if (tk.text == "break") tk.type = TokenType::BREAK;
                        if (tk.text == "continue") tk.type = TokenType::CONTINUE;
                        if (tk.text == "throw") tk.type = TokenType::THROW;
                        if (tk.text == "else") tk.type = TokenType::ELSE;
                        if (tk.text == "while") tk.type = TokenType::WHILE;
                        if (tk.text == "try") tk.type = TokenType::TRY;
                        if (tk.text == "except") tk.type = TokenType::EXCEPT;
                        if (tk.text == "then") tk.type = TokenType::THEN;
                        if (tk.text == "return") tk.type = TokenType::RETURN;
                        if (tk.text == "function") tk.type = TokenType::FUNCTION;
                        if (tk.text == "object") tk.type = TokenType::OBJECT;
                        if (tk.text == "this") tk.type = TokenType::THIS;
                        if (tk.text == "async") tk.type = TokenType::ASYNC;
                        if (tk.text == "import") tk.type = TokenType::IMPORT;
                        if (tk.text == "main") tk.type = TokenType::MAIN;
                        tokens.push_back(tk);
                    } else {
                        errors.push_back("Error at line " + 
                                    std::to_string(m_line) + ", column " + 
                                    std::to_string(m_column) + ": " + ": Unexpected character '" + c + "'");
                        recoverFromError(); 
                    }
            }
        }
        tokens.push_back(Token{TokenType::END_OF_FILE, "<EOF>", static_cast<int>(m_pos), m_line, m_column});
        return tokens;
    }

    const std::vector<std::string>& getErrors() const {
        return errors;
    }

private:
    std::string m_input;
    size_t m_pos;
    int m_line;
    int m_column;

    std::vector<std::string> errors;

    bool isEOF() const {
        return m_pos >= m_input.size();
    }

    char peek() const {
        if (m_pos < m_input.size()) {
            return m_input[m_pos];
        }
        return '\0';
    }

    void recoverFromError() {
        while (!isEOF()) {
            char c = peek();
            if (c == '\\' || c == '\n') {
                advance();
                break; 
            }
            advance();
        }
    }

    void advance() {
        if (m_pos < m_input.size()) {
            if (m_input[m_pos] == '\n') {
                ++m_line;
                m_column = 1;  
            } else {
                ++m_column;
            }
            ++m_pos;
        }
    }

    bool matchSequence(const std::string& seq) {
        if (m_pos + seq.size() <= m_input.size()) {
            return m_input.compare(m_pos, seq.size(), seq) == 0;
        }
        return false;
    }

    Token makeToken(TokenType type, const std::string& text) {
        return Token{ type, text, static_cast<int>(m_pos), m_line, m_column };
    }

    Token consumeStringLiteral(char quoteChar) {
        size_t startPos = m_pos;
        int startLine = m_line;
        int startColumn = m_column;

        advance();

        std::string value;

        while (!isEOF() && peek() != quoteChar) {
            if (peek() == '\\') {
                advance();
                if (!isEOF()) {
                    value.push_back(peek());
                    advance();
                }
            } else {
                value.push_back(peek());
                advance();
            }
        }
        if (peek() != quoteChar) {
            errors.emplace_back("Unterminated string at line " + std::to_string(startLine)
                + ", column " + std::to_string(startColumn));
            return Token{TokenType::ERROR, value, static_cast<int>(startPos), startLine, startColumn};
        }
        advance(); 

        return Token{TokenType::STRING_LITERAL, value, static_cast<int>(startPos), startLine, startColumn};
    }

   Token consumeIdentifier() {
        size_t start = m_pos;
        int startLine = m_line;
        int startColumn = m_column;

        while (std::isalnum(static_cast<unsigned char>(peek())) || peek() == '_') {
            advance();
        }
        std::string value = m_input.substr(start, m_pos - start);
        return Token{TokenType::IDENTIFIER, value, static_cast<int>(start), startLine, startColumn};
    }
};
