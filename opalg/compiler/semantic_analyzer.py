# compiler/semantic_analyzer.py

from opalg.compiler.ast_nodes import *
from opalg.opalg_types.node_types import IntType, FloatType, StringType, BoolType, VoidType, CustomType

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
    
    def analyze(self, node):
        method_name = f'analyze_{type(node).__name__}'
        analyzer = getattr(self, method_name, self.generic_analyze)
        analyzer(node)
    
    def generic_analyze(self, node):
        raise NotImplementedError(f'No semantic analyzer for {type(node).__name__}')
    
    def analyze_ProgramNode(self, node):
        for stmt in node.statements:
            self.analyze(stmt)
    
    def analyze_VariableDeclarationNode(self, node):
        if node.name in self.symbol_table:
            raise Exception(f"Variable '{node.name}' already declared")
        var_type = self.resolve_type(node.var_type)
        value_type = self.analyze_expression(node.value)
        if var_type and not self.type_compatible(var_type, value_type):
            raise Exception(f"Type mismatch in variable '{node.name}': Expected {var_type}, got {value_type}")
        self.symbol_table[node.name] = var_type
    
    def analyze_FunctionDeclarationNode(self, node):
        if node.name in self.symbol_table:
            raise Exception(f"Function '{node.name}' already declared")
        return_type = self.resolve_type(node.return_type)
        param_types = []
        for param in node.parameters:
            param_type = self.resolve_type(param.param_type)
            param_types.append(param_type)
            self.symbol_table[param.name] = param_type
        self.symbol_table[node.name] = ('function', param_types, return_type)
        # Analyze function body
        for stmt in node.body.statements:
            self.analyze(stmt)
    
    def analyze_ReturnStatementNode(self, node):
        if node.expression:
            return self.analyze_expression(node.expression)
        return VoidType()
    
    def analyze_ShowStatementNode(self, node):
        self.analyze_expression(node.value)
    
    def analyze_IfStatementNode(self, node):
        condition_type = self.analyze_expression(node.condition)
        if not isinstance(condition_type, BoolType):
            raise Exception("Condition in if statement must be of type bool")
        for stmt in node.then_block.statements:
            self.analyze(stmt)
        if node.else_block:
            for stmt in node.else_block.statements:
                self.analyze(stmt)
    
    def analyze_WhileStatementNode(self, node):
        condition_type = self.analyze_expression(node.condition)
        if not isinstance(condition_type, BoolType):
            raise Exception("Condition in while statement must be of type bool")
        for stmt in node.body.statements:
            self.analyze(stmt)
    
    def analyze_ForStatementNode(self, node):
        iterable_type = self.analyze_expression(node.iterable)
        # Assume iterable is of some iterable type
        for stmt in node.body.statements:
            self.analyze(stmt)
    
    def analyze_expression(self, expr):
        method_name = f'analyze_expr_{type(expr).__name__}'
        analyzer = getattr(self, method_name, self.generic_analyze_expression)
        return analyzer(expr)
    
    def generic_analyze_expression(self, expr):
        raise NotImplementedError(f'No semantic analyzer for expression {type(expr).__name__}')
    
    def analyze_expr_BinaryOperationNode(self, expr):
        left_type = self.analyze_expression(expr.left)
        right_type = self.analyze_expression(expr.right)
        if expr.op in ['+', '-', '*', '/']:
            if isinstance(left_type, (IntType, FloatType)) and isinstance(right_type, (IntType, FloatType)):
                return FloatType() if isinstance(left_type, FloatType) or isinstance(right_type, FloatType) else IntType()
            else:
                raise Exception(f"Unsupported operand types for {expr.op}: {left_type} and {right_type}")
        elif expr.op in ['&&', '||']:
            if isinstance(left_type, BoolType) and isinstance(right_type, BoolType):
                return BoolType()
            else:
                raise Exception(f"Logical operators require bool types, got {left_type} and {right_type}")
        elif expr.op in ['==', '!=', '<', '>', '<=', '>=']:
            if self.type_compatible(left_type, right_type):
                return BoolType()
            else:
                raise Exception(f"Comparison requires compatible types, got {left_type} and {right_type}")
        elif expr.op == '=':
            if isinstance(expr.left, IdentifierNode):
                var_name = expr.left.name
                if var_name not in self.symbol_table:
                    raise Exception(f"Variable '{var_name}' not declared")
                var_type = self.symbol_table[var_name]
                if not self.type_compatible(var_type, right_type):
                    raise Exception(f"Type mismatch in assignment to '{var_name}': Expected {var_type}, got {right_type}")
                return var_type
            else:
                raise Exception("Left side of assignment must be a variable")
        else:
            raise Exception(f"Unknown binary operator {expr.op}")
    
    def analyze_expr_UnaryOperationNode(self, expr):
        operand_type = self.analyze_expression(expr.operand)
        if expr.op == '-':
            if isinstance(operand_type, (IntType, FloatType)):
                return operand_type
            else:
                raise Exception("Unary '-' operator requires int or float type")
        elif expr.op == '!':
            if isinstance(operand_type, BoolType):
                return BoolType()
            else:
                raise Exception("Unary '!' operator requires bool type")
        else:
            raise Exception(f"Unknown unary operator {expr.op}")
    
    def analyze_expr_NumberLiteralNode(self, expr):
        if isinstance(expr.value, int):
            return IntType()
        elif isinstance(expr.value, float):
            return FloatType()
    
    def analyze_expr_StringLiteralNode(self, expr):
        return StringType()
    
    def analyze_expr_BoolLiteralNode(self, expr):
        return BoolType()
    
    def analyze_expr_IdentifierNode(self, expr):
        var_name = expr.name
        if var_name not in self.symbol_table:
            raise Exception(f"Variable '{var_name}' not declared")
        var_type = self.symbol_table[var_name]
        if isinstance(var_type, tuple) and var_type[0] == 'function':
            raise Exception(f"'{var_name}' is a function, not a variable")
        return var_type
    
    def analyze_expr_FunctionCallNode(self, expr):
        func_name = expr.function.name if isinstance(expr.function, IdentifierNode) else None
        if not func_name or func_name not in self.symbol_table:
            raise Exception(f"Function '{func_name}' not declared")
        func_info = self.symbol_table[func_name]
        if not isinstance(func_info, tuple) or func_info[0] != 'function':
            raise Exception(f"'{func_name}' is not a function")
        param_types = func_info[1]
        return_type = func_info[2]
        if len(param_types) != len(expr.arguments):
            raise Exception(f"Function '{func_name}' expects {len(param_types)} arguments, got {len(expr.arguments)}")
        for i, arg in enumerate(expr.arguments):
            arg_type = self.analyze_expression(arg)
            if not self.type_compatible(param_types[i], arg_type):
                raise Exception(f"Type mismatch in argument {i+1} of function '{func_name}': Expected {param_types[i]}, got {arg_type}")
        return return_type
    
    def analyze_expr_MemberAccessNode(self, expr):
        # Implement member access type analysis
        # For simplicity, assume all members are of type string
        self.analyze_expression(expr.obj)
        return StringType()
    
    def analyze_expr_AwaitExpressionNode(self, expr):
        # Implement await expression type analysis
        return VoidType()
    
    def resolve_type(self, type_node):
        if isinstance(type_node, IntType):
            return IntType()
        elif isinstance(type_node, FloatType):
            return FloatType()
        elif isinstance(type_node, StringType):
            return StringType()
        elif isinstance(type_node, BoolType):
            return BoolType()
        elif isinstance(type_node, VoidType):
            return VoidType()
        elif isinstance(type_node, CustomType):
            return type_node
        elif isinstance(type_node, TypeNode):
            # Resolve generic types if necessary
            return type_node
        else:
            return None
    
    def type_compatible(self, expected, actual):
        if isinstance(expected, type(actual)):
            return True
        # Allow int to float promotion
        if isinstance(expected, FloatType) and isinstance(actual, IntType):
            return True
        return False
