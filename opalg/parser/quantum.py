# parser/quantum.py

from opalg.compiler.ast_nodes import (
    QuantumDefineQubitNode, QuantumApplyNode, QuantumMeasureNode,
    BlockNode, IdentifierNode, VariableDeclarationNode
)
from opalg.lexer.lexer import tokens

def p_quantum_statement(p):
    '''quantum_statement : quantum_define_qubit
                         | quantum_apply
                         | quantum_measure_expr'''
    p[0] = p[1]

def p_quantum_define_qubit(p):
    '''quantum_define_qubit : DEFINE IDENTIFIER AS QUBIT'''
    p[0] = QuantumDefineQubitNode(p[2])

def p_quantum_apply(p):
    '''quantum_apply : APPLY IDENTIFIER ON identifier_list'''
    p[0] = QuantumApplyNode(p[2], p[4])

def p_quantum_measure_expr(p):
    '''quantum_measure_expr : DEFINE IDENTIFIER EQUALS MEASURE IDENTIFIER'''
    var_name = p[2]
    qubit_name = p[5]
    p[0] = VariableDeclarationNode(var_name, None, QuantumMeasureNode(var_name, qubit_name))
