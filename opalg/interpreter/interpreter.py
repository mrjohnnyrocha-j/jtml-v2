# opalg/interpreter/interpreter.py

from opalg.compiler.ast_nodes import *
from opalg.interpreter.optimizer import Optimizer   # If you have an optimizer.py
from opalg.interpreter.code_generator import CodeGenerator  # If you want to reference the code generator

# If your jtml engine is exposed via pybind11 as "import jtml_engine"
# then you must do:
import jtml_engine


class Environment:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent
    
    def set(self, name, value):
        self.vars[name] = value
    
    def get(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Variable '{name}' not defined")
    
    def exists(self, name):
        if name in self.vars:
            return True
        elif self.parent:
            return self.parent.exists(name)
        else:
            return False


class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.functions = {}
        # If you plan to actually use the CodeGenerator or Optimizer, you can instantiate them here
        # e.g. self.codegen = CodeGenerator() or self.optimizer = Optimizer()

    def interpret(self, node):
        if isinstance(node, ProgramNode):
            for stmt in node.statements:
                self.execute(stmt, self.global_env)
        else:
            raise Exception("Invalid AST root node")
    
    def execute(self, node, env):
        method_name = f'execute_{type(node).__name__}'
        executor = getattr(self, method_name, self.generic_execute)
        return executor(node, env)
    
    def generic_execute(self, node, env):
        raise NotImplementedError(f'No execute_{type(node).__name__} method')
    
    # ---------------------
    # Statement Handlers
    # ---------------------

    def execute_VariableDeclarationNode(self, node, env):
        value = self.evaluate(node.value, env)
        env.set(node.name, value)
    
    def execute_FunctionDeclarationNode(self, node, env):
        self.functions[node.name] = node
    
    def execute_ReturnStatementNode(self, node, env):
        value = self.evaluate(node.expression, env) if node.expression else None
        raise ReturnException(value)
    
    def execute_ShowStatementNode(self, node, env):
        value = self.evaluate(node.value, env)
        print(value)
    
    def execute_IfStatementNode(self, node, env):
        condition = self.evaluate(node.condition, env)
        if condition:
            new_env = Environment(env)
            for stmt in node.then_block.statements:
                self.execute(stmt, new_env)
        elif node.else_block:
            new_env = Environment(env)
            for stmt in node.else_block.statements:
                self.execute(stmt, new_env)
    
    def execute_WhileStatementNode(self, node, env):
        while self.evaluate(node.condition, env):
            new_env = Environment(env)
            for stmt in node.body.statements:
                self.execute(stmt, new_env)
    
    def execute_ForStatementNode(self, node, env):
        iterable = self.evaluate(node.iterable, env)
        for item in iterable:
            env.set(node.iterator.name, item)
            new_env = Environment(env)
            for stmt in node.body.statements:
                self.execute(stmt, new_env)
    
    def execute_ExpressionStatementNode(self, node, env):
        self.evaluate(node.expression, env)
    
    # -----------------------
    # Jtml Integration
    # -----------------------

    def execute_JTMLElementNode(self, node, env):
        """
        We have a Python-level JTMLElementNode: #tagName, attributes, content (opalg-based).
        We'll convert it to a jtml snippet string, then call the C++ jtml engine to parse + interpret.
        """
        jtml_code = self.serialize_jtml(node, env)
        # now delegate to the C++ jtml engine
        jtml_engine.interpret_string(jtml_code)

    def serialize_jtml(self, node, env):
        """
        Convert JTMLElementNode + any recognized opalg statements in 'content'
        into a single jtml snippet that the C++ engine accepts.
        E.g.: #tagName attr:"val",attr2:"val2"\\ show "Hello"\\ #tagName
        """
        snippet = f"#{node.tag_name}"
        if node.attributes:
            attr_parts = []
            for k, v in node.attributes.items():
                attr_parts.append(f'{k}:"{v}"')
            if attr_parts:
                snippet += " " + ", ".join(attr_parts)
        snippet += " \\"  # open block (like #div style:"..."\\ )

        for item in node.content:
            if isinstance(item, ShowStatementNode):
                # Evaluate the show statement's value in opalg
                text_val = self.evaluate(item.value, env)
                snippet += f'show "{text_val}"\\\\'
            elif isinstance(item, VariableDeclarationNode):
                # define varName="val"\\
                val = self.evaluate(item.value, env)
                snippet += f'define {item.name}="{val}"\\\\'
            else:
                raise NotImplementedError(
                    f"Cannot serialize {type(item).__name__} in jtml content"
                )

        snippet += f"#{node.tag_name}"
        return snippet

    # --------------------
    # Expression evaluation
    # --------------------
    
    def evaluate(self, expr, env):
        method_name = f'evaluate_{type(expr).__name__}'
        evaluator = getattr(self, method_name, self.generic_evaluate)
        return evaluator(expr, env)
    
    def generic_evaluate(self, expr, env):
        raise NotImplementedError(f'No evaluate_{type(expr).__name__} method')

    def evaluate_NumberLiteralNode(self, expr, env):
        return expr.value
    
    def evaluate_StringLiteralNode(self, expr, env):
        return expr.value
    
    def evaluate_BoolLiteralNode(self, expr, env):
        return expr.value
    
    def evaluate_IdentifierNode(self, expr, env):
        return env.get(expr.name)
    
    def evaluate_BinaryOperationNode(self, expr, env):
        left = self.evaluate(expr.left, env)
        right = self.evaluate(expr.right, env)
        if expr.op == '+':
            return left + right
        elif expr.op == '-':
            return left - right
        elif expr.op == '*':
            return left * right
        elif expr.op == '/':
            return left / right
        elif expr.op == '&&':
            return left and right
        elif expr.op == '||':
            return left or right
        elif expr.op == '==':
            return left 
