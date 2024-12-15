# interpreter/interpreter.py

from compiler.ast_nodes import *
from interpreter.optimizer import Optimizer
from interpreter.code_generator import InterpreterCodeGenerator

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
            return left == right
        elif expr.op == '!=':
            return left != right
        elif expr.op == '<':
            return left < right
        elif expr.op == '>':
            return left > right
        elif expr.op == '<=':
            return left <= right
        elif expr.op == '>=':
            return left >= right
        elif expr.op == '=':
            if isinstance(expr.left, IdentifierNode):
                env.set(expr.left.name, right)
                return right
            else:
                raise Exception("Left side of assignment must be a variable")
        else:
            raise Exception(f"Unknown binary operator {expr.op}")
    
    def evaluate_UnaryOperationNode(self, expr, env):
        operand = self.evaluate(expr.operand, env)
        if expr.op == '-':
            return -operand
        elif expr.op == '!':
            return not operand
        else:
            raise Exception(f"Unknown unary operator {expr.op}")
    
    def evaluate_FunctionCallNode(self, expr, env):
        func = expr.function.name if isinstance(expr.function, IdentifierNode) else None
        if func not in self.functions:
            raise Exception(f"Function '{func}' not defined")
        func_def = self.functions[func]
        if len(expr.arguments) != len(func_def.parameters):
            raise Exception(f"Function '{func}' expects {len(func_def.parameters)} arguments, got {len(expr.arguments)}")
        new_env = Environment(self.global_env)
        for param, arg in zip(func_def.parameters, expr.arguments):
            arg_value = self.evaluate(arg, env)
            new_env.set(param.name, arg_value)
        try:
            for stmt in func_def.body.statements:
                self.execute(stmt, new_env)
        except ReturnException as ret:
            return ret.value
        return None
    
    def execute_ClassDeclarationNode(self, node, env):
        # Implement class declaration handling
        pass
    
    # Add more execute and evaluate methods as needed

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value
