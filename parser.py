from nodes import *
from tokenclass import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current_token(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, kind):
        token: Token = self.current_token()
        if token and token.kind == kind:
            self.position += 1
            return token
        raise SyntaxError(f"Expected token {kind}, got {token}")

    # --- Parsing entry point ---
    def parse(self):
        token: Token = self.current_token()
        if token is None:
            return None
        if token.kind == "DEFINE":
            return self.parse_define()
        else:
            return self.parse_boolean()

    # --- DEFINE num INT 301 ---
    def parse_define(self):
        self.eat("DEFINE")
        name = self.eat("IDENTIFIER").value
        type_token = self.eat("TYPE").value
        value_node = self.parse_expr()
        return DefineNode(name, type_token, value_node)

    # --- Expression grammar ---
    # expr   -> term ((ADD|SUB) term)*
    # term   -> factor ((MUL|DIV|FDIV) factor)*
    # factor -> NUMBER | IDENTIFIER | '(' expr ')'

    def parse_expr(self):
        node = self.parse_term()
        while self.current_token() and self.current_token().kind in ("ADD", "SUB"):
            op = self.eat(self.current_token().kind).kind
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token() and self.current_token().kind in ("MUL", "DIV", "FDIV"):
            op = self.eat(self.current_token().kind).kind
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node
    
    def parse_boolean(self):
        node = self.parse_expr()
        while self.current_token() and self.current_token().kind in ("EQ", "NEQ", "LT", "LTE", "GT", "GTE", "AND", "OR"):
            op = self.eat(self.current_token().kind).kind
            right = self.parse_expr()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        token = self.current_token()

        if token.kind == "NUMBER":
            self.eat("NUMBER")
            return NumberNode(token.value)
        elif token.kind == "IDENTIFIER":
            self.eat("IDENTIFIER")
            return IdentifierNode(token.value)
        elif token.kind == "STRING":
            self.eat("STRING")
            return StringNode(token.value)
        elif token.kind == "CHAR":
            self.eat("CHAR")
            return CharNode(token.value)
        elif token.kind == "LPAREN":
            self.eat("LPAREN")
            node = self.parse_boolean()
            self.eat("RPAREN")
            return node
        else:
            raise SyntaxError(f"Unexpected token {token}")
        