# interpreter/optimizer.py

from compiler.ast_nodes import *

class Optimizer:
    def __init__(self):
        pass
    
    def optimize(self, node):
        method_name = f'optimize_{type(node).__name__}'
        optimizer = getattr(self, method_name, self.generic_optimize)
        return optimizer(node)
    
    def generic_optimize(self, node):
        return node
    
    def optimize_ProgramNode(self, node):
        node.statements = [self.optimize(stmt) for stmt in node.statements]
        return node
    
    def optimize_VariableDeclarationNode(self, node):
        node.value = self.optimize(node.value)
        return node
    
    def optimize_BinaryOperationNode(self, node):
        node.left = self.optimize(node.left)
        node.right = self.optimize(node.right)
        # Example: constant folding
        if isinstance(node.left, NumberLiteralNode) and isinstance(node.right, NumberLiteralNode):
            result = self.fold_constants(node.op, node.left.value, node.right.value)
            return NumberLiteralNode(result)
        return node
    
    def fold_constants(self, op, left, right):
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left / right
        elif op == '==':
            return left == right
        elif op == '!=':
            return left != right
        elif op == '<':
            return left < right
        elif op == '>':
            return left > right
        elif op == '<=':
            return left <= right
        elif op == '>=':
            return left >= right
        elif op == '&&':
            return left and right
        elif op == '||':
            return left or right
        else:
            return None
    # Add more optimization methods as needed
