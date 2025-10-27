from parser import Parser
from lexer import Lexer
from interpreter import Interpreter
from environment import Env

lexer = Lexer()
global_env = Env()
interpreter = Interpreter(global_env)

def format_value(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)

# for ex in example_code:
#     try:
#         tokens = lexer.tokenize(ex)
#         parser = Parser(tokens)
#         ast = parser.parse()
#         result = interpreter.visit(ast)
#         print(format_value(result))
#     except Exception as e:
#         result = f"Error: {e}"
#         print(result)

with open("example.xs", "r") as file:
    code = file.read()  # read the whole file as one string

try:
    tokens = lexer.tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse() # parse the entire program
    result = format_value(interpreter.visit(ast))
    for token in tokens:
        print(token)
except Exception as e:
    print(f"Error: {e}")
