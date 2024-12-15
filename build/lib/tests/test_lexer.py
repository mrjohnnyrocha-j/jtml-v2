# tests/test_lexer.py

import unittest
from lexer.lexer import lexer

class TestJTMLLexer(unittest.TestCase):
    def setUp(self):
        # Initialize the lexer before each test
        self.lexer = lexer

    def tokenize(self, code):
        """
        Helper method to tokenize input code and return a list of tokens.
        """
        self.lexer.input(code)
        tokens = []
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

    def test_empty_input(self):
        """
        Test that empty input produces no tokens.
        """
        code = ""
        tokens = self.tokenize(code)
        self.assertEqual(len(tokens), 0)

    def test_define_variable(self):
        """
        Test tokenization of a variable declaration with an integer.
        Example: define x = 10\\
        """
        code = "define x = 10\\\\"
        tokens = self.tokenize(code)
        expected_types = ['DEFINE', 'IDENTIFIER', 'EQUALS', 'INT_LITERAL', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'x')
        self.assertEqual(tokens[3].value, 10)

    def test_define_const_variable(self):
        """
        Test tokenization of a constant variable declaration with a string.
        Example: const y = "hello"\\
        """
        code = 'const y = "hello"\\\\'
        tokens = self.tokenize(code)
        expected_types = ['CONST', 'IDENTIFIER', 'EQUALS', 'STRING_LITERAL', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[3].value, 'hello')

    def test_show_statement(self):
        """
        Test tokenization of a show statement with a string.
        Example: show "Hello, World!"\\
        """
        code = 'show "Hello, World!"\\\\'
        tokens = self.tokenize(code)
        expected_types = ['SHOW', 'STRING_LITERAL', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'Hello, World!')

    def test_crypto_generate_key_all_parameters(self):
        """
        Test tokenization of a generate_key statement with type, algorithm, and size.
        Example: define privateKey = generate_key type:"RSA", algorithm:"SHA256", size:2048\\
        """
        code = 'define privateKey = generate_key type:"RSA", algorithm:"SHA256", size:2048\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'GENERATE_KEY',
            'TYPE', 'COLON', 'STRING_LITERAL',
            'COMMA',
            'ALGORITHM', 'COLON', 'STRING_LITERAL',
            'COMMA',
            'SIZE', 'COLON', 'INT_LITERAL',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "privateKey")
        self.assertEqual(tokens[6].value, "RSA")
        self.assertEqual(tokens[10].value, "SHA256")
        self.assertEqual(tokens[14].value, 2048)

    def test_crypto_generate_key_type_and_size(self):
        """
        Test tokenization of a generate_key statement with type and size.
        Example: define privateKey = generate_key type:"RSA", size:2048\\
        """
        code = 'define privateKey = generate_key type:"RSA", size:2048\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'GENERATE_KEY',
            'TYPE', 'COLON', 'STRING_LITERAL',
            'COMMA',
            'SIZE', 'COLON', 'INT_LITERAL',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "privateKey")
        self.assertEqual(tokens[6].value, "RSA")
        self.assertEqual(tokens[10].value, 2048)

    def test_crypto_generate_key_type_and_algorithm(self):
        """
        Test tokenization of a generate_key statement with type and algorithm.
        Example: define privateKey = generate_key type:"RSA", algorithm:"SHA256"\\
        """
        code = 'define privateKey = generate_key type:"RSA", algorithm:"SHA256"\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'GENERATE_KEY',
            'TYPE', 'COLON', 'STRING_LITERAL',
            'COMMA',
            'ALGORITHM', 'COLON', 'STRING_LITERAL',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "privateKey")
        self.assertEqual(tokens[6].value, "RSA")
        self.assertEqual(tokens[10].value, "SHA256")

    def test_crypto_generate_key_only_type(self):
        """
        Test tokenization of a generate_key statement with only type.
        Example: define privateKey = generate_key type:"RSA"\\
        """
        code = 'define privateKey = generate_key type:"RSA"\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'GENERATE_KEY',
            'TYPE', 'COLON', 'STRING_LITERAL',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "privateKey")
        self.assertEqual(tokens[6].value, "RSA")

    def test_crypto_derive_public_key(self):
        """
        Test tokenization of a derive_public_key statement.
        Example: define publicKey = derive_public_key from privateKey\\
        """
        code = 'define publicKey = derive_public_key from privateKey\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'DERIVE_PUBLIC_KEY',
            'FROM', 'IDENTIFIER', 'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "publicKey")
        self.assertEqual(tokens[5].value, "privateKey")

    def test_crypto_encrypt(self):
        """
        Test tokenization of an encrypt statement.
        Example: define enc = encrypt data: message with key:publicKey algorithm:"RSA"\\
        """
        code = 'define enc = encrypt data: message with key:publicKey algorithm:"RSA"\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'ENCRYPT',
            'DATA', 'COLON', 'IDENTIFIER',
            'WITH', 'KEY', 'COLON', 'IDENTIFIER',
            'ALGORITHM', 'COLON', 'STRING_LITERAL',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, "enc")
        self.assertEqual(tokens[6].value, "message")
        self.assertEqual(tokens[10].value, "publicKey")
        self.assertEqual(tokens[13].value, "RSA")

    def test_invalid_token(self):
        """
        Test handling of invalid tokens. Illegal characters should be skipped.
        Example: invalid@token\\
        """
        code = 'invalid@token\\\\'
        tokens = self.tokenize(code)
        # Assuming that '@' is illegal and will be skipped, tokens should include IDENTIFIER 'invalid', IDENTIFIER 'token', BACKSLASH
        expected_types = ['IDENTIFIER', 'IDENTIFIER', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[0].value, "invalid")
        self.assertEqual(tokens[1].value, "token")

    def test_parentheses(self):
        """
        Test tokenization of function calls with parentheses and arguments.
        Example: function_call(a, b)\\
        """
        code = 'function_call(a, b)\\\\'
        tokens = self.tokenize(code)
        expected_types = ['IDENTIFIER', 'LPAREN', 'IDENTIFIER', 'COMMA', 'IDENTIFIER', 'RPAREN', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[0].value, 'function_call')
        self.assertEqual(tokens[2].value, 'a')
        self.assertEqual(tokens[4].value, 'b')

    def test_boolean_literals(self):
        """
        Test tokenization of boolean literals.
        Example:
            define flag = true\\
            define flag2 = false\\
        """
        code = 'define flag = true\\\\\ndefine flag2 = false\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'BOOL_LITERAL', 'BACKSLASH',
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'BOOL_LITERAL', 'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertTrue(tokens[3].value)
        self.assertFalse(tokens[8].value)

    def test_operators(self):
        """
        Test tokenization of various operators.
        Example: a = b + c * d / e - f == g != h && i || j !k\\
        """
        code = 'a = b + c * d / e - f == g != h && i || j !k\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'IDENTIFIER', 'EQUALS', 'IDENTIFIER', 'PLUS',
            'IDENTIFIER', 'TIMES', 'IDENTIFIER', 'DIVIDE',
            'IDENTIFIER', 'MINUS', 'IDENTIFIER', 'EQEQ',
            'IDENTIFIER', 'NEQ', 'IDENTIFIER', 'AND',
            'IDENTIFIER', 'OR', 'IDENTIFIER', 'NOT',
            'IDENTIFIER', 'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[0].value, 'a')
        self.assertEqual(tokens[2].value, 'b')
        self.assertEqual(tokens[4].value, 'c')
        self.assertEqual(tokens[6].value, 'd')
        self.assertEqual(tokens[8].value, 'e')
        self.assertEqual(tokens[10].value, 'f')
        self.assertEqual(tokens[12].value, 'g')
        self.assertEqual(tokens[14].value, 'h')
        self.assertEqual(tokens[16].value, 'i')
        self.assertEqual(tokens[18].value, 'j')
        self.assertEqual(tokens[20].value, 'k')

    def test_jtml_element_simple(self):
        """
        Test tokenization of a simple JTMLElement with no attributes and no content.
        Example: #p: "Hello, World!" #\\
        """
        code = '#p: "Hello, World!" #\\\\'
        tokens = self.tokenize(code)
        expected_types = ['HASH', 'IDENTIFIER', 'COLON', 'STRING_LITERAL', 'HASH', 'BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'p')
        self.assertEqual(tokens[3].value, 'Hello, World!')

    def test_jtml_element_with_attributes_and_content(self):
        """
        Test tokenization of a JTMLElement with attributes and nested content.
        Example:
            #div class:"container":\\
                show "Inside div"\\
            \\
        """
        code = (
            '#div class:"container":\\\\\n'
            '    show "Inside div"\\\\\n'
            '\\\\\n'
        )
        tokens = self.tokenize(code)
        expected_types = [
            'HASH', 'IDENTIFIER', 'CLASS', 'COLON', 'STRING_LITERAL',
            'COLON', 'BACKSLASH',
            'SHOW', 'STRING_LITERAL', 'BACKSLASH',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'div')
        self.assertEqual(tokens[4].value, 'container')  # Changed from tokens[3] to tokens[4]
        self.assertEqual(tokens[7].value, 'show')
        self.assertEqual(tokens[8].value, 'Inside div')


    def test_type_specification(self):
        """
        Test tokenization of type specifications in function declarations.
        Example: (a:int, b:string)\\
        """
        code = '(a:int, b:string)\\\\'
        tokens = self.tokenize(code)
        expected_types = [
            'LPAREN',
            'IDENTIFIER', 'COLON', 'TYPE',
            'COMMA',
            'IDENTIFIER', 'COLON', 'TYPE',
            'RPAREN',
            'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'a')
        self.assertEqual(tokens[3].value, 'int')
        self.assertEqual(tokens[5].value, 'b')
        self.assertEqual(tokens[7].value, 'string')

    def test_comment_handling(self):
        """
        Test handling of comments. Comments start with '//' and are skipped by the lexer.
        Example: // This is a comment
                \\
        """
        code = '// This is a comment\n\\\\'
        tokens = self.tokenize(code)
        expected_types = ['BACKSLASH']
        self.assertEqual([tok.type for tok in tokens], expected_types)

    def test_multiple_statements(self):
        """
        Test tokenization of multiple statements in a single input.
        Example:
            define x = 10\\
            show "Hello"\\
        """
        code = "define x = 10\\\\\nshow \"Hello\"\\\\"
        tokens = self.tokenize(code)
        expected_types = [
            'DEFINE', 'IDENTIFIER', 'EQUALS', 'INT_LITERAL', 'BACKSLASH',
            'SHOW', 'STRING_LITERAL', 'BACKSLASH'
        ]
        self.assertEqual([tok.type for tok in tokens], expected_types)
        self.assertEqual(tokens[1].value, 'x')
        self.assertEqual(tokens[3].value, 10)
        self.assertEqual(tokens[6].value, 'Hello')  


if __name__ == '__main__':
    unittest.main()
