# parser/expressions.py

from compiler.ast_nodes import (
    BinaryOperationNode, UnaryOperationNode, BoolLiteralNode, StringLiteralNode,
    NumberLiteralNode, IdentifierNode, FunctionCallNode, MemberAccessNode,
    AwaitExpressionNode
)
from parser.parser import tokens

def p_expression(p):
    '''expression : assignment_expression'''
    p[0] = p[1]

def p_assignment_expression_plus_eq(p):
    '''assignment_expression : IDENTIFIER PLUSEQ expression'''
    p[0] = BinaryOperationNode(IdentifierNode(p[1]), '+=', p[3])

def p_assignment_expression_assign_only(p):
    '''assignment_expression : IDENTIFIER EQUALS expression'''
    p[0] = BinaryOperationNode(IdentifierNode(p[1]), '=', p[3])

def p_assignment_expression_logic(p):
    '''assignment_expression : logical_or_expression'''
    p[0] = p[1]

def p_logical_or_expression(p):
    '''logical_or_expression : logical_or_expression OR logical_and_expression
                             | logical_and_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], '||', p[3])
    else:
        p[0] = p[1]

def p_logical_and_expression(p):
    '''logical_and_expression : logical_and_expression AND equality_expression
                              | equality_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], '&&', p[3])
    else:
        p[0] = p[1]

def p_equality_expression(p):
    '''equality_expression : equality_expression EQEQ relational_expression
                           | equality_expression NEQ relational_expression
                           | relational_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_relational_expression(p):
    '''relational_expression : relational_expression LESS additive_expression
                             | relational_expression GREATER additive_expression
                             | relational_expression LEQ additive_expression
                             | relational_expression GEQ additive_expression
                             | additive_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_additive_expression(p):
    '''additive_expression : additive_expression PLUS multiplicative_expression
                           | additive_expression MINUS multiplicative_expression
                           | multiplicative_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_multiplicative_expression(p):
    '''multiplicative_expression : multiplicative_expression TIMES unary_expression
                                 | multiplicative_expression DIVIDE unary_expression
                                 | unary_expression'''
    if len(p) == 4:
        p[0] = BinaryOperationNode(p[1], p[2], p[3])
    else:
        p[0] = p[1]

def p_unary_expression_uminus(p):
    '''unary_expression : MINUS unary_expression %prec UMINUS'''
    p[0] = UnaryOperationNode('-', p[2])

def p_unary_expression_not(p):
    '''unary_expression : NOT unary_expression'''
    p[0] = UnaryOperationNode('!', p[2])

def p_unary_expression_await(p):
    '''unary_expression : AWAIT unary_expression'''
    p[0] = AwaitExpressionNode(p[2])

def p_unary_expression_postfix(p):
    '''unary_expression : postfix_expression'''
    p[0] = p[1]

def p_postfix_expression_member(p):
    '''postfix_expression : postfix_expression DOT IDENTIFIER'''
    p[0] = MemberAccessNode(p[1], p[3])

def p_postfix_expression_call(p):
    '''postfix_expression : postfix_expression LPAREN argument_list RPAREN'''
    p[0] = FunctionCallNode(p[1], p[3])

def p_postfix_expression_primary(p):
    '''postfix_expression : primary_expression'''
    p[0] = p[1]

def p_primary_expression_literal(p):
    '''primary_expression : INT_LITERAL
                          | FLOAT_LITERAL
                          | STRING_LITERAL
                          | BOOL_LITERAL'''
    val = p[1]
    if isinstance(val, bool):
        p[0] = BoolLiteralNode(val)
    elif isinstance(val, str):
        p[0] = StringLiteralNode(val)
    else:
        p[0] = NumberLiteralNode(val)

def p_primary_expression_identifier(p):
    '''primary_expression : IDENTIFIER'''
    p[0] = IdentifierNode(p[1])

def p_primary_expression_paren(p):
    '''primary_expression : LPAREN expression RPAREN'''
    p[0] = p[2]
