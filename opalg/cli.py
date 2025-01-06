# cli.py
import sys
from opalg.parser.parser import parser
from opalg.interpreter.interpreter import Interpreter

def main():
    """
    CLI entry point for opalg. Usage:
      poetry run opalg path/to/file.op
    or
      python cli.py path/to/file.op
    """
    if len(sys.argv) < 2:
        print("Usage: opalg <file.op>")
        sys.exit(1)

    filename = sys.argv[1]
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    # 1) Parse the OPALG source into an AST
    try:
        ast = parser.parse(source)
    except Exception as e:
        print(f"Parse error: {e}")
        sys.exit(1)

    # 2) Interpret the AST
    interpreter = Interpreter()
    try:
        interpreter.interpret(ast)
    except Exception as e:
        print(f"Runtime error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
