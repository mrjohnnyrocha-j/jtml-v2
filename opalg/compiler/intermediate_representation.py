# compiler/intermediate_representation.py

from opalg.compiler.ast_nodes import *

class IntermediateRepresentation:
    def __init__(self):
        self.instructions = []
    
    def generate(self, node):
        method_name = f'ir_{type(node).__name__}'
        generator = getattr(self, method_name, self.generic_ir)
        generator(node)
    
    def generic_ir(self, node):
        raise NotImplementedError(f'No IR generator for {type(node).__name__}')
    
    def ir_ProgramNode(self, node):
        for stmt in node.statements:
            self.generate(stmt)
    
    def ir_VariableDeclarationNode(self, node):
        # Example IR instruction for variable declaration
        self.instructions.append(('DECLARE', node.name, node.var_type, node.value))
    
    def ir_FunctionDeclarationNode(self, node):
        # Example IR instruction for function declaration
        self.instructions.append(('FUNC_DECL', node.name, node.parameters, node.return_type))
        for stmt in node.body.statements:
            self.generate(stmt)
        self.instructions.append(('FUNC_END', node.name))
    
    def ir_ReturnStatementNode(self, node):
        self.instructions.append(('RETURN', node.expression))
    
    def ir_ShowStatementNode(self, node):
        self.instructions.append(('SHOW', node.value))
    
    def ir_IfStatementNode(self, node):
        self.instructions.append(('IF', node.condition))
        for stmt in node.then_block.statements:
            self.generate(stmt)
        if node.else_block:
            self.instructions.append(('ELSE',))
            for stmt in node.else_block.statements:
                self.generate(stmt)
        self.instructions.append(('ENDIF',))
    
    def ir_WhileStatementNode(self, node):
        self.instructions.append(('WHILE', node.condition))
        for stmt in node.body.statements:
            self.generate(stmt)
        self.instructions.append(('ENDWHILE',))
    
    def ir_ForStatementNode(self, node):
        self.instructions.append(('FOR', node.iterator, node.iterable))
        for stmt in node.body.statements:
            self.generate(stmt)
        self.instructions.append(('ENDFOR',))
    
    # Add IR generation methods for other AST nodes as needed
