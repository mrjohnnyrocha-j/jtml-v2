# parser/error_handling.py

from compiler.ast_nodes import (
    TryCatchFinallyNode, BlockNode, IdentifierNode
)
from parser.parser import tokens

def p_try_catch_finally_try(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, None)

def p_try_catch_finally_try_catch(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[7]), BlockNode(p[10]), None)

def p_try_catch_finally_try_catch_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt BACKSLASH FINALLY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[7]), BlockNode(p[10]), BlockNode(p[14]))

def p_try_catch_finally_try_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH FINALLY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, BlockNode(p[7]))
