from parser import Parser
from lexer import Lexer
from interpreter import Interpreter

lexer = Lexer()
Interpreter = Interpreter()

while True:
    try:
        text = input(">>> ")
        tokens = lexer.tokenize(text)
        parser = Parser(tokens)
        ast = parser.parse()
        result = Interpreter.visit(ast)
        print(result)  # Print symbol table after each operation)
    except Exception as e:
        print(e)
        break

