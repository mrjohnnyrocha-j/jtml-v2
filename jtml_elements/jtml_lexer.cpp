#pragma once

#include <string>
#include <vector>
#include <stdexcept>
#include <cctype>

/**
 * TokenType enumerates all token categories for jtml:
 *  - '#' / '\#'
 *  - ',' / ':' / '='
 *  - STMT_TERMINATOR: '\\' (double-backslash in grammar)
 *  - SHOW / DEFINE (keywords)
 *  - IDENTIFIER, STRING_LITERAL
 *  - END_OF_FILE
 */
enum class TokenType {
    HASH,              // '#'
    BACKSLASH_HASH,    // '\#'
    PLUS,
    PLUSEQ,
    MINUSEQ,
    MULTIPLYEQ,
    DIVIDEEQ,
    MODULUSEQ,
    POWEREQ,
    AND,
    OR,
    NOT,
    LT,
    GT,
    LTEQ,
    GTEQ,
    EQ,
    NEQ,
    ASSIGN,           // '='
    MINUS,
    MULTIPLY,
    DIVIDE,
    MODULUS,
    POWER,
    LPAREN,
    RPAREN,
    COMMA,             // ','
    COLON,             // ':'
    STMT_TERMINATOR,   // '\\'
    SHOW,              // 'show'
    DEFINE,            // 'define'
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
    CATCH,
    FINALLY,
    RETURN,
    FUNCTION,
    OBJECT,
    THIS,
    ASYNC,
    IMPORT,
    MAIN,
    IDENTIFIER,
    STRING_LITERAL,
    END_OF_FILE
};

struct Token {
    TokenType type;
    std::string text;
    int position;  // for error messages
};

class Lexer {
public:
    explicit Lexer(const std::string& input)
        : m_input(input), m_pos(0) {}

    std::vector<Token> tokenize() {
        std::vector<Token> tokens;
        while (!isEOF()) {
            char c = peek();
            if (std::isspace(static_cast<unsigned char>(c))) {
                advance();
                continue;
            }

            // Detect double-backslash => STMT_TERMINATOR
            if (matchSequence("\\\\")) {
                tokens.push_back(makeToken(TokenType::STMT_TERMINATOR, "\\\\"));
                m_pos += 2;
                continue;
            }
            // Detect "\#"
            if (matchSequence("\\#")) {
                tokens.push_back(makeToken(TokenType::BACKSLASH_HASH, "\\#"));
                m_pos += 2;
                continue;
            }

            switch (c) {
                case '#':
                    tokens.push_back(makeToken(TokenType::HASH, "#"));
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
                    tokens.push_back(consumeStringLiteral());
                    break;
                default:
                    if (std::isalpha(static_cast<unsigned char>(c)) || c == '_') {
                        Token tk = consumeIdentifier();
                        if (tk.text == "show")   tk.type = TokenType::SHOW;
                        if (tk.text == "define") tk.type = TokenType::DEFINE;
                        tokens.push_back(tk);
                    } else {
                        throw std::runtime_error("Unexpected char '" + std::string(1, c)
                            + "' at position " + std::to_string(m_pos));
                    }
            }
        }
        tokens.push_back(Token{TokenType::END_OF_FILE, "<EOF>", static_cast<int>(m_pos)});
        return tokens;
    }

private:
    std::string m_input;
    size_t m_pos;

    bool isEOF() const {
        return m_pos >= m_input.size();
    }

    char peek() const {
        if (m_pos < m_input.size()) {
            return m_input[m_pos];
        }
        return '\0';
    }

    void advance() {
        m_pos++;
    }

    bool matchSequence(const std::string& seq) {
        if (m_pos + seq.size() <= m_input.size()) {
            return m_input.compare(m_pos, seq.size(), seq) == 0;
        }
        return false;
    }

    Token makeToken(TokenType type, const std::string& text) {
        return Token{ type, text, static_cast<int>(m_pos) };
    }

    Token consumeStringLiteral() {
        // skip the opening quote
        size_t startPos = m_pos;
        advance(); // consume the opening '"'

        std::string value;
        while (!isEOF() && peek() != '"') {
            if (peek() == '\\') {
                // handle escape
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
        if (peek() != '"') {
            throw std::runtime_error("Unterminated string at position " + std::to_string(m_pos));
        }
        advance(); // skip closing quote

        return Token{TokenType::STRING_LITERAL, value, static_cast<int>(startPos)};
    }

    Token consumeIdentifier() {
        size_t startPos = m_pos;
        std::string result;
        while (!isEOF()) {
            char c = peek();
            if (std::isalnum(static_cast<unsigned char>(c)) || c == '_') {
                result.push_back(c);
                advance();
            } else {
                break;
            }
        }
        return Token{TokenType::IDENTIFIER, result, static_cast<int>(startPos)};
    }
};
