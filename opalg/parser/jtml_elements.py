from opalg.compiler.ast_nodes import (
    JTMLElementNode, # your python Node
    IdentifierNode,
    # plus any statement or expression nodes you might embed
)
from opalg.lexer.lexer import tokens

def p_jtml_body(p):
    '''jtml_body : jtml_attributes BACKSLASH jtml_content_item_list
                 | jtml_attributes
                 | jtml_content_item_list
                 | jtml_empty'''
    # Cases:
    # 1) attributes + \\ + content
    # 2) just attributes
    # 3) just content
    # 4) empty
    if len(p) == 4:
        attributes = p[1] if p[1] else {}
        content = p[3] if p[3] else []
    elif len(p) == 2:
        if p[1] is None:
            attributes = {}
            content = []
        elif isinstance(p[1], dict):
            attributes = p[1]
            content = []
        else:
            attributes = {}
            content = p[1]
    else:
        attributes = {}
        content = []
    p[0] = (attributes, content)

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
    p[0] = {p[1]: p[3]}

def p_closing_tag(p):
    '''closing_tag : HASH
                   | HASH IDENTIFIER'''
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_jtml_content_item_list(p):
    '''jtml_content_item_list : jtml_content_item_list jtml_content_item
                              | jtml_content_item'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_jtml_content_item(p):
    '''jtml_content_item : statement BACKSLASH
                         | expression BACKSLASH
                         | dynamic_content BACKSLASH'''
    # For now, content can be any statement or expression from opalg,
    # or a #(...) dynamic expression
    p[0] = p[1]

def p_dynamic_content(p):
    '''dynamic_content : HASH LPAREN IDENTIFIER RPAREN'''
    # example for #(...) syntax
    # you can store it as a custom AST node
    p[0] = DynamicExpressionNode(IdentifierNode(p[3]))

def p_jtml_empty(p):
    'jtml_empty :'
    p[0] = None

def p_jtml_element(p):
    '''jtml_element : HASH IDENTIFIER jtml_body closing_tag'''
    tag_name = p[2]
    attributes, content = p[3] if p[3] else ({}, [])
    closing_tag = p[4]
    if closing_tag and closing_tag != tag_name:
        raise SyntaxError(f"Closing tag '{closing_tag}' does not match opening tag '{tag_name}'")

    # Just store in a Python-level JTMLElementNode:
    p[0] = JTMLElementNode(tag_name, attributes, content)
