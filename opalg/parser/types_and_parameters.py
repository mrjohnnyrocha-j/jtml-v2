# parser/types_and_parameters.py

from opalg.compiler.ast_nodes import (
    TypeNode, IntType, FloatType, StringType, BoolType, VoidType, CustomType,
    ParameterNode, IdentifierNode
)
from opalg.lexer.lexer import tokens

def p_type(p):
    '''type : type_name
            | type_name generic_arguments'''
    if len(p) == 2:
        tname = p[1]
        primitive_map = {
            'int': IntType(),
            'float': FloatType(),
            'string': StringType(),
            'bool': BoolType(),
            'void': VoidType(),
        }
        p[0] = primitive_map.get(tname, CustomType(tname))
    else:
        p[0] = TypeNode(p[1], p[2])

def p_type_name(p):
    '''type_name : IDENTIFIER
                 | TYPE'''
    p[0] = p[1]

def p_type_spec(p):
    '''type_spec : TYPE COLON STRING_LITERAL'''
    p[0] = {'type': p[3]}

def p_param_list_opt(p):
    '''param_list_opt : COMMA param_list
                      | empty'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = {}

def p_param_list_multiple(p):
    '''param_list : param_list COMMA param'''
    p[0] = p[1]
    p[0].update(p[3])

def p_param_list_single(p):
    '''param_list : param'''
    p[0] = p[1]

def p_param(p):
    '''
    param : IDENTIFIER COLON value
          | DB COLON value
          | SIZE COLON value
          | ALGORITHM COLON value
          | KEY COLON value
          | DATA COLON value
          | SIGNATURE COLON value
    '''
    if p.slice[1].type == 'DB':
        key = 'db'
    elif p.slice[1].type == 'SIZE':
        key = 'size'
    elif p.slice[1].type == 'ALGORITHM':
        key = 'algorithm'
    elif p.slice[1].type == 'KEY':
        key = 'key'
    elif p.slice[1].type == 'DATA':
        key = 'data'
    elif p.slice[1].type == 'SIGNATURE':
        key = 'signature'
    else:
        key = p[1]
    p[0] = {key: p[3]}

def p_value(p):
    '''value : STRING_LITERAL
             | INT_LITERAL'''
    p[0] = p[1]

def p_generic_arguments(p):
    '''generic_arguments : LESS type_list GREATER'''
    p[0] = p[2]

def p_type_list_single(p):
    '''type_list : type'''
    p[0] = [p[1]]

def p_type_list_multiple(p):
    '''type_list : type_list COMMA type'''
    p[0] = p[1] + [p[3]]

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

def p_argument_list(p):
    '''argument_list : expression
                     | argument_list COMMA expression
                     | empty'''
    if p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_identifier_list_single(p):
    '''identifier_list : IDENTIFIER'''
    p[0] = [IdentifierNode(p[1])]

def p_identifier_list_multiple(p):
    '''identifier_list : identifier_list COMMA IDENTIFIER'''
    p[0] = p[1] + [IdentifierNode(p[3])]