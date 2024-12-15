# parser/functions_and_classes.py

from compiler.ast_nodes import (
    FunctionDeclarationNode, ParameterNode, BlockNode, IdentifierNode,
    TypeNode, VoidType, IntType, FloatType, StringType, BoolType, CustomType, ReturnStatementNode, ThrowStatementNode, ClassDeclarationNode
)
from lexer.lexer import tokens
from parser.utils import has_return_statement

def p_function_declaration(p):
    '''function_declaration : function_head BACKSLASH function_body'''
    name, params, rtype, async_flag = p[1]
    body = p[3]
    print(f"Parsed function '{name}' with body: {body.statements}")  # Debug print
    if not body.statements:
        raise SyntaxError(f"Function '{name}' must have at least one return statement.")
    if not has_return_statement(body.statements):
        raise SyntaxError(f"Function '{name}' must have at least one return statement.")
    p[0] = FunctionDeclarationNode(name, params, rtype, body, async_function=async_flag)


def p_function_head_async(p):
    '''function_head : ASYNC FUNCTION IDENTIFIER parameter_list function_return_type'''
    p[0] = (p[3], p[4], p[5], True)

def p_function_head(p):
    '''function_head : FUNCTION IDENTIFIER parameter_list function_return_type'''
    p[0] = (p[2], p[3], p[4], False)
    
def p_function_body(p):
    '''function_body : statement_list'''
    p[0] = BlockNode(p[1])

def p_parameter_list(p):
    '''parameter_list : LPAREN parameters_opt RPAREN'''
    p[0] = p[2]

def p_parameters_opt(p):
    '''parameters_opt : parameters
                      | empty'''
    p[0] = p[1] if p[1] else []

def p_parameters_multiple(p):
    '''parameters : parameters COMMA parameter'''
    p[0] = p[1] + [p[3]]

def p_parameters_single(p):
    '''parameters : parameter'''
    p[0] = [p[1]]

def p_parameter_def(p):
    '''parameter : IDENTIFIER COLON type'''
    p[0] = ParameterNode(p[1], p[3])

def p_function_return_type_typed(p):
    '''function_return_type : COLON type'''
    p[0] = p[2]

def p_function_return_type_void(p):
    '''function_return_type : empty'''
    p[0] = VoidType()
    
def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER BACKSLASH statement_list_opt '''
    p[0] = ClassDeclarationNode(p[2], p[4])
