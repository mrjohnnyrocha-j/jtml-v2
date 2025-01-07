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

    std::vector<std::unique_ptr<ASTNode>> parseProgram() {
        std::vector<std::unique_ptr<ASTNode>> nodes;
        while (!isAtEnd()) {
            try {
                auto stmt = parseStatement();
                if (stmt) {  // might be null if error
                    nodes.push_back(std::move(stmt));
                }
            } catch (const std::runtime_error& e) {
                recordError(e.what());
                synchronize();
            }
        }
        return nodes;
    }

    std::unique_ptr<ASTNode> parseStatement() {
        if (check(TokenType::SHOW))           return parseShowStatement();
        if (check(TokenType::DEFINE))         return parseDefineStatement();
        if (check(TokenType::DERIVE))         return parseDeriveStatement();
        if (check(TokenType::UNBIND))         return parseUnbindStatement();
        if (check(TokenType::STORE))          return parseStoreStatement();

        if (check(TokenType::IF))             return parseIfElseStatement();
        if (check(TokenType::WHILE))          return parseWhileStatement();
        if (check(TokenType::FOR))            return parseForStatement();
        if (check(TokenType::TRY))            return parseTryExceptThenStatement();
        if (check(TokenType::RETURN))         return parseReturnStatement();
        if (check(TokenType::THROW))          return parseThrowStatement();

        if (check(TokenType::HASH))           return parseJtmlElement();

        // Possibly other statements, or fallback to expression statement
        // For now, we do a basic "unexpected token" approach
        Token t = peek();
        throw std::runtime_error("Unexpected token '" + t.text +
            "' at line " + std::to_string(t.line) +
            ", column " + std::to_string(t.column));
    }

    std::unique_ptr<ExpressionStatementNode> parseExpression() {
        return parseLogicalOr();
    }

    std::unique_ptr<ExpressionStatementNode> parseLogicalOr() {
        auto left = parseLogicalAnd();

        while (match(TokenType::OR)) { // '||'
            Token op = previous();
            auto right = parseLogicalAnd();
            left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseLogicalAnd() {
        auto left = parseEquality();

        while (match(TokenType::AND)) { // '&&'
            Token op = previous();
            auto right = parseEquality();
            left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseEquality() {
        auto left = parseComparison();

        while (check(TokenType::EQ) || check(TokenType::NEQ)) {
            Token op = advance(); // consume == or !=
            auto right = parseComparison();
            left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseComparison() {
        auto left = parseAddition();

        while (true) {
            if (match(TokenType::LT) || match(TokenType::LTEQ) ||
                match(TokenType::GT) || match(TokenType::GTEQ)) {
                Token op = previous();
                auto right = parseAddition();
                left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
            } else {
                break;
            }
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseAddition() {
        auto left = parseMultiplication();

        while (true) {
            if (match(TokenType::PLUS) || match(TokenType::MINUS)) {
                Token op = previous();
                auto right = parseMultiplication();
                left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
            } else {
                break;
            }
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseMultiplication() {
        auto left = parseUnary();

        while (true) {
            if (match(TokenType::MULTIPLY) || match(TokenType::DIVIDE) || match(TokenType::MODULUS)) {
                Token op = previous();
                auto right = parseUnary();
                left = std::make_unique<BinaryExpressionStatementNode>(op, std::move(left), std::move(right));
            } else {
                break;
            }
        }
        return left;
    }

    std::unique_ptr<ExpressionStatementNode> parseUnary() {
        // handle unary operators like -x, !x
        if (match(TokenType::NOT) || match(TokenType::MINUS)) {
            Token op = previous();
            auto right = parseUnary();
            return std::make_unique<UnaryExpressionStatementNode>(op, std::move(right));
        }
        return parsePrimary();
    }

    std::unique_ptr<ExpressionStatementNode> parsePrimary() {
        if (match(TokenType::IDENTIFIER)) {
            Token name = previous();
            return std::make_unique<VariableExpressionStatementNode>(name);
        }
        if (match(TokenType::STRING_LITERAL)) {
            Token str = previous();
            return std::make_unique<StringLiteralExpressionStatementNode>(str);
        }
        if (matchNumberLiteral()) {
            // if you have a separate token type or if you interpret IDENTIFIER if numeric
            Token num = previous();
            return std::make_unique<NumberLiteralExpressionStatementNode>(num);
        }
        if (match(TokenType::LPAREN)) {
            auto expr = parseExpression();
            consume(TokenType::RPAREN, "Expected ')' after expression");
            return expr; // parenthesized
        }

        // if none matched, error
        Token t = peek();
        throw std::runtime_error("Unexpected token '" + t.text + "' in primary expression");
    }

    std::unique_ptr<ASTNode> parseDeriveStatement() {
        // grammar: derive IDENTIFIER (: type)? = expression STMT_TERMINATOR
        Token deriveTok = consume(TokenType::DERIVE, "Expected 'derive' keyword");
        Token idTok = consume(TokenType::IDENTIFIER, "Expected identifier after 'derive'");

        std::string declaredType;
        if (check(TokenType::COLON)) {
            advance(); // consume ':'
            Token typeTok = consume(TokenType::IDENTIFIER, "Expected type identifier after ':'");
            declaredType = typeTok.text;
        }

        consume(TokenType::ASSIGN, "Expected '=' in derive statement");

        auto expr = parseExpression();

        consume(TokenType::STMT_TERMINATOR, "Expected '\\\\' after derive statement");

        auto node = std::make_unique<DeriveStatementNode>();
        node->identifier = idTok.text;
        node->declaredType = declaredType;
        node->expression =std::move(expr);
        return node;
    }

    std::unique_ptr<ASTNode> parseUnbindStatement() {
        consume(TokenType::UNBIND, "Expected 'unbind'");
        Token idTok = consume(TokenType::IDENTIFIER, "Expected identifier after 'unbind'");
        consume(TokenType::STMT_TERMINATOR, "Expected '\\\\' after unbind statement");

        auto node = std::make_unique<UnbindStatementNode>();
        node->identifier = idTok.text;
        return node;
    }

    std::unique_ptr<ASTNode> parseStoreStatement() {
        consume(TokenType::STORE, "Expected 'store' keyword");
        consume(TokenType::LPAREN, "Expected '(' after 'store'");

        // scope can be MAIN or IDENTIFIER
        std::string scopeStr;
        if (check(TokenType::MAIN)) {
            scopeStr = "main";
            advance(); // consume 'main'
        } else if (check(TokenType::IDENTIFIER)) {
            scopeStr = peek().text;
            advance();
        } else {
            throw std::runtime_error("Expected 'main' or identifier in store(...)");
        }

        consume(TokenType::RPAREN, "Expected ')' after scope identifier");

        Token varTok = consume(TokenType::IDENTIFIER, "Expected variable name after store(...)");
        consume(TokenType::STMT_TERMINATOR, "Expected '\\\\' after store statement");

        auto node = std::make_unique<StoreStatementNode>();
        node->targetScope = scopeStr;
        node->variableName = varTok.text;
        return node;
    }


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
                recordError("Mismatched closing tag at line" + std::to_string(m_line) + ": " + closeTag.text + " != " + openTag.text);
        }
        return elem;
    }

private:
    std::vector<Token> m_tokens;
    size_t m_pos;
    int m_line;
    int m_column;

    std::vector<std::string> m_errors;

    void parseJtmlBody(JtmlElementNode& elem) {
        // optional attributes
        if (lookAheadIsAttribute()) {
            parseAttributes(elem.attributes);
            match(TokenType::STMT_TERMINATOR);
        }
        // parse zero or more content items
        while (!check(TokenType::BACKSLASH_HASH) && !check(TokenType::END_OF_FILE)) {
            auto stmt = parseStatement(); // or parseContentItem
            if (stmt) {
                elem.content.push_back(std::move(stmt));
            }
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
        try {
            if (check(TokenType::SHOW)) {
                return parseShowStatement();
            } else if (check(TokenType::DEFINE)) {
                return parseDefineStatement();
            } else if (check(TokenType::HASH)) {
                return parseJtmlElement();
            }
            throw std::runtime_error("Unexpected token '" + peek().text + "' in content item.");
        } catch (const std::runtime_error& e) {
            recordError(e.what());
            synchronize();
            return nullptr;
        }
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

    std::unique_ptr<ASTNode> parseIfElseStatement() {
        consume(TokenType::IF, "Expected 'if'");
        consume(TokenType::LPAREN, "Expected '(' after 'if'");
        // parse condition as single token or string
        Token condTok = peek();
        if (condTok.type != TokenType::IDENTIFIER && condTok.type != TokenType::STRING_LITERAL) {
            throw std::runtime_error("Expected condition expression after '(' in if");
        }
        advance();
        consume(TokenType::RPAREN, "Expected ')' after condition");

        // Now we expect a BACKSLASH, parse statements until next lone backslash or else
        // We'll store them in IfStatementNode->thenStatements
        auto ifNode = std::make_unique<IfStatementNode>();
        ifNode->condition = condTok.text;

        // parse block statements
        parseBlockStatementList(ifNode->thenStatements);

        // optional else
        if (check(TokenType::ELSE)) {
            advance(); // consume else
            parseBlockStatementList(ifNode->elseStatements);
        }

        return ifNode;
    }

    // a helper
    void parseBlockStatementList(std::vector<std::unique_ptr<ASTNode>>& stmts) {
        consume(TokenType::STMT_TERMINATOR, "Expected '\\' to start block");
        // read statements until we see a line with just '\\' or an END
        while (!check(TokenType::STMT_TERMINATOR) && !check(TokenType::END_OF_FILE)) {
            auto s = parseStatement();
            if (s) { stmts.push_back(std::move(s)); }
        }
        consume(TokenType::STMT_TERMINATOR, "Expected '\\' to end block");
    }

    std::unique_ptr<ASTNode> parseForStatement() {
    
    }
    
    std::unique_ptr<ASTNode> parseWhileStatement() {
    
    }

    std::unique_ptr<ASTNode> parseTryExceptThenStatement() {

    }

    std::unique_ptr<ASTNode> parseReturnStatement() {

    }

    std::unique_ptr<ASTNode> parseThrowStatement() {

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
        auto& badToken = peek();
        std::string fullMsg = errMsg + " (line " + std::to_string(badToken.line) +
            ", col " + std::to_string(badToken.column) + "). Found: '" + badToken.text + "'";
        recordError(fullMsg);
        synchronize()
    }

    Token advance() {
        if (!isAtEnd()) m_pos++;
        return m_tokens[m_pos - 1];
    }

    Token previous() const {
        if (m_pos == 0) {
            throw std::runtime_error("No previous token exists.");
        }
        return m_tokens[m_pos - 1];
    }

    bool isAtEnd() const {
        return peek().type == TokenType::END_OF_FILE;
    }

    const Token& peek() const {
        return m_tokens[m_pos];
    }

    void recordError(const std::string& message) {
        m_errors.push_back(message);
    }

    void synchronize() {
        while (!isAtEnd()) {
            switch (peek().type) {
                case TokenType::STMT_TERMINATOR:
                case TokenType::BACKSLASH_HASH:
                    advance();
                    return;
                default:
                    advance();
            }
        }
    }
};

