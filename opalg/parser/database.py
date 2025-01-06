# parser/database.py

from opalg.compiler.ast_nodes import (
    ConnectStatementNode, QueryStatementNode, TransactionNode,
    BlockNode, IdentifierNode
)
from opalg.lexer.lexer import tokens

def p_connect_statement(p):
    '''connect_statement : CONNECT TO STRING_LITERAL AS IDENTIFIER'''
    p[0] = ConnectStatementNode(p[3], p[5])

def p_query_statement(p):
    '''query_statement : QUERY ON IDENTIFIER COLON STRING_LITERAL'''
    p[0] = QueryStatementNode(p[3], p[5])

def p_transaction_block(p):
    '''transaction_block : TRANSACTION ON IDENTIFIER BACKSLASH statement_list_opt BACKSLASH commit_rollback BACKSLASH'''
    p[0] = TransactionNode(p[3], BlockNode(p[5]), p[7])

def p_commit_rollback(p):
    '''commit_rollback : COMMIT
                       | ROLLBACK'''
    p[0] = p[1]
