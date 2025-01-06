# parser/statements.py

from opalg.compiler.ast_nodes import (
    ReturnStatementNode, ThrowStatementNode,
    ExpressionStatementNode, ShowStatementNode, SaveStatementNode, DeleteStatementNode
)
from opalg.lexer.lexer import tokens

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ExpressionStatementNode(p[1])

def p_show_statement(p):
    '''show_statement : SHOW expression'''
    p[0] = ShowStatementNode(p[2])

def p_save_statement(p):
    '''save_statement : SAVE IDENTIFIER EQUALS expression'''
    p[0] = SaveStatementNode(p[2], p[4])

def p_delete_statement(p):
    '''delete_statement : DELETE IDENTIFIER'''
    p[0] = DeleteStatementNode(p[2])
    
def p_throw_statement(p):
    '''throw_statement : THROW expression'''
    p[0] = ThrowStatementNode(p[2])

def p_return_statement_expr(p):
    '''return_statement : RETURN expression'''
    p[0] = ReturnStatementNode(p[2])

def p_return_statement_none(p):
    '''return_statement : RETURN'''
    p[0] = ReturnStatementNode(None)