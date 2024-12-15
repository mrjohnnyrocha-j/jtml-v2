# code_generator.py

from compiler.ast_nodes import *
import sys

class CodeGenerator:
    def __init__(self):
        self.output = []
    
    def generate(self, node):
        method_name = f'generate_{type(node).__name__}'
        generator = getattr(self, method_name, self.generic_generate)
        generator(node)
    
    def generic_generate(self, node):
        raise NotImplementedError(f'No generate_{type(node).__name__} method')
    
    def generate_ProgramNode(self, node):
        for statement in node.statements:
            self.generate(statement)
    
    def generate_VariableDeclarationNode(self, node):
        var_type = self.get_type(node.var_type) if node.var_type else 'var'
        const = 'const ' if node.const else ''
        value = self.generate_expression(node.value)
        self.output.append(f'{const}{var_type} {node.name} = {value};')
    
    def generate_FunctionDeclarationNode(self, node):
        async_prefix = 'async ' if node.async_function else ''
        return_type = self.get_type(node.return_type)
        params = ', '.join([f'{self.get_type(param.param_type)} {param.name}' for param in node.parameters])
        self.output.append(f'{async_prefix}function {node.name}({params}): {return_type} {{')
        for stmt in node.body.statements:
            self.generate(stmt)
        self.output.append('}')
    
    def generate_ReturnStatementNode(self, node):
        if node.expression:
            expr = self.generate_expression(node.expression)
            self.output.append(f'return {expr};')
        else:
            self.output.append('return;')
    
    def generate_ShowStatementNode(self, node):
        expr = self.generate_expression(node.value)
        self.output.append(f'show({expr});')
    
    def generate_SaveStatementNode(self, node):
        expr = self.generate_expression(node.expression)
        self.output.append(f'save({node.identifier}, {expr});')
    
    def generate_DeleteStatementNode(self, node):
        self.output.append(f'delete({node.identifier});')
    
    def generate_IfStatementNode(self, node):
        condition = self.generate_expression(node.condition)
        self.output.append(f'if ({condition}) {{')
        for stmt in node.then_block.statements:
            self.generate(stmt)
        self.output.append('}')
        if node.else_block:
            self.output.append('else {')
            for stmt in node.else_block.statements:
                self.generate(stmt)
            self.output.append('}')
    
    def generate_WhileStatementNode(self, node):
        condition = self.generate_expression(node.condition)
        self.output.append(f'while ({condition}) {{')
        for stmt in node.body.statements:
            self.generate(stmt)
        self.output.append('}')
    
    def generate_ForStatementNode(self, node):
        iterable = self.generate_expression(node.iterable)
        self.output.append(f'for (let {node.iterator.name} of {iterable}) {{')
        for stmt in node.body.statements:
            self.generate(stmt)
        self.output.append('}')
    
    def generate_expression_statement(self, node):
        expr = self.generate_expression(node.expression)
        self.output.append(f'{expr};')
    
    def generate_expression(self, expr):
        method_name = f'generate_expr_{type(expr).__name__}'
        generator = getattr(self, method_name, self.generic_generate_expression)
        return generator(expr)
    
    def generic_generate_expression(self, expr):
        raise NotImplementedError(f'No generate_expr_{type(expr).__name__} method')
    
    def generate_expr_BinaryOperationNode(self, expr):
        left = self.generate_expression(expr.left)
        right = self.generate_expression(expr.right)
        return f'({left} {expr.op} {right})'
    
    def generate_expr_UnaryOperationNode(self, expr):
        operand = self.generate_expression(expr.operand)
        return f'({expr.op}{operand})'
    
    def generate_expr_NumberLiteralNode(self, expr):
        return str(expr.value)
    
    def generate_expr_StringLiteralNode(self, expr):
        return f'"{expr.value}"'
    
    def generate_expr_BoolLiteralNode(self, expr):
        return 'true' if expr.value else 'false'
    
    def generate_expr_IdentifierNode(self, expr):
        return expr.name
    
    def generate_expr_FunctionCallNode(self, expr):
        func = self.generate_expression(expr.function)
        args = ', '.join([self.generate_expression(arg) for arg in expr.arguments])
        return f'{func}({args})'
    
    def generate_expr_MemberAccessNode(self, expr):
        obj = self.generate_expression(expr.obj)
        return f'{obj}.{expr.member}'
    
    def generate_expr_AwaitExpressionNode(self, expr):
        return f'await {self.generate_expression(expr.expression)}'
    
    def get_type(self, type_node):
        if isinstance(type_node, VoidType):
            return 'void'
        elif isinstance(type_node, IntType):
            return 'int'
        elif isinstance(type_node, FloatType):
            return 'float'
        elif isinstance(type_node, StringType):
            return 'string'
        elif isinstance(type_node, BoolType):
            return 'bool'
        elif isinstance(type_node, CustomType):
            return type_node.name
        elif isinstance(type_node, TypeNode):
            generic = ', '.join([self.get_type(arg) for arg in type_node.generic_args])
            return f'{type_node.name}<{generic}>'
        else:
            return 'var'
    
    def get_output(self):
        return '\n'.join(self.output)
    
    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.get_output())
    
    # Additional methods for other AST nodes can be added here
