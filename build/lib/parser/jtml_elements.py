# parser/jtml_elements.py

from compiler.ast_nodes import (
    JTMLElementNode, StringLiteralNode, BlockNode, IdentifierNode, VariableDeclarationNode
)
from parser.parser import tokens

def p_jtml_element(p):
    '''jtml_element : HASH IDENTIFIER jtml_attributes_opt jtml_content_opt HASH closing_tag_opt BACKSLASH'''
    tag_name = p[2]
    attributes = p[3] if p[3] else {}
    content = p[4] if p[4] else []
    closing_tag = p[6]
    if closing_tag and closing_tag != tag_name:
        raise SyntaxError(f"Closing tag '{closing_tag}' does not match opening tag '{tag_name}'")
    p[0] = JTMLElementNode(tag_name, attributes, content)

def p_jtml_attributes_opt(p):
    '''jtml_attributes_opt : jtml_attributes
                           | empty'''
    p[0] = p[1] if p[1] else {}

def p_jtml_attributes(p):
    '''jtml_attributes : jtml_attributes attribute
                       | attribute'''
    if len(p) == 3:
        d = dict(p[1])
        d.update(p[2])
        p[0] = d
    else:
        p[0] = p[1]

def p_attribute(p):
    '''attribute : IDENTIFIER COLON STRING_LITERAL'''
    p[0] = {p[1]: StringLiteralNode(p[3])}

def p_jtml_content_opt(p):
    '''jtml_content_opt : jtml_content
                        | empty'''
    p[0] = p[1] if p[1] else []

def p_jtml_content(p):
    '''jtml_content : jtml_content content_item
                    | content_item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_content_item_statement(p):
    '''content_item : statement'''
    p[0] = p[1]

def p_content_item_string(p):
    '''content_item : STRING_LITERAL'''
    p[0] = StringLiteralNode(p[1])

def p_closing_tag_opt(p):
    '''closing_tag_opt : IDENTIFIER
                       | empty'''
    p[0] = p[1] if p[1] else None
