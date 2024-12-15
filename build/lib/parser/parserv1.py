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
import parser.control_flow
import parser.crypto
import parser.database
import parser.error_handling
import parser.expressions
import parser.functions_and_classes
import parser.jtml_elements
import parser.quantum
import parser.statements
import parser.types_and_parameters
import parser.variables_and_constants

# Define the start symbol
start = 'program'

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('left', 'EQEQ', 'NEQ'),
    ('left', 'LESS', 'LEQ', 'GREATER', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'UMINUS'),
    ('left', 'DOT'),
    ('right', 'ELSE')
)

def p_empty(p):
    'empty :'
    p[0] = None

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
parser = yacc.yacc(debug=True)
