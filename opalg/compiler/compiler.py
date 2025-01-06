# compiler/compiler.py

from opalg.compiler.ast_nodes import *
from opalg.compiler.intermediate_representation import IntermediateRepresentation
from opalg.compiler.semantic_analyzer import SemanticAnalyzer
from opalg.interpreter.code_generator import CodeGenerator

class Compiler:
    def __init__(self):
        self.semantic_analyzer = SemanticAnalyzer()
        self.ir = IntermediateRepresentation()
        self.code_generator = CodeGenerator()
    
    def compile(self, ast_root):
        # Perform semantic analysis
        self.semantic_analyzer.analyze(ast_root)
        
        # Generate Intermediate Representation (IR)
        self.ir.generate(ast_root)
        
        # Generate target code
        self.code_generator.generate(ast_root)
        return self.code_generator.get_output()
