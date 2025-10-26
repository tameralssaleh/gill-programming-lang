from nodes import *
from tokenclass import Token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    @property
    def current_token(self) -> Token:
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def eat(self, kind):
        token: Token = self.current_token
        if token and token.kind == kind:
            self.position += 1
            return token
        raise SyntaxError(f"Expected token {kind}, got {token}")

    def parse(self):
        statements = []
        while self.current_token is not None:
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
        return BlockNode(statements)

    def parse_define(self):
        self.eat("DEFINE")
        name = self.eat("IDENTIFIER").value
        type_token = self.eat("TYPE").value
        value_node = self.parse_expr()
        return DefineNode(name, type_token, value_node)
    
    def parse_assign(self):
        self.eat("ASSIGN")
        name = self.eat("IDENTIFIER").value
        value_node = self.parse_expr()
        return AssignNode(name, value_node)
    
    def parse_casting(self):
        cast_token = self.eat("CAST").value
        expr_node = self.parse_expr()
        # Cast token would be the target type...
        return CastNode(cast_token, expr_node)

    # --- Expression grammar ---
    # expr   -> term ((ADD|SUB) term)*
    # term   -> factor ((MUL|DIV|FDIV) factor)*
    # factor -> NUMBER | IDENTIFIER | '(' expr ')'

    def parse_expr(self):
        node = self.parse_term()
        while self.current_token and self.current_token.kind in ("ADD", "SUB"):
            op = self.eat(self.current_token.kind).kind
            right = self.parse_term()
            node = BinOpNode(node, op, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token and self.current_token.kind in ("MUL", "DIV", "FDIV"):
            op = self.eat(self.current_token.kind).kind
            right = self.parse_factor()
            node = BinOpNode(node, op, right)
        return node
    
    def parse_boolean(self):
        node = self.parse_expr()
        while self.current_token and self.current_token.kind in ("EQ", "NEQ", "LT", "LTE", "GT", "GTE", "AND", "OR"):
            op = self.eat(self.current_token.kind).kind
            right = self.parse_expr()
            node = BinOpNode(node, op, right)
        return node

    def parse_factor(self):
        token = self.current_token

        if token.kind == "NUMBER":
            self.eat("NUMBER")
            return NumberNode(token.value)
        
        elif token.kind == "IDENTIFIER":
            self.eat("IDENTIFIER")
            variable_name = token.value

            if self.check("INC"):
                self.eat("INC")
                return IdentifierNode(variable_name)
            
            elif self.check("DEC"):
                self.eat("DEC")
                return IdentifierNode(variable_name)
            
            return IdentifierNode(variable_name)
        
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
        
        elif token.kind == "BOOLEAN":
            self.eat("BOOLEAN")
            return BooleanNode(token.value)
        
        elif token.kind == "NOT":
            op = self.eat("NOT").kind
            operand = self.parse_factor()
            return UnaryOpNode(op, operand)
        
        elif token.kind == "OUTPUT":
            self.eat("OUTPUT")
            return OutputNode(token.value)
        
        elif token.kind == "CAST":
            return self.parse_casting()

        else:
            raise SyntaxError(f"Unexpected token {token}")
        
    def parse_output_expr(self):
        expr_node = self.parse_expr()
        return OutputNode(expr_node)
        
    def expect(self, kind):
        if self.current_token.kind != kind:
            raise SyntaxError(f"Expected {kind}, got {self.current_token.kind}\nError @ {self.current_token.line}:{self.current_token.column}")
        token = self.current_token
        self.position += 1
        return token

    def check(self, kind):
        """Return True if the current token matches `kind`."""
        return self.current_token is not None and self.current_token.kind == kind
    
    def peek(self, offset=1):
        pos = self.position + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def parse_if(self):
        self.eat("IF")
        condition = self.parse_boolean()
        true_block = self.parse_block()
        false_block = None

        # Check the current token AFTER the true block
        if self.current_token and self.current_token.kind == "ELSE":
            false_block = self.parse_else()

        return IfBlockNode(condition, true_block, false_block)

    def parse_else(self):
        self.eat("ELSE")
        return self.parse_block()

    def parse_while(self):
        self.eat("WHILE")
        condition = self.parse_boolean()
        body = self.parse_block()
        return WhileBlockNode(condition, body)
    
    def parse_statement(self):
        tok = self.current_token

        if tok.kind == "DEFINE":
            return self.parse_define()
        elif tok.kind == "IDENTIFIER":
            next_tok = self.peek()
            if next_tok and next_tok.kind == "INC":
                var_name = tok.value
                self.eat("IDENTIFIER")
                self.eat("INC")
                return IncNode(var_name)
            elif next_tok and next_tok.kind == "DEC":
                var_name = tok.value
                self.eat("IDENTIFIER")
                self.eat("DEC")
                return DecNode(var_name)
            else:
                return self.parse_assign()
            
        elif tok.kind == "LCBRACE":
            return self.parse_block()
        elif tok.kind == "OUTPUT":
            self.eat("OUTPUT")
            return self.parse_output_expr()
        else:
            raise SyntaxError(f"Unexpected token {tok}")

    def parse_block(self):
        self.expect("LCBRACE")
        statements = []

        while not self.check("RCBRACE"):
            stmt = self.parse_statement()  # <--- uses the new LCBBRACE case
            if stmt:
                statements.append(stmt)

        self.expect("RCBRACE")
        return BlockNode(statements)
