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

# The start symbol
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

# ----------------------
# Statement Block
# ----------------------

# Program: optional list of statements
def p_program(p):
    '''program : statement_list_opt'''
    p[0] = ProgramNode(p[1] if p[1] else [])

# Optional statement list
def p_statement_list_opt(p):
    '''statement_list_opt : statement_list 
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
                 | transaction_block
                 | jtml_element'''
    p[0] = p[1]

# ----------------------
# Variables and Constants
# ----------------------
def p_show_statement(p):
    '''show_statement : SHOW expression'''
    p[0] = ShowStatementNode(p[2])

def p_save_statement(p):
    '''save_statement : SAVE IDENTIFIER EQUALS expression'''
    p[0] = SaveStatementNode(p[2], p[4])

def p_delete_statement(p):
    '''delete_statement : DELETE IDENTIFIER'''
    p[0] = DeleteStatementNode(p[2])

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


# ----------------------
# Functions and Classes
# ----------------------
def p_function_declaration(p):
    '''function_declaration : function_head BACKSLASH statement_list_opt BACKSLASH'''
    name, params, rtype, async_flag = p[1]
    p[0] = FunctionDeclarationNode(name, params, rtype, BlockNode(p[3]), async_function=async_flag)

def p_function_head_async(p):
    '''function_head : ASYNC FUNCTION IDENTIFIER parameter_list function_return_type'''
    p[0] = (p[3], p[4], p[5], True)

def p_function_head(p):
    '''function_head : FUNCTION IDENTIFIER parameter_list function_return_type'''
    p[0] = (p[2], p[3], p[4], False)

def p_class_declaration(p):
    '''class_declaration : CLASS IDENTIFIER BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = ClassDeclarationNode(p[2], p[4])

# ----------------------
# Control Flow
# ----------------------
def p_if_statement_else(p):
    '''if_statement : IF LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH ELSE BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = IfStatementNode(p[3], BlockNode(p[6]), BlockNode(p[10]))

def p_if_statement_no_else(p):
    '''if_statement : IF LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = IfStatementNode(p[3], BlockNode(p[6]), None)

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = WhileStatementNode(p[3], BlockNode(p[6]))

def p_for_statement(p):
    '''for_statement : FOR LPAREN IDENTIFIER IN expression RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = ForStatementNode(p[3], p[5], BlockNode(p[8]))

def p_try_catch_finally_try(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, None)

def p_try_catch_finally_try_catch(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[7]), BlockNode(p[10]), None)

def p_try_catch_finally_try_catch_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH CATCH LPAREN IDENTIFIER RPAREN BACKSLASH statement_list_opt BACKSLASH FINALLY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), IdentifierNode(p[7]), BlockNode(p[10]), BlockNode(p[14]))

def p_try_catch_finally_try_finally(p):
    '''try_catch_finally : TRY BACKSLASH statement_list_opt BACKSLASH FINALLY BACKSLASH statement_list_opt BACKSLASH'''
    p[0] = TryCatchFinallyNode(BlockNode(p[3]), None, None, BlockNode(p[7]))

def p_throw_statement(p):
    '''throw_statement : THROW expression'''
    p[0] = ThrowStatementNode(p[2])

def p_return_statement_expr(p):
    '''return_statement : RETURN expression'''
    p[0] = ReturnStatementNode(p[2])

def p_return_statement_none(p):
    '''return_statement : RETURN'''
    p[0] = ReturnStatementNode(None)

def p_expression_statement(p):
    '''expression_statement : expression'''
    p[0] = p[1]

# ----------------------
# Database
# ----------------------
def p_connect_statement(p):
    '''connect_statement : CONNECT TO STRING_LITERAL AS IDENTIFIER'''
    p[0] = ConnectStatementNode(p[3], p[5])

def p_query_statement(p):
    '''query_statement : QUERY ON IDENTIFIER COLON STRING_LITERAL'''
    p[0] = QueryStatementNode(p[3], p[5])

def p_transaction_block(p):
    '''transaction_block : TRANSACTION ON IDENTIFIER BACKSLASH statement_list_opt BACKSLASH commit_rollback BACKSLASH'''
    p[0] = TransactionNode(p[3], BlockNode(p[5]), p[7])

def p_commit_rollback(p):
    '''commit_rollback : COMMIT
                       | ROLLBACK'''
    p[0] = p[1]

# ----------------------
# Crypto
# ----------------------
def p_crypto_statement(p):
    '''crypto_statement : crypto_generate_key_expr
                        | crypto_derive_public_key_expr
                        | crypto_encrypt_expr
                        | crypto_decrypt_expr
                        | crypto_hash_expr
                        | crypto_sign_expr
                        | crypto_verify_expr'''
    p[0] = p[1]

def p_crypto_generate_key_expr(p):
    '''crypto_generate_key_expr : DEFINE IDENTIFIER EQUALS GENERATE_KEY type_spec param_list_opt'''
    var_name = p[2]
    type_dict = p[5] if p[5] else {}
    param_dict = p[6] if p[6] else {}
    merged_dict = {**type_dict, **param_dict}
    key_type_str = merged_dict.get('type', None)
    key_type = TypeNode(key_type_str, None) if key_type_str else None
    algorithm = merged_dict.get('algorithm', None)
    size = merged_dict.get('size', None)
    db = merged_dict.get('db', None)
    node = CryptoGenerateKeyNode(var_name, key_type, algorithm, size, db)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_derive_public_key_expr(p):
    '''crypto_derive_public_key_expr : DEFINE IDENTIFIER EQUALS DERIVE_PUBLIC_KEY FROM IDENTIFIER'''
    var_name = p[2]
    private_key_name = p[6]
    node = CryptoDerivePublicKeyNode(var_name, private_key_name)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_encrypt_expr(p):
    '''crypto_encrypt_expr : DEFINE IDENTIFIER EQUALS ENCRYPT DATA COLON STRING_LITERAL WITH KEY COLON STRING_LITERAL ALGORITHM COLON STRING_LITERAL'''
    var_name = p[2]
    data_expr = StringLiteralNode(p[7])
    key_expr = StringLiteralNode(p[11])
    algorithm = p[15]
    node = CryptoEncryptNode(var_name, data_expr, key_expr, algorithm)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_decrypt_expr(p):
    '''crypto_decrypt_expr : DEFINE IDENTIFIER EQUALS DECRYPT DATA COLON STRING_LITERAL WITH KEY COLON STRING_LITERAL ALGORITHM COLON STRING_LITERAL'''
    var_name = p[2]
    data_expr = StringLiteralNode(p[7])
    key_expr = StringLiteralNode(p[11])
    algorithm = p[15]
    node = CryptoDecryptNode(var_name, data_expr, key_expr, algorithm)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_hash_expr(p):
    '''crypto_hash_expr : DEFINE IDENTIFIER EQUALS HASH DATA COLON STRING_LITERAL ALGORITHM COLON STRING_LITERAL'''
    var_name = p[2]
    data_expr = StringLiteralNode(p[6])
    algorithm = p[10]
    node = CryptoHashNode(var_name, data_expr, algorithm)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_sign_expr(p):
    '''crypto_sign_expr : DEFINE IDENTIFIER EQUALS SIGN DATA COLON STRING_LITERAL WITH KEY COLON STRING_LITERAL ALGORITHM COLON STRING_LITERAL'''
    var_name = p[2]
    data_expr = StringLiteralNode(p[6])
    key_expr = StringLiteralNode(p[10])
    algorithm = p[14]
    node = CryptoSignNode(var_name, data_expr, key_expr, algorithm)
    p[0] = VariableDeclarationNode(var_name, None, node)

def p_crypto_verify_expr(p):
    '''crypto_verify_expr : DEFINE IDENTIFIER EQUALS VERIFY SIGNATURE COLON STRING_LITERAL DATA COLON STRING_LITERAL WITH KEY COLON STRING_LITERAL ALGORITHM COLON STRING_LITERAL'''
    var_name = p[2]
    signature_expr = StringLiteralNode(p[6])
    data_expr = StringLiteralNode(p[9])
    key_expr = StringLiteralNode(p[13])
    algorithm = p[17]
    node = CryptoVerifyNode(var_name, signature_expr, data_expr, key_expr, algorithm)
    p[0] = VariableDeclarationNode(var_name, None, node)

# ----------------------
# Quantum
# ----------------------
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

# ----------------------
# JTML Elements
# ----------------------
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

# ----------------------
# Types and Parameters
# ----------------------
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

# ----------------------
# Expressions
# ----------------------
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

parser = yacc.yacc(debug=True)
