# tests/test_parser.py

import unittest
from parser.parser import parser
from lexer.lexer import lexer
from compiler.ast_nodes import (
    ProgramNode, VariableDeclarationNode, ExpressionStatementNode,
    NumberLiteralNode, StringLiteralNode, BoolLiteralNode,
    IdentifierNode, BinaryOperationNode, ReturnStatementNode,
    IfStatementNode, BlockNode, ShowStatementNode,
    FunctionDeclarationNode, ParameterNode, ConnectStatementNode,
    QueryStatementNode, TransactionNode, QuantumDefineQubitNode,
    QuantumApplyNode, QuantumMeasureNode, CryptoGenerateKeyNode,
    CryptoDerivePublicKeyNode, CryptoEncryptNode, VariableDeclarationNode,
    CryptoDecryptNode, CryptoHashNode, CryptoSignNode,
    CryptoVerifyNode, JTMLElementNode, TypeNode, FunctionCallNode,
    ForStatementNode, WhileStatementNode
)
from jtml_types.node_types import IntType, VoidType, FloatType, StringType, BoolType, CustomType

class TestJTMLParser(unittest.TestCase):
    def setUp(self):
        self.parser = parser
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


    def parse_code(self, code):
        # PLY handles the lexing internally, no need to manually input code
        return self.parser.parse(code, lexer=self.lexer)

    # ----------------------
    # Basic Tests
    # ----------------------

    def test_empty_program(self):
        result = self.parse_code("")
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 0)

    def test_define_variable(self):
        # define x = 10\\
        code = r'define x = 10\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "x")
        self.assertIsInstance(stmt.value, NumberLiteralNode)
        self.assertEqual(stmt.value.value, 10)

    def test_simple_expression_statement(self):
        # x = 1 + 2\\
        code = r'x = 1 + 2\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, ExpressionStatementNode)
        
        expr = stmt.expression
        self.assertIsInstance(expr, BinaryOperationNode)
        self.assertEqual(expr.op, '=')
        self.assertEqual(expr.op, '=')
        self.assertIsInstance(expr.left, IdentifierNode)
        self.assertEqual(expr.left.name, 'x')
        self.assertIsInstance(expr.right, BinaryOperationNode)
        self.assertEqual(expr.right.op, '+')  
        self.assertIsInstance(expr.right.left, NumberLiteralNode)
        self.assertEqual(expr.right.left.value, 1)
        self.assertIsInstance(expr.right.right, NumberLiteralNode)
        self.assertEqual(expr.right.right.value, 2)

    def test_show_statement(self):
        # show "Hello"\\
        code = r'show "Hello"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, ShowStatementNode)
        self.assertIsInstance(stmt.value, StringLiteralNode)
        self.assertEqual(stmt.value.value, "Hello")

    # ----------------------
    # Control Flow Tests
    # ----------------------

    def test_if_statement_no_else(self):
        # define x = 10\\
        # if (x > 0) \\
        #     show "Positive"\\
        # \\
        code = (
            r'define x = 10\\ if (x > 0) \\     show "Positive"\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 2)
        
        # Check Variable Declaration
        decl_stmt = result.statements[0]
        self.assertIsInstance(decl_stmt, VariableDeclarationNode)
        self.assertEqual(decl_stmt.name, "x")
        self.assertIsInstance(decl_stmt.value, NumberLiteralNode)
        self.assertEqual(decl_stmt.value.value, 10)
        
        # Check If Statement
        if_stmt = result.statements[1]
        self.assertIsInstance(if_stmt, IfStatementNode)
        self.assertIsInstance(if_stmt.condition, BinaryOperationNode)
        self.assertEqual(if_stmt.condition.op, '>')
        self.assertIsInstance(if_stmt.condition.left, IdentifierNode)
        self.assertEqual(if_stmt.condition.left.name, "x")
        self.assertIsInstance(if_stmt.condition.right, NumberLiteralNode)
        self.assertEqual(if_stmt.condition.right.value, 0)
        self.assertIsInstance(if_stmt.then_block, BlockNode)
        self.assertEqual(len(if_stmt.then_block.statements), 1)
        show_stmt = if_stmt.then_block.statements[0]
        self.assertIsInstance(show_stmt, ShowStatementNode)
        self.assertIsInstance(show_stmt.value, StringLiteralNode)
        self.assertEqual(show_stmt.value.value, "Positive")
        self.assertIsNone(if_stmt.else_block)

    def test_if_statement_with_else(self):
        # define x = -1\\
        # if (x > 0) \\
        #     show "Positive"\\
        # else \\
        #     show "Non-positive"\\
        # \\
        code = (
            r'define x = -1\\ if (x > 0) \\     show "Positive"\\ else \\     show "Non-positive"\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 2)
        
        # Check Variable Declaration
        decl_stmt = result.statements[0]
        self.assertIsInstance(decl_stmt, VariableDeclarationNode)
        self.assertEqual(decl_stmt.name, "x")
        self.assertIsInstance(decl_stmt.value, NumberLiteralNode)
        self.assertEqual(decl_stmt.value.value, -1)
        
        # Check If Statement
        if_stmt = result.statements[1]
        self.assertIsInstance(if_stmt, IfStatementNode)
        self.assertIsInstance(if_stmt.condition, BinaryOperationNode)
        self.assertEqual(if_stmt.condition.op, '>')
        self.assertIsInstance(if_stmt.condition.left, IdentifierNode)
        self.assertEqual(if_stmt.condition.left.name, "x")
        self.assertIsInstance(if_stmt.condition.right, NumberLiteralNode)
        self.assertEqual(if_stmt.condition.right.value, 0)
        self.assertIsInstance(if_stmt.then_block, BlockNode)
        self.assertEqual(len(if_stmt.then_block.statements), 1)
        show_stmt_then = if_stmt.then_block.statements[0]
        self.assertIsInstance(show_stmt_then, ShowStatementNode)
        self.assertIsInstance(show_stmt_then.value, StringLiteralNode)
        self.assertEqual(show_stmt_then.value.value, "Positive")
        self.assertIsInstance(if_stmt.else_block, BlockNode)
        self.assertEqual(len(if_stmt.else_block.statements), 1)
        show_stmt_else = if_stmt.else_block.statements[0]
        self.assertIsInstance(show_stmt_else, ShowStatementNode)
        self.assertIsInstance(show_stmt_else.value, StringLiteralNode)
        self.assertEqual(show_stmt_else.value.value, "Non-positive")

    def test_while_statement(self):
        # while (count < 5) \\
        #     show count\\
        #     count += 1\\
        # \\
        code = (
            r'while (count < 5) \\     show count\\     count += 1\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        while_stmt = result.statements[0]
        self.assertIsInstance(while_stmt, WhileStatementNode)
        self.assertIsInstance(while_stmt.condition, BinaryOperationNode)
        self.assertEqual(while_stmt.condition.op, '<')
        self.assertIsInstance(while_stmt.condition.left, IdentifierNode)
        self.assertEqual(while_stmt.condition.left.name, "count")
        self.assertIsInstance(while_stmt.condition.right, NumberLiteralNode)
        self.assertEqual(while_stmt.condition.right.value, 5)
        self.assertIsInstance(while_stmt.body, BlockNode)
        self.assertEqual(len(while_stmt.body.statements), 2)
        
        # Check first statement inside while
        show_stmt = while_stmt.body.statements[0]
        self.assertIsInstance(show_stmt, ShowStatementNode)
        self.assertIsInstance(show_stmt.value, IdentifierNode)
        self.assertEqual(show_stmt.value.name, "count")
        
        # Check second statement inside while
        incr_stmt = while_stmt.body.statements[1]
        incr_stmt = incr_stmt.expression
        self.assertIsInstance(incr_stmt, BinaryOperationNode)
        self.assertEqual(incr_stmt.op, '+=')
        self.assertIsInstance(incr_stmt.left, IdentifierNode)
        self.assertEqual(incr_stmt.left.name, "count")
        self.assertIsInstance(incr_stmt.right, NumberLiteralNode)
        self.assertEqual(incr_stmt.right.value, 1)

    def test_for_loop(self):
        # for (item in items) \\
        #     show item\\
        # \\
        code = (
            r'for (item in items) \\     show item\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        for_stmt = result.statements[0]
        self.assertIsInstance(for_stmt, ForStatementNode)
        self.assertIsInstance(for_stmt.iterator, IdentifierNode)
        self.assertEqual(for_stmt.iterator.name, "item")
        self.assertIsInstance(for_stmt.iterable, IdentifierNode)
        self.assertEqual(for_stmt.iterable.name, "items")
        self.assertIsInstance(for_stmt.body, BlockNode)
        self.assertEqual(len(for_stmt.body.statements), 1)
        show_stmt = for_stmt.body.statements[0]
        self.assertIsInstance(show_stmt, ShowStatementNode)
        self.assertIsInstance(show_stmt.value, IdentifierNode)
        self.assertEqual(show_stmt.value.name, "item")

    # ----------------------
    # Function Declaration Tests
    # ----------------------
    
    def test_function_with_return(self):
        # function add(a:int, b:int):int \\
        #     return a + b\\
        # \\
        code = r'function add(a:int,b:int):int \\ return a+b\\ \\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        func = result.statements[0]
        self.assertIsInstance(func, FunctionDeclarationNode)
        self.assertEqual(func.name, "add")
        self.assertEqual(len(func.parameters), 2)
        self.assertIsInstance(func.parameters[0], ParameterNode)
        self.assertEqual(func.parameters[0].name, "a")
        self.assertIsInstance(func.parameters[0].param_type, IntType)
        self.assertIsInstance(func.parameters[1], ParameterNode)
        self.assertEqual(func.parameters[1].name, "b")
        self.assertIsInstance(func.parameters[1].param_type, IntType)
        self.assertIsInstance(func.return_type, IntType)
        self.assertIsInstance(func.body, BlockNode)
        self.assertEqual(len(func.body.statements), 1)
        ret_stmt = func.body.statements[0]
        self.assertIsInstance(ret_stmt, ReturnStatementNode)
        self.assertEqual(ret_stmt.expression.op, '+')
        self.assertEqual(ret_stmt.expression.left.name, "a")
        self.assertEqual(ret_stmt.expression.right.name, "b")


    def test_function_without_return(self):
        # function invalid():int \\
        #     show "No return"\\
        # \\
        code = r'function invalid():int \\ show "No return"\\ \\'
        with self.assertRaises(SyntaxError) as context:
            self.parse_code(code)
        self.assertIn("Function 'invalid' must have at least one return statement.", str(context.exception))

    def test_empty_function(self):
        # function empty():void \\
        # \\
        code = r'function empty():void \\'
        with self.assertRaises(SyntaxError) as context:
            self.parse_code(code)
        self.assertIn("Function 'empty' must have at least one return statement.", str(context.exception))

    def test_async_function_with_return(self):
        # async function fetchData():void \\
        #     return\\
        # \\
        code = r'async function fetchData():void \\ return\\ \\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        func = result.statements[0]
        self.assertIsInstance(func, FunctionDeclarationNode)
        self.assertTrue(func.async_function)
        self.assertEqual(func.name, "fetchData")
        self.assertIsInstance(func.return_type, VoidType)
        self.assertIsInstance(func.body, BlockNode)
        self.assertEqual(len(func.body.statements), 1)
        ret_stmt = func.body.statements[0]
        self.assertIsInstance(ret_stmt, ReturnStatementNode)
        self.assertIsNone(ret_stmt.expression)

    def test_function_with_conditional_return(self):
        # function checkPositive(n:int):bool \\
        #     if (n > 0) \\
        #         return true\\
        #     else \\
        #         return false\\
        # \\
        code = (
            r'function checkPositive(n:int):bool \\'
            r'if (n > 0) \\ return true\\ else \\ return false\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        func = result.statements[0]
        self.assertIsInstance(func, FunctionDeclarationNode)
        self.assertEqual(func.name, "checkPositive")
        self.assertEqual(len(func.parameters), 1)
        self.assertEqual(func.parameters[0].name, "n")
        self.assertIsInstance(func.parameters[0].param_type, IntType)
        self.assertIsInstance(func.return_type, BoolType)
        self.assertIsInstance(func.body, BlockNode)
        self.assertEqual(len(func.body.statements), 1)
        if_stmt = func.body.statements[0]
        self.assertIsInstance(if_stmt, IfStatementNode)
        self.assertIsInstance(if_stmt.condition, BinaryOperationNode)
        self.assertEqual(if_stmt.condition.op, '>')
        self.assertEqual(if_stmt.condition.left.name, "n")
        self.assertEqual(if_stmt.condition.right.value, 0)
        self.assertIsInstance(if_stmt.then_block, BlockNode)
        self.assertEqual(len(if_stmt.then_block.statements), 1)
        ret_then = if_stmt.then_block.statements[0]
        self.assertIsInstance(ret_then, ReturnStatementNode)
        self.assertEqual(ret_then.expression.value, True)
        self.assertIsInstance(if_stmt.else_block, BlockNode)
        self.assertEqual(len(if_stmt.else_block.statements), 1)
        ret_else = if_stmt.else_block.statements[0]
        self.assertIsInstance(ret_else, ReturnStatementNode)
        self.assertEqual(ret_else.expression.value, False)

    def test_function_recursion(self):
        # function factorial(n:int):int \\
        #     if (n <= 1) \\
        #         return 1\\
        #     else \\
        #         return n * factorial(n-1)\\
        # \\
        code = (
            r'function factorial(n:int):int \\     if (n <= 1) \\         return 1\\     else \\         return n * factorial(n-1)\\ \\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        func = result.statements[0]
        self.assertIsInstance(func, FunctionDeclarationNode)
        self.assertEqual(func.name, "factorial")
        self.assertEqual(len(func.parameters), 1)
        self.assertEqual(func.parameters[0].name, "n")
        self.assertIsInstance(func.parameters[0].param_type, TypeNode)
        self.assertEqual(func.parameters[0].param_type.name, "int")
        self.assertIsInstance(func.return_type, IntType)
        self.assertIsInstance(func.body, BlockNode)
        self.assertEqual(len(func.body.statements), 2)
        
        # Check If Statement
        if_stmt = func.body.statements[0]
        self.assertIsInstance(if_stmt, IfStatementNode)
        self.assertIsInstance(if_stmt.condition, BinaryOperationNode)
        self.assertEqual(if_stmt.condition.op, '<=')
        self.assertIsInstance(if_stmt.condition.left, IdentifierNode)
        self.assertEqual(if_stmt.condition.left.name, "n")
        self.assertIsInstance(if_stmt.condition.right, NumberLiteralNode)
        self.assertEqual(if_stmt.condition.right.value, 1)
        
        # Check Return in If Block
        ret_if = if_stmt.then_block.statements[0]
        self.assertIsInstance(ret_if, ReturnStatementNode)
        self.assertIsInstance(ret_if.expression, NumberLiteralNode)
        self.assertEqual(ret_if.expression.value, 1)
        
        # Check Return in Else Block
        ret_else = if_stmt.else_block.statements[0]
        self.assertIsInstance(ret_else, ReturnStatementNode)
        self.assertIsInstance(ret_else.expression, BinaryOperationNode)
        self.assertEqual(ret_else.expression.op, '*')
        self.assertIsInstance(ret_else.expression.left, IdentifierNode)
        self.assertEqual(ret_else.expression.left.name, "n")
        self.assertIsInstance(ret_else.expression.right, FunctionCallNode)
        self.assertEqual(ret_else.expression.right.function.name, "factorial")
        self.assertEqual(len(ret_else.expression.right.arguments), 1)
        arg = ret_else.expression.right.arguments[0]
        self.assertIsInstance(arg, BinaryOperationNode)
        self.assertEqual(arg.op, '-')
        self.assertIsInstance(arg.left, IdentifierNode)
        self.assertEqual(arg.left.name, "n")
        self.assertIsInstance(arg.right, NumberLiteralNode)
        self.assertEqual(arg.right.value, 1)

    # ----------------------
    # Boolean Literals Test
    # ----------------------

    def test_boolean_literals(self):
        # define flag = true\\
        # define isActive = false\\
        code = (
            r'define flag = true\\ define isActive = false\\'
        )
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 2)
        
        # Check first variable
        flag_decl = result.statements[0]
        self.assertIsInstance(flag_decl, VariableDeclarationNode)
        self.assertEqual(flag_decl.name, "flag")
        self.assertIsInstance(flag_decl.value, BoolLiteralNode)
        self.assertTrue(flag_decl.value.value)
        
        # Check second variable
        isActive_decl = result.statements[1]
        self.assertIsInstance(isActive_decl, VariableDeclarationNode)
        self.assertEqual(isActive_decl.name, "isActive")
        self.assertIsInstance(isActive_decl.value, BoolLiteralNode)
        self.assertFalse(isActive_decl.value.value)

    # ----------------------
    # Complex Expression Test
    # ----------------------

    def test_complex_expression(self):
        # x = (y + 3) * 2\\
        code = r'x = (y + 3) * 2\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, ExpressionStatementNode)
        
        expr = stmt.expression
        self.assertEqual(expr.op, '=')
        self.assertIsInstance(expr.left, IdentifierNode)
        self.assertEqual(expr.left.name, 'x')
        self.assertIsInstance(expr.right, BinaryOperationNode)
        self.assertEqual(expr.right.op, '*')
        self.assertIsInstance(expr.right.left, BinaryOperationNode)
        self.assertEqual(expr.right.left.op, '+')
        self.assertIsInstance(expr.right.left.left, IdentifierNode)
        self.assertEqual(expr.right.left.left.name, 'y')
        self.assertIsInstance(expr.right.left.right, NumberLiteralNode)
        self.assertEqual(expr.right.left.right.value, 3)
        self.assertIsInstance(expr.right.right, NumberLiteralNode)
        self.assertEqual(expr.right.right.value, 2)

    # ----------------------
    # Database Statements Tests
    # ----------------------

    def test_connect_statement(self):
        # connect to "sqlite:///mydb.db" as mydb\\
        code = r'connect to "sqlite:///mydb.db" as mydb\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, ConnectStatementNode)
        self.assertEqual(stmt.db_url, "sqlite:///mydb.db")
        self.assertEqual(stmt.db_var, "mydb")

    def test_query_statement(self):
        # query on mydb:"SELECT * FROM users"\\
        code = r'query on mydb:"SELECT * FROM users"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, QueryStatementNode)
        self.assertEqual(stmt.db_var, "mydb")
        self.assertEqual(stmt.query_str, "SELECT * FROM users")

    # ----------------------
    # Quantum Statements Tests
    # ----------------------

    def test_quantum_define_qubit(self):
        # define q1 as qubit\\
        code = r'define q1 as qubit\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, QuantumDefineQubitNode)
        self.assertEqual(stmt.qubit_name, "q1")

    def test_quantum_apply(self):
        # apply H on q1,q2\\
        code = r'apply H on q1,q2\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, QuantumApplyNode)
        self.assertEqual(stmt.gate, "H")
        self.assertEqual(len(stmt.qubits), 2)
        self.assertIsInstance(stmt.qubits[0], IdentifierNode)
        self.assertEqual(stmt.qubits[0].name, "q1")
        self.assertIsInstance(stmt.qubits[1], IdentifierNode)
        self.assertEqual(stmt.qubits[1].name, "q2")

    def test_quantum_measure(self):
        # define r = measure q1\\
        code = r'define r = measure q1\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "r")
        self.assertIsInstance(stmt.value, QuantumMeasureNode)
        self.assertEqual(stmt.value.var_name, "r")
        self.assertEqual(stmt.value.qubit_name, "q1")

    # ----------------------
    # Crypto Statements Tests
    # ----------------------

    def test_crypto_generate_key_all_parameters(self):
        # define privateKey = generate_key type:"RSA", algorithm:"SHA256", size:2048, db:"myDatabase"\\
        code = r'define privateKey = generate_key type:"RSA", algorithm:"SHA256", size:2048, db:"myDatabase"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "privateKey")
        self.assertIsInstance(stmt.value, CryptoGenerateKeyNode)
        self.assertEqual(stmt.value.key_type.name, "RSA")
        self.assertEqual(stmt.value.algorithm, "SHA256")
        self.assertEqual(stmt.value.size, 2048)
        self.assertEqual(stmt.value.db, "myDatabase")
        
    def test_crypto_generate_key_only_type(self):
        # define privateKey = generate_key type:"RSA"\\
        code = r'define privateKey = generate_key type:"RSA"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "privateKey")
        self.assertIsInstance(stmt.value, CryptoGenerateKeyNode)
        self.assertEqual(stmt.value.key_type.name, "RSA")
        self.assertIsNone(stmt.value.algorithm)
        self.assertIsNone(stmt.value.size)
        self.assertIsNone(stmt.value.db)
    
    def test_crypto_generate_key_type_and_size(self):
        # define privateKey = generate_key type:"RSA", size:2048\\
        code = r'define privateKey = generate_key type:"RSA", size:2048\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "privateKey")
        self.assertIsInstance(stmt.value, CryptoGenerateKeyNode)
        self.assertEqual(stmt.value.key_type.name, "RSA")
        self.assertIsNone(stmt.value.algorithm)
        self.assertEqual(stmt.value.size, 2048)
        self.assertIsNone(stmt.value.db)
    
    def test_crypto_generate_key_type_and_algorithm(self):
        # define privateKey = generate_key type:"RSA", algorithm:"SHA256"\\
        code = r'define privateKey = generate_key type:"RSA", algorithm:"SHA256"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "privateKey")
        self.assertIsInstance(stmt.value, CryptoGenerateKeyNode)
        self.assertEqual(stmt.value.key_type.name, "RSA")
        self.assertEqual(stmt.value.algorithm, "SHA256")
        self.assertIsNone(stmt.value.size)
        self.assertIsNone(stmt.value.db)
    
    def test_crypto_derive_public_key(self):
        # define publicKey = derive_public_key from privateKey\\
        code = r'define publicKey = derive_public_key from privateKey\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "publicKey")
        self.assertIsInstance(stmt.value, CryptoDerivePublicKeyNode)
        self.assertEqual(stmt.value.operation, "derive_public_key")
        self.assertIsInstance(stmt.value.identifier, IdentifierNode)
        self.assertEqual(stmt.value.identifier.name, "privateKey")

    def test_crypto_encrypt(self):
        # define enc = encrypt data:"message" with key:"publicKey" algorithm:"RSA"\\
        code = r'define enc = encrypt data:"message" with key:"publicKey" algorithm:"RSA"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "enc")
        self.assertIsInstance(stmt.value, CryptoEncryptNode)
        self.assertEqual(stmt.value.var_name, "enc")
        self.assertIsInstance(stmt.value.data_expr, StringLiteralNode)
        self.assertEqual(stmt.value.data_expr.value, "message")
        self.assertIsInstance(stmt.value.key_expr, StringLiteralNode)
        self.assertEqual(stmt.value.key_expr.value, "publicKey")
        self.assertEqual(stmt.value.algorithm, "RSA")

    def test_crypto_decrypt(self):
        # define dec = decrypt data:"encryptedMessage" with key:"privateKey" algorithm:"RSA"\\
        code = r'define dec = decrypt data: "encryptedMessage" with key: "privateKey" algorithm: "RSA"\\'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        
        stmt = result.statements[0]
        self.assertIsInstance(stmt, VariableDeclarationNode)
        self.assertEqual(stmt.name, "dec")
        self.assertIsInstance(stmt.value, CryptoDecryptNode)
        self.assertEqual(stmt.value.var_name, "dec")
        self.assertIsInstance(stmt.value.data_expr, StringLiteralNode)
        self.assertEqual(stmt.value.data_expr.value, "encryptedMessage")
        self.assertIsInstance(stmt.value.key_expr, StringLiteralNode)
        self.assertEqual(stmt.value.key_expr.value, "privateKey")
        self.assertEqual(stmt.value.algorithm, "RSA")

    # def test_crypto_hash(self):
    #     # define hashed = hash data:"myData" algorithm:"SHA256"\\
    #     code = r'define hashed = hash data: "myData" algorithm: "SHA256"\\'
    #     result = self.parse_code(code)
    #     self.assertIsInstance(result, ProgramNode)
    #     self.assertEqual(len(result.statements), 1)
        
    #     stmt = result.statements[0]
    #     self.assertIsInstance(stmt, VariableDeclarationNode)
    #     self.assertEqual(stmt.name, "hashed")
    #     self.assertIsInstance(stmt.value, CryptoHashNode)
    #     self.assertEqual(stmt.value.var_name, "hashed")
    #     self.assertIsInstance(stmt.value.data_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.data_expr.value, "myData")
    #     self.assertEqual(stmt.value.algorithm, "SHA256")

    # def test_crypto_sign(self):
    #     # define signature = sign data:"message" with key:"privateKey" algorithm:"SHA256"\\
    #     code = r'define signature = sign data:"message" with key:"privateKey" algorithm:"SHA256"\\'
    #     result = self.parse_code(code)
    #     self.assertIsInstance(result, ProgramNode)
    #     self.assertEqual(len(result.statements), 1)
        
    #     stmt = result.statements[0]
    #     self.assertIsInstance(stmt, VariableDeclarationNode)
    #     self.assertEqual(stmt.name, "signature")
    #     self.assertIsInstance(stmt.value, CryptoSignNode)
    #     self.assertEqual(stmt.value.var_name.value, "signature")
    #     self.assertIsInstance(stmt.value.data_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.data_expr.value, "message")
    #     self.assertIsInstance(stmt.value.key_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.key_expr.value, "privateKey")
    #     self.assertEqual(stmt.value.algorithm, "SHA256")

    # def test_crypto_verify(self):
    #     # define isValid = verify signature:"signature" data:"message" with key:"publicKey" algorithm:"SHA256"\\
    #     code = r'define isValid = verify signature: "signature" data: "message" with key: "publicKey" algorithm: "SHA256"\\'
    #     result = self.parse_code(code)
    #     self.assertIsInstance(result, ProgramNode)
    #     self.assertEqual(len(result.statements), 1)
        
    #     stmt = result.statements[0]
    #     self.assertIsInstance(stmt, VariableDeclarationNode)
    #     self.assertEqual(stmt.name, "isValid")
    #     self.assertIsInstance(stmt.value, CryptoVerifyNode)
    #     self.assertEqual(stmt.value.var_name, "isValid")
    #     self.assertIsInstance(stmt.value.signature_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.signature_expr.value, "signature")
    #     self.assertIsInstance(stmt.value.data_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.data_expr.value, "message")
    #     self.assertIsInstance(stmt.value.key_expr, StringLiteralNode)
    #     self.assertEqual(stmt.value.key_expr.value, "publicKey")
    #     self.assertEqual(stmt.value.algorithm, "SHA256")

    # ----------------------
    # JTMLElementNode Tests
    # ----------------------

    def test_jtml_element_simple_no_closing_tag(self):
        # JTML Code:
        # #p
        #     show "Hello, World!"\\
        # #
        code = r'#p   show "Hello, World!"\\ #'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        
        stmt = result.statements[0]
        self.assertIsInstance(stmt, JTMLElementNode)
        self.assertEqual(stmt.tag_name, "p")
        self.assertEqual(stmt.attributes, {})
        self.assertEqual(len(stmt.content), 1)
        self.assertIsInstance(stmt.content[0], ShowStatementNode)
        self.assertEqual(stmt.content[0].value.value, "Hello, World!")

    def test_jtml_element_simple_with_repeating_closing_tag(self):
        # JTML Code:
        # #p
        #     show "Hello, World!"\\
        # #
        code = r'#p    show "Hello, World!"\\#p'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)
        
        stmt = result.statements[0]
        self.assertIsInstance(stmt, JTMLElementNode)
        self.assertEqual(stmt.tag_name, "p")
        self.assertEqual(stmt.attributes, {})
        self.assertEqual(len(stmt.content), 1)
        self.assertIsInstance(stmt.content[0], ShowStatementNode)
        self.assertEqual(stmt.content[0].value.value, "Hello, World!")

    def test_jtml_element_with_attributes_and_content(self):
        # JTML Code:
        # #div name: "container" \\
        #     define x = 1 + 2\\
        #     define y = x * 3\\
        # #
        code = r'#div name: "container"\\   define x = 1 + 2\\  define  y = x * 3\\#'
        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 1)

        element = result.statements[0]
        self.assertIsInstance(element, JTMLElementNode)
        self.assertEqual(element.tag_name, "div")
        self.assertEqual(element.attributes, {'name': 'container'})
        self.assertEqual(len(element.content), 2)

        stmt1 = element.content[0]
        self.assertIsInstance(stmt1, VariableDeclarationNode)

        expr1 = stmt1.expression
        self.assertIsInstance(expr1, BinaryOperationNode)
        self.assertEqual(expr1.op, '=')

        self.assertIsInstance(expr1.left, IdentifierNode)
        self.assertEqual(expr1.left.name, 'x')

        self.assertIsInstance(expr1.right, BinaryOperationNode)
        self.assertEqual(expr1.right.op, '+')

        self.assertIsInstance(expr1.right.left, NumberLiteralNode)
        self.assertEqual(expr1.right.left.value, 1)

        self.assertIsInstance(expr1.right.right, NumberLiteralNode)
        self.assertEqual(expr1.right.right.value, 2)

        stmt2 = element.content[1]
        self.assertIsInstance(stmt2, VariableDeclarationNode)

        expr2 = stmt2.expression
        self.assertIsInstance(expr2, BinaryOperationNode)
        self.assertEqual(expr2.op, '=')

        self.assertIsInstance(expr2.left, IdentifierNode)
        self.assertEqual(expr2.left.name, 'y')

        self.assertIsInstance(expr2.right, BinaryOperationNode)
        self.assertEqual(expr2.right.op, '*')

        self.assertIsInstance(expr2.right.left, IdentifierNode)
        self.assertEqual(expr2.right.left.name, 'x')

        self.assertIsInstance(expr2.right.right, NumberLiteralNode)
        self.assertEqual(expr2.right.right.value, 3)

    def test_jtml_element_dynamic_content(self):
        # JTML Code:
        # define userName = "Alice"\\
        # #p
        #     show "Welcome, #(userName)"\\
        # #
            
        code = (
            r'define userName = "Alice"\\ #p     show "Welcome, #(userName)"\\ #p'
        )
        for token in self.tokenize(code):
            print(token)

        result = self.parse_code(code)
        self.assertIsInstance(result, ProgramNode)
        self.assertEqual(len(result.statements), 2)
        
        # Check Variable Declaration
        decl_stmt = result.statements[0]
        self.assertIsInstance(decl_stmt, VariableDeclarationNode)
        self.assertEqual(decl_stmt.name, "userName")
        self.assertIsInstance(decl_stmt.value, StringLiteralNode)
        self.assertEqual(decl_stmt.value.value, "Alice")
        
        # Check JTML Element
        p_stmt = result.statements[1]
        self.assertIsInstance(p_stmt, JTMLElementNode)
        self.assertEqual(p_stmt.tag_name, "p")
        self.assertEqual(p_stmt.attributes, {})
        self.assertEqual(len(p_stmt.content), 1)
        self.assertIsInstance(p_stmt.content[0], ShowStatementNode)
        self.assertEqual(p_stmt.content[0].value.value, "Welcome, #(userName)")
        
    def test_jtml_element_mismatched_closing_tag(self):
        code = r'#div name: "container"\\ show "Hello, World!"\\#span'
        with self.assertRaises(SyntaxError) as context:
            self.parse_code(code)
        self.assertIn("Closing tag 'span' does not match opening tag 'div'", str(context.exception))
            

    # ----------------------
    # Additional Tests (Optional)
    # ----------------------
    
    # You can add more test cases here to cover other aspects of your JTML parser.

if __name__ == '__main__':
    unittest.main()
