# parser/statements.py

from compiler.ast_nodes import (
    ExpressionStatementNode
)
from parser.parser import tokens

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = ExpressionStatementNode(p[1])
