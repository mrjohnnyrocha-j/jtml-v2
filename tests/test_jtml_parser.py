# test_jtmlparser.py

import sys
sys.path.append('.')
import jtmlparser


def main():
    parser = jtmlparser.ParserWrapper()
    
    # Sample JTML input
    jtml_input = '#div name:"container" show "Hello, World!"\\#div'
    
    try:
        ast_node = parser.parse(jtml_input)
        ast_dict = ast_node.to_dict()
        print(ast_dict)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
