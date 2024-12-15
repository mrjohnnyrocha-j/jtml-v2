import unittest
from parser.parser import parser
from compiler.ast_nodes import JTMLElementNode, ShowStatementNode, VariableDeclarationNode
import jtmlparser

class TestJTMLElementCppIntegration(unittest.TestCase):
    def setUp(self):
        self.parser = parser

    def parse_code(self, code):
        return self.parser.parse(code)

    def test_jtml_element_with_dynamic_content_cpp(self):
        # JTML Code:
        # define userName = "Alice"\\
        # #p
        #     show "Welcome, #(userName)"\\
        # #
        code = (
            r'define userName = "Alice"\\ #p     show "Welcome, #(userName)"\\ #p'
        )

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

        show_stmt = p_stmt.content[0]
        self.assertIsInstance(show_stmt, ShowStatementNode)
        self.assertEqual(show_stmt.value, "Welcome, #(userName)")
