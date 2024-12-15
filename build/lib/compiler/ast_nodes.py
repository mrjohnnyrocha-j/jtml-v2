# ast_nodes.py
#
# Abstract Syntax Tree (AST) node definitions for JTML.
# Updated to be consistent with the parser and tests.
#
# Notes:
# - Blocks are sequences of statements terminated by a standalone '\\' line.
# - Every statement ends with '\\'.
# - Conditional statements, loops, functions, etc., follow the unified block structure.
# - Crypto and Quantum nodes are wrapped in VariableDeclarationNode where tests expect them.
#
# fenote: This file defines all AST node classes that represent constructs in the JTML language.
#         Each node type corresponds to a grammatical construct. By using a structured AST,
#         the parser output can be easily analyzed or transformed by subsequent compiler phases.
#
# fenote: Nodes generally hold references to other nodes or primitive values.
#         For example, a BinaryOperationNode holds references to its left and right operands (also nodes),
#         and a variable declaration node holds the name, type, and an expression node representing the initial value.
#
# fenote: The presence of Crypto and Quantum nodes aligns with advanced language features.
#         The tests require these nodes to appear inside VariableDeclarationNodes in some cases,
#         so we integrate these new nodes in a way that matches test expectations.
#
# fenote: Where possible, docstrings describe the expected structure and usage of each node type.

from jtml_types.node_types import *

class Node:
    """Base class for all AST nodes."""
    pass

class EmptyStatementNode(Node):
    """Represents an empty statement (a standalone backslash)."""
    def __init__(self):
        pass

class ProgramNode(Node):
    """
    Represents the entire JTML program.
    A program is zero or more top-level statements.
    
    fenote: The root of the AST. Contains a list of statements at the top-level scope.
    """
    def __init__(self, statements):
        self.statements = statements  # list of Node

class BlockNode(Node):
    """
    A block of statements, ended by a line with '\\'.
    
    fenote: Represents a grouped sequence of statements, such as those inside a function, if-then block, etc.
    """
    def __init__(self, statements):
        self.statements = statements  # list of Node

class VariableDeclarationNode(Node):
    """
    Represents a variable or const declaration.
    Examples:
      define x = 10\\
      const y: int = 20\\
    
    fenote: Declares a named variable with an optional type and initial value.
    """
    def __init__(self, name, var_type, value, const=False):
        self.name = name            # str
        self.var_type = var_type    # TypeNode or None
        self.value = value          # Node representing the initial value
        self.const = const          # bool

class ShowStatementNode(Node):
    """show <expression>\\
    
    fenote: Outputs the value of an expression to the console or another medium.
    """
    def __init__(self, value):
        self.value = value  # ExpressionNode

class SaveStatementNode(Node):
    """save <identifier> = <expression>\\
    
    fenote: Saves the value of an expression into a persistent store, keyed by the identifier.
    """
    def __init__(self, identifier, value):
        self.identifier = identifier  # str
        self.value = value            # ExpressionNode

class DeleteStatementNode(Node):
    """delete <identifier>\\
    
    fenote: Removes a previously saved variable or resource identified by the given identifier.
    """
    def __init__(self, identifier):
        self.identifier = identifier  # str

class ReturnStatementNode(Node):
    """return [expression]\\
    
    fenote: Returns from the current function call, optionally with a result value.
    """
    def __init__(self, expression):
        self.expression = expression  # ExpressionNode or None

class ThrowStatementNode(Node):
    """throw <expression>\\
    
    fenote: Throws an exception or error represented by the given expression.
    """
    def __init__(self, expression):
        self.expression = expression  # ExpressionNode

class ExpressionStatementNode(Node):
    """
    <expression>\\
    Represents an expression used as a statement.
    
    fenote: Allows a standalone expression (like x = y+2) to form a statement.
    """
    def __init__(self, expression):
        self.expression = expression  # ExpressionNode

class IfStatementNode(Node):
    """
    if (condition) \\
        ...then_block...\\
    else \\
        ...else_block...\\
    \\
    else_block is optional.
    
    fenote: A conditional branching node. Executes then_block if condition is true,
            else executes else_block if present.
    """
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition    # ExpressionNode
        self.then_block = then_block  # BlockNode
        self.else_block = else_block  # BlockNode or None

class WhileStatementNode(Node):
    """while (condition) \\
        ...body...\\
    
    fenote: A loop node that repeats body while condition is true.
    """
    def __init__(self, condition, body):
        self.condition = condition  # ExpressionNode
        self.body = body            # BlockNode

class ForStatementNode(Node):
    """
    for (iterator in expression) \\
        ...statements...\\
    \\
    
    fenote: A loop node that iterates over an iterable expression, binding each element to the iterator variable.
    """
    def __init__(self, iterator_name, iterable_expr, body):
        self.iterator = IdentifierNode(iterator_name) # tests expect an IdentifierNode
        self.iterable = iterable_expr                 # ExpressionNode
        self.body = body                              # BlockNode

class TryCatchFinallyNode(Node):
    """
    try \\
        ...try_block...\\
    catch(e) \\
        ...catch_block...\\
    finally \\
        ...finally_block...\\
    \\
    catch and finally are optional.
    
    fenote: Error handling construct with optional catch and finally blocks.
    """
    def __init__(self, try_block, exception_var, catch_block, finally_block):
        self.try_block = try_block          # BlockNode
        self.exception_var = exception_var  # IdentifierNode or None
        self.catch_block = catch_block      # BlockNode or None
        self.finally_block = finally_block  # BlockNode or None

class FunctionDeclarationNode(Node):
    """
    function <name>(params): returnType \\
        ...statements...\\
    \\
    or async function.
    
    fenote: Defines a named function or an async function with parameters, return type, and a body.
    """
    def __init__(self, name, parameters, return_type, body, async_function=False):
        self.name = name                # str
        self.parameters = parameters    # list of ParameterNode
        self.return_type = return_type  # TypeNode or VoidType
        self.body = body                # BlockNode
        self.async_function = async_function

class ParameterNode(Node):
    """A single function parameter: name: type.
    
    fenote: Declares one parameter of a function.
    """
    def __init__(self, name, param_type):
        self.name = name        # str
        self.param_type = param_type # TypeNode or primitive

class ClassDeclarationNode(Node):
    """class <Name> \\
        ...members...\\
    
    fenote: Declares a class with members (fields, methods).
    """
    def __init__(self, name, members):
        self.name = name       # str
        self.members = members # list of Node

class ConnectStatementNode(Node):
    """connect to "db_url" as db\\
    
    fenote: Establishes a connection to a database and assigns it to a variable.
    """
    def __init__(self, db_url, db_var):
        self.db_url = db_url  # str
        self.db_var = db_var  # str

class QueryStatementNode(Node):
    """query on db:"SQL"\\
    
    fenote: Executes a database query on a previously connected database.
    """
    def __init__(self, db_var, query_str):
        self.db_var = db_var
        self.query_str = query_str

class TransactionNode(Node):
    """transaction on db \\
        ...block...\\
    commit or rollback\\
    
    fenote: A transactional block of statements executed on a database connection, ending with commit or rollback.
    """
    def __init__(self, db_var, block, mode):
        self.db_var = db_var   # str
        self.block = block     # BlockNode
        self.mode = mode       # "commit" or "rollback"

class QuantumDefineQubitNode(Node):
    """define q1 as qubit\\
    
    fenote: Declares a quantum qubit variable.
    """
    def __init__(self, qubit_name):
        self.qubit_name = qubit_name

class QuantumApplyNode(Node):
    """apply H on q1,q2\\
    
    fenote: Applies a quantum gate to one or more qubits.
    """
    def __init__(self, gate, qubits):
        self.gate = gate       # str
        self.qubits = qubits   # list of IdentifierNode

class QuantumMeasureNode(Node):
    """Represents measure operation, often used inside a variable declaration.
    
    fenote: Measures a qubit and assigns its classical result to a variable.
    """
    def __init__(self, var_name, qubit_name):
        self.var_name = var_name
        self.qubit_name = qubit_name

class CryptoGenerateKeyNode(Node):
    """
    define var = generate_key type:"RSA", algorithm:"SHA256", size:2048, db:"myDatabase"\\
    
    fenote: Generates a cryptographic key with given parameters.
    """
    def __init__(self, var_name, key_type, algorithm=None, size=None, db=None):
        self.var_name = var_name
        self.key_type = key_type
        self.algorithm = algorithm
        self.size = size
        self.db = db

class CryptoDerivePublicKeyNode(Node):
    """
    define var = derive_public_key from privateKey\\
    
    fenote: Derives a public key from a private key.
    """
    def __init__(self, var_name, private_key_name):
        self.var_name = var_name
        self.private_key_name = private_key_name
        self.operation = "derive_public_key"
        self.identifier = IdentifierNode(private_key_name)

class CryptoEncryptNode(Node):
    """
    define var = encrypt data:"message" with key:"publicKey" algorithm:"RSA"\\
    
    fenote: Encrypts data using a given key and algorithm.
    """
    def __init__(self, var_name, data_expr, key_expr, algorithm):
        self.var_name = var_name
        self.data_expr = data_expr
        self.key_expr = key_expr
        self.algorithm = algorithm

class CryptoDecryptNode(Node):
    """
    define var = decrypt data:"encryptedMessage" with key:"privateKey" algorithm:"RSA"\\
    
    fenote: Decrypts data using a given key and algorithm.
    """
    def __init__(self, var_name, data_expr, key_expr, algorithm):
        self.var_name = var_name
        self.data_expr = data_expr
        self.key_expr = key_expr
        self.algorithm = algorithm

class CryptoHashNode(Node):
    """
    define var = hash data:"myData" algorithm:"SHA256"\\
    
    fenote: Hashes data using the specified algorithm.
    """
    def __init__(self, var_name, data_expr, algorithm):
        self.var_name = var_name
        self.data_expr = data_expr
        self.algorithm = algorithm

class CryptoSignNode(Node):
    """
    define var = sign data:"message" with key:"privateKey" algorithm:"SHA256"\\
    
    fenote: Signs data using a key and a hashing algorithm.
    """
    def __init__(self, var_name, data_expr, key_expr, algorithm):
        self.var_name = var_name
        self.data_expr = data_expr
        self.key_expr = key_expr
        self.algorithm = algorithm

class CryptoVerifyNode(Node):
    """
    define var = verify signature:"signature" data:"message" with key:"publicKey" algorithm:"SHA256"\\
    
    fenote: Verifies a signature for given data and key using a specified algorithm.
    """
    def __init__(self, var_name, signature_expr, data_expr, key_expr, algorithm):
        self.var_name = var_name
        self.signature_expr = signature_expr
        self.data_expr = data_expr
        self.key_expr = key_expr
        self.algorithm = algorithm

class JTMLElementNode(Node):
    """
    #tagName attributes content # or #tagName
    
    fenote: Represents a JTML element (similar to HTML), with attributes and child content.
    """
    def __init__(self, tag_name, attributes, content):
        self.tag_name = tag_name
        self.attributes = attributes
        self.content = content

class AwaitExpressionNode(Node):
    """await expression
    
    fenote: Represents an asynchronous wait on a promise or future.
    """
    def __init__(self, expression):
        self.expression = expression

class ExpressionNode(Node):
    """Base class for all expressions."""
    pass

class BinaryOperationNode(ExpressionNode):
    """(left op right)
    
    fenote: A binary operation (e.g. +, -, *, /, <, >, ==) on two operand expressions.
    """
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class UnaryOperationNode(ExpressionNode):
    """op operand
    
    fenote: A unary operation (e.g. -x, !x) on a single operand.
    """
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

class NumberLiteralNode(ExpressionNode):
    """A numeric literal (int or float)."""
    def __init__(self, value):
        self.value = value

class StringLiteralNode(ExpressionNode):
    """A string literal."""
    def __init__(self, value):
        self.value = value

class BoolLiteralNode(ExpressionNode):
    """A boolean literal: true or false."""
    def __init__(self, value):
        self.value = value

class IdentifierNode(ExpressionNode):
    """An identifier referencing a variable, function, or object property."""
    def __init__(self, name):
        self.name = name

class FunctionCallNode(ExpressionNode):
    """function(args...) or obj.method(args...)"""
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

class MemberAccessNode(ExpressionNode):
    """obj.member
    
    fenote: Accesses a property or method of an object.
    """
    def __init__(self, obj, member):
        self.obj = obj
        self.member = member
