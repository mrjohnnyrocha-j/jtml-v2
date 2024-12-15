# parser/parser.py

import ply.yacc as yacc
from lexer.lexer import tokens
from compiler.ast_nodes import (
    ProgramNode, BlockNode,
    VariableDeclarationNode, FunctionDeclarationNode, ParameterNode,
    ClassDeclarationNode, ForStatementNode, IfStatementNode, WhileStatementNode,
    TryCatchFinallyNode, ThrowStatementNode, ShowStatementNode, SaveStatementNode,
    DeleteStatementNode, ReturnStatementNode, ExpressionStatementNode,
    ConnectStatementNode, QueryStatementNode, TransactionNode,
    QuantumDefineQubitNode, QuantumApplyNode, QuantumMeasureNode,
    CryptoGenerateKeyNode, CryptoDerivePublicKeyNode, CryptoEncryptNode, CryptoDecryptNode,
    CryptoHashNode, CryptoSignNode, CryptoVerifyNode,
    JTMLElementNode,
    BinaryOperationNode, UnaryOperationNode, NumberLiteralNode, StringLiteralNode, BoolLiteralNode,
    IdentifierNode, FunctionCallNode, MemberAccessNode, AwaitExpressionNode,
    TypeNode, CustomType, VoidType, IntType, FloatType, StringType, BoolType
)

# Import all grammar rule modules to register their p_* functions
from parser.control_flow import *
from parser.crypto import *
from parser.database import *
from parser.error_handling import *
from parser.expressions import *
from parser.functions_and_classes import *
from parser.jtml_elements import *
from parser.quantum import *
from parser.statements import *
from parser.types_and_parameters import *
from parser.variables_and_constants import *

import jtmlparser  # Import the C++ parser module via pybind11

# Define the start symbol
start = 'program'

# Operator precedence
precedence = (
    ('left', 'BACKSLASH'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LESS', 'LEQ', 'GREATER', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'DOT'),
    ('right', 'ELSE'),
)

def p_empty(p):
    'empty :'
    p[0] = None

def p_program(p):
    '''program : item_list
               | item_list BACKSLASH
               | empty'''
    p[0] = ProgramNode(p[1] if p[1] else [])

def p_item_list(p):
    '''item_list : item_list item
                 | item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_item(p):
    '''item : statement BACKSLASH
            | jtml_element'''
    p[0] = p[1]

# Optional statement list
def p_statement_list_opt(p):
    '''statement_list_opt : statement_list 
                          | jtml_element
                          | empty'''
    p[0] = p[1] if p[1] else []

# Statements must end with '\\'
def p_statement_list_single(p):
    '''statement_list : statement BACKSLASH'''
    p[0] = [p[1]]

def p_statement_list_multiple(p):
    '''statement_list : statement BACKSLASH statement_list'''
    p[0] = [p[1]] + p[3]

def p_statement(p):
    '''statement : variable_declaration
                 | const_declaration
                 | show_statement
                 | save_statement
                 | delete_statement
                 | return_statement
                 | throw_statement
                 | connect_statement
                 | query_statement
                 | crypto_statement
                 | quantum_statement
                 | expression_statement
                 | function_declaration
                 | class_declaration
                 | if_statement
                 | while_statement
                 | for_statement
                 | try_catch_finally
                 | transaction_block'''
    p[0] = p[1]

def p_jtml_element(p):
    '''jtml_element : HASH IDENTIFIER jtml_body closing_tag'''
    tag_name = p[2]
    attributes = p[3][0] if p[3] else {}
    content = p[3][1] if p[3] else []
    closing_tag = p[4]

    if closing_tag and closing_tag != tag_name:
        raise SyntaxError(f"Closing tag '{closing_tag}' does not match opening tag '{tag_name}'")

    # Serialize the JTML element into a string format for the C++ parser
    jtml_string = f"#{tag_name}"
    if attributes:
        attrs = ", ".join([f'{k}:"{v}"' for k, v in attributes.items()])
        jtml_string += f' {attrs}'
    jtml_string += " \\\\"

    for stmt in content:
        # Serialize each statement based on its type
        if isinstance(stmt, ShowStatementNode):
            jtml_string += f'show "{stmt.value}"\\\\'
        elif isinstance(stmt, VariableDeclarationNode):
            var_type = f": {stmt.var_type}" if stmt.var_type else ""
            jtml_string += f'define {stmt.name}{var_type} = {serialize_expression(stmt.value)}\\\\'
        # ... handle other statement types similarly
        else:
            # For unhandled statement types, raise an error or implement serialization
            raise NotImplementedError(f"Serialization for {type(stmt)} is not implemented.")

    jtml_string += f"#{closing_tag if closing_tag else tag_name}"

    # Use the C++ parser to parse the JTML element
    parser = jtmlparser.ParserWrapper()
    try:
        ast_node = parser.parse(jtml_string)
    except Exception as e:
        raise SyntaxError(f"Error parsing JTML element '{tag_name}': {e}")

    p[0] = ast_node

def serialize_expression(expr):
    """Helper function to serialize Python AST expressions to strings."""
    if isinstance(expr, BinaryOperationNode):
        return f"{serialize_expression(expr.left)} {expr.op} {serialize_expression(expr.right)}"
    elif isinstance(expr, UnaryOperationNode):
        return f"{expr.op}{serialize_expression(expr.operand)}"
    elif isinstance(expr, NumberLiteralNode):
        return str(expr.value)
    elif isinstance(expr, StringLiteralNode):
        return f'"{expr.value}"'
    elif isinstance(expr, IdentifierNode):
        return expr.name
    else:
        raise NotImplementedError(f"Serialization for {type(expr)} is not implemented.")

# Error handling
def p_error(p):
    if p:
        column = find_column(p)
        line = p.lineno
        lines = p.lexer.lexdata.split('\n')
        error_line = lines[line - 1] if line <= len(lines) else ''
        message = f"Syntax error at line {line}, column {column}: Unexpected token '{p.value}'\n"
        message += f"    {error_line}\n"
        message += "    " + " "*(column-1) + "^"
        raise SyntaxError(message)
    else:
        raise SyntaxError("Syntax error at EOF")

def find_column(token):
    input_data = token.lexer.lexdata
    start_of_line = input_data.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - start_of_line + 1

# Build the parser
parser = yacc.yacc(debug=True, write_tables=False)
