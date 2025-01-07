#pragma once

#include "jtml_ast.cpp"
#include "jtml_lexer.cpp"
#include <memory>
#include <stdexcept>

/**
 * Simplified grammar:
 * 
 * jtmlElement
 *   : '#' IDENTIFIER jtmlBody? '\#' IDENTIFIER
 * 
 * jtmlBody
 *   : [ jtmlAttributes ( STMT_TERMINATOR )? ] jtmlContentItem*
 * 
 * jtmlAttributes
 *   : attribute (',' attribute)*
 * 
 * attribute
 *   : IDENTIFIER ':' STRING_LITERAL
 * 
 * jtmlContentItem
 *   : showStatement
 *   | defineStatement
 *   | jtmlElement
 * 
 * showStatement
 *   : 'show' STRING_LITERAL STMT_TERMINATOR
 * 
 * defineStatement
 *   : 'define' IDENTIFIER '=' expression STMT_TERMINATOR
 * 
 * expression
 *   : IDENTIFIER
 *   | STRING_LITERAL
 */
class Parser {
public:
    explicit Parser(std::vector<Token> tokens)
        : m_tokens(std::move(tokens)), m_pos(0) {}

    // Parse a single top-level jtmlElement
    std::unique_ptr<JtmlElementNode> parseJtmlElement() {
        consume(TokenType::HASH, "Expected '#'");
        Token openTag = consume(TokenType::IDENTIFIER, "Expected identifier after '#'");

        auto elem = std::make_unique<JtmlElementNode>();
        elem->tagName = openTag.text;

        // jtmlBody? (if not immediately BACKSLASH_HASH or EOF)
        if (!check(TokenType::BACKSLASH_HASH) && !check(TokenType::END_OF_FILE)) {
            parseJtmlBody(*elem);
        }

        consume(TokenType::BACKSLASH_HASH, "Expected '\\#'");
        Token closeTag = consume(TokenType::IDENTIFIER, "Expected identifier after '\\#'");
        if (closeTag.text != openTag.text) {
            throw std::runtime_error("Mismatched closing tag: " 
                                     + closeTag.text + " != " + openTag.text);
        }
        return elem;
    }

private:
    std::vector<Token> m_tokens;
    size_t m_pos;

    void parseJtmlBody(JtmlElementNode& elem) {
        // optional attributes
        if (lookAheadIsAttribute()) {
            parseAttributes(elem.attributes);
            // optional STMT_TERMINATOR after attributes
            match(TokenType::STMT_TERMINATOR);
        }
        // parse zero or more content items
        while (!check(TokenType::BACKSLASH_HASH) && !check(TokenType::END_OF_FILE)) {
            elem.content.push_back(parseContentItem());
        }
    }

    bool lookAheadIsAttribute() const {
        // Need: IDENTIFIER : STRING_LITERAL
        if (!check(TokenType::IDENTIFIER)) return false;
        if (!checkNext(TokenType::COLON))  return false;
        if (!checkNextNext(TokenType::STRING_LITERAL)) return false;
        return true;
    }

    void parseAttributes(std::vector<JtmlAttribute>& attrs) {
        // attribute (',' attribute)*
        attrs.push_back(parseOneAttribute());
        while (match(TokenType::COMMA)) {
            attrs.push_back(parseOneAttribute());
        }
    }

    JtmlAttribute parseOneAttribute() {
        Token idTok = consume(TokenType::IDENTIFIER, "Expected identifier in attribute");
        consume(TokenType::COLON, "Expected ':' in attribute");
        Token strTok = consume(TokenType::STRING_LITERAL, "Expected string literal in attribute");
        return { idTok.text, strTok.text };
    }

    std::unique_ptr<ASTNode> parseContentItem() {
        if (check(TokenType::SHOW)) {
            return parseShowStatement();
        } else if (check(TokenType::DEFINE)) {
            return parseDefineStatement();
        } else if (check(TokenType::HASH)) {
            return parseJtmlElement();
        }
        throw std::runtime_error("Unexpected token '" + peek().text + "' in content item.");
    }

    std::unique_ptr<ASTNode> parseShowStatement() {
        consume(TokenType::SHOW, "Expected 'show'");
        Token strTok = consume(TokenType::STRING_LITERAL, "Expected string literal after 'show'");
        consume(TokenType::STMT_TERMINATOR, "Expected '\\\\' after show statement");

        auto showNode = std::make_unique<ShowStatementNode>();
        showNode->message = strTok.text;
        return showNode;
    }

    std::unique_ptr<ASTNode> parseDefineStatement() {
        consume(TokenType::DEFINE, "Expected 'define'");
        Token idTok = consume(TokenType::IDENTIFIER, "Expected identifier after 'define'");
        consume(TokenType::ASSIGN, "Expected '=' in define statement");
        Token exprTok = peek();
        if (exprTok.type == TokenType::IDENTIFIER || exprTok.type == TokenType::STRING_LITERAL) {
            advance(); // consume the expression token
        } else {
            throw std::runtime_error("Expected IDENTIFIER or STRING_LITERAL in define statement.");
        }
        consume(TokenType::STMT_TERMINATOR, "Expected '\\\\' after define statement");

        auto defNode = std::make_unique<DefineStatementNode>();
        defNode->identifier = idTok.text;
        defNode->expression = exprTok.text;
        return defNode;
    }

    // -- Utility methods --
    bool check(TokenType type) const {
        if (isAtEnd()) return false;
        return peek().type == type;
    }
    bool checkNext(TokenType type) const {
        if (m_pos + 1 >= m_tokens.size()) return false;
        return m_tokens[m_pos + 1].type == type;
    }
    bool checkNextNext(TokenType type) const {
        if (m_pos + 2 >= m_tokens.size()) return false;
        return m_tokens[m_pos + 2].type == type;
    }

    bool match(TokenType type) {
        if (check(type)) {
            advance();
            return true;
        }
        return false;
    }

    Token consume(TokenType type, const std::string& errMsg) {
        if (check(type)) {
            return advance();
        }
        throw std::runtime_error(errMsg + " at position " + std::to_string(peek().position));
    }

    Token advance() {
        if (!isAtEnd()) m_pos++;
        return m_tokens[m_pos - 1];
    }

    bool isAtEnd() const {
        return peek().type == TokenType::END_OF_FILE;
    }

    const Token& peek() const {
        return m_tokens[m_pos];
    }
};

