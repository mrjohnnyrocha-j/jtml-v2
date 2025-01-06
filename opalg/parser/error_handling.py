# parser/error_handling.py

from opalg.compiler.ast_nodes import (
    TryCatchFinallyNode, BlockNode, IdentifierNode
)
from opalg.lexer.lexer import tokens

def p_try_catch_finally_try(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt '''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, None)

def p_try_catch_finally_try_catch(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt '''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[6]), BlockNode(p[9]), None)

def p_try_catch_finally_try_catch_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt  FINALLY BACKSLASH statement_list_opt '''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[6]), BlockNode(p[9]), BlockNode(p[12]))

def p_try_catch_finally_try_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt FINALLY BACKSLASH statement_list_opt '''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, BlockNode(p[6]))
