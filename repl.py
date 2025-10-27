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

while True:
    try:
        line = input(">>> ")
        tokens = lexer.tokenize(line)
        parser = Parser(tokens)
        ast = parser.parse()
        result = interpreter.visit(ast)
        print(format_value(result))
    except Exception as e:
        print(f"Error: {e}")