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

with open("example.gill", "r") as file:
    code = file.read()  # read the whole file as one string

try:
    tokens = lexer.tokenize(code)
    parser = Parser(tokens)
    ast = parser.parse() # parse the entire program
    result = format_value(interpreter.visit(ast))
except Exception as e:
    print(interpreter.global_env.functions)
    print(f"Error: {e}")


