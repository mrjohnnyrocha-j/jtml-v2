# parser/control_flow.py

from compiler.ast_nodes import IfStatementNode, WhileStatementNode, ForStatementNode, BinaryOperationNode, BlockNode, IdentifierNode, NumberLiteralNode
from parser.parser import tokens

def p_if_statement_with_else(p):
    '''if_statement : IF LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH ELSE BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = IfStatementNode(p[3], BlockNode(p[6]), BlockNode(p[10]))

def p_if_statement_no_else(p):
    '''if_statement : IF LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = IfStatementNode(p[3], BlockNode(p[6]), None)

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = WhileStatementNode(p[3], BlockNode(p[6]))

def p_for_statement(p):
    '''for_statement : FOR LPAREN IDENTIFIER IN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = ForStatementNode(p[3], p[5], BlockNode(p[8]))
