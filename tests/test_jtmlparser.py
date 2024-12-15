# test_jtmlparser.py

import jtmlparser

def main():
    parser = jtmlparser.ParserWrapper()
    jtml_code = '#p name:"container"\\ show "Hello, World!"\\\\#p'
    try:
        ast_node = parser.parse(jtml_code)
        ast_dict = ast_node.to_dict()
        print(ast_dict)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
