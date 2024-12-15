# lexer.py

import ply.lex as lex

# Reserved words mapped to their token types
reserved = {
    'define': 'DEFINE',
    'function': 'FUNCTION',
    'async': 'ASYNC',
    'return': 'RETURN',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'try': 'TRY',
    'catch': 'CATCH',
    'finally': 'FINALLY',
    'throw': 'THROW',
    'int': 'TYPE',
    'float': 'TYPE',
    'string': 'TYPE',
    'bool': 'TYPE',
    'void': 'TYPE',
    'show': 'SHOW',
    'save': 'SAVE',
    'delete': 'DELETE',
    'true': 'BOOL_LITERAL',
    'false': 'BOOL_LITERAL',
    'const': 'CONST',
    'class': 'CLASS',
    'connect': 'CONNECT',
    'as': 'AS',
    'db': 'DB',
    'query': 'QUERY',
    'transaction': 'TRANSACTION',
    'commit': 'COMMIT',
    'rollback': 'ROLLBACK',
    'derive_public_key': 'DERIVE_PUBLIC_KEY',
    'generate_key': 'GENERATE_KEY',
    'qubit': 'QUBIT',
    'apply': 'APPLY',
    'measure': 'MEASURE',
    'encrypt': 'ENCRYPT',
    'decrypt': 'DECRYPT',
    'sign': 'SIGN',
    'verify': 'VERIFY',
    'in': 'IN',
    'to': 'TO',
    'on': 'ON',
    'size': 'SIZE',
    'from': 'FROM',
    'data': 'DATA',
    'with': 'WITH',
    'key': 'KEY',
    'algorithm': 'ALGORITHM',
    'signature': 'SIGNATURE',
    'await': "AWAIT",
    'type': 'TYPE'
}

tokens = [
    'LPAREN',
    'RPAREN',
    'IDENTIFIER',
    'INT_LITERAL',
    'FLOAT_LITERAL',
    'STRING_LITERAL',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'LESS',
    'GREATER',
    'LEQ',
    'GEQ',
    'EQEQ',
    'NEQ',
    'COLON',
    'COMMA',
    'PLUSEQ',
    'DOT',
    'OR',
    'AND',
    'NOT',
    'HASH',
    'BACKSLASH'
] + list(set(reserved.values()))  # Include all reserved token types except duplicates

# Regular expressions for simple tokens
t_PLUS       = r'\+'
t_MINUS      = r'-'
t_TIMES      = r'\*'
t_DIVIDE     = r'/'
t_EQUALS     = r'='
t_LESS       = r'<'
t_GREATER    = r'>'
t_LEQ        = r'<='
t_GEQ        = r'>='
t_EQEQ       = r'=='
t_NEQ        = r'!='
t_COLON      = r':'
t_COMMA      = r','
t_PLUSEQ     = r'\+='
t_DOT        = r'\.'
t_OR         = r'\|\|'
t_AND        = r'&&'
t_NOT        = r'!'
t_HASH       = r'\#'
t_LPAREN     = r'\('
t_RPAREN     = r'\)'
t_BACKSLASH = r'\\\\'

# Comments
def t_COMMENT(t):
    r'//.*'
    pass  # No return value. Token discarded.

def t_IDENTIFIER(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Check for reserved words
    if t.type == 'BOOL_LITERAL':
        t.value = True if t.value == 'true' else False
    return t

def t_FLOAT_LITERAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LITERAL(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STRING_LITERAL(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}, column {find_column(t)}")
    t.lexer.skip(1)

def find_column(token):
    input_data = token.lexer.lexdata
    start_of_line = input_data.rfind('\n', 0, token.lexpos) + 1
    return token.lexpos - start_of_line + 1

# Build the lexer
lexer = lex.lex()
