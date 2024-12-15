# parser/crypto.py

from compiler.ast_nodes import (
    CryptoGenerateKeyNode, CryptoDerivePublicKeyNode,
    CryptoEncryptNode, CryptoDecryptNode, CryptoHashNode,
    CryptoSignNode, CryptoVerifyNode, VariableDeclarationNode,
    StringLiteralNode, TypeNode
)
from lexer.lexer import tokens

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
