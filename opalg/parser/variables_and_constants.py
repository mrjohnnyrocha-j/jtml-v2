# parser/variables_and_constants.py

from opalg.compiler.ast_nodes import (
    VariableDeclarationNode, QuantumMeasureNode, IdentifierNode,
    NumberLiteralNode, StringLiteralNode, BoolLiteralNode
)
from opalg.lexer.lexer import tokens

def p_variable_declaration_typed(p):
    '''variable_declaration : DEFINE IDENTIFIER COLON type EQUALS expression'''
    if isinstance(p[6], QuantumMeasureNode):
        p[6].var_name = p[2]
    p[0] = VariableDeclarationNode(p[2], p[4], p[6])

def p_variable_declaration_untyped(p):
    '''variable_declaration : DEFINE IDENTIFIER EQUALS expression'''
    if isinstance(p[4], QuantumMeasureNode):
        p[4].var_name = p[2]
    p[0] = VariableDeclarationNode(p[2], None, p[4])

def p_const_declaration_typed(p):
    '''const_declaration : CONST IDENTIFIER COLON type EQUALS expression'''
    if isinstance(p[6], QuantumMeasureNode):
        p[6].var_name = p[2]
    p[0] = VariableDeclarationNode(p[2], p[4], p[6], const=True)

def p_const_declaration_untyped(p):
    '''const_declaration : CONST IDENTIFIER EQUALS expression'''
    if isinstance(p[4], QuantumMeasureNode):
        p[4].var_name = p[2]
    p[0] = VariableDeclarationNode(p[2], None, p[4], const=True)
