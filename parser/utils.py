# parser/utils.py

from compiler.ast_nodes import ReturnStatementNode, IfStatementNode, WhileStatementNode, ForStatementNode

def has_return_statement(statements):
    """
    Recursively checks for a return statement in the given list of statements.
    """
    for stmt in statements:
        print(f"Checking statement: {stmt}")
        if isinstance(stmt, ReturnStatementNode):
            print("Found a return statement.")
            return True
        elif isinstance(stmt, IfStatementNode):
            print("Checking if statement branches for return statements.")
            if stmt.then_block and has_return_statement(stmt.then_block.statements):
                return True
            if stmt.else_block and has_return_statement(stmt.else_block.statements):
                return True
        elif isinstance(stmt, WhileStatementNode) or isinstance(stmt, ForStatementNode):
            print("Checking loop body for return statements.")
            if has_return_statement(stmt.body.statements):
                return True
    print("Did not find a return statement. Function syntax not valid.")
    return False
