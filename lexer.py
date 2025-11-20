import re
from tokenclass import Token

class Lexer:
    def __init__(self):
        self.position = 0
        self.current_char = None
        self.text = ""
        self.tokens = []
        self.token_specs = [
            ("OUTPUT", r"out"),
            ("IF", r"if"),
            ("ELSE", r"else"),
            ("WHILE", r"while"),
            ("FOR", r"for"),
            ("FOREACH", r"foreach"),
            ("DEFINE", r"define"),
            ("ASSIGN", r"assign"),
            ("FUNCTION", r"function"),
            ("DEFAULT", r"default"),
            ("RETURN", r"return"),
            ("TYPE", r"int|float|string|char|bool|void"),
            ("CAST", r"\((int|float|string|char|bool|void)\)"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("STRING", r'"[^"]*"'),
            ("CHAR", r"'.'"),
            # ("NULLABLEID", r"\??[A-Za-z_][A-Za-z0-9_]*"),
            ("INC", r"\+\+"),
            ("DEC", r"--"),  
            ("EXECUTE", r"exec"),         
            ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
            ("COMMENT", r";"),
            ("COMMA", r","),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("LCBRACE", r"\{"),
            ("RCBRACE", r"\}"),
            ("LBRACKET", r"\["),
            ("RBRACKET", r"\]"),
            ("COLON", r":"),
            ("SEMICOLON", r";"),
            ("ADD", r"\+"),
            ("SUB", r"-"),
            ("MUL", r"\*"),
            ("DIV", r"/"),
            ("FDIV", r"//"),
            ("MOD", r"%"),
            ("EQ", r"=="),
            ("NEQ", r"!="),
            ("LT", r"<"),
            ("LTE", r"<="),
            ("GT", r">"),
            ("GTE", r">="),
            ("AND", r"&&"),
            ("OR", r"\|\|"),
            ("NOT", r"!"),
            ("WHITESPACE", r"\s+"),
            ("NEWLINE", r"\n")
        ]

        self.token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_specs)

    def tokenize(self, text):
        # Remove semicolon comments
        text = re.sub(r";[^\n]*", "", text)
        self.text = text
        self.position = 0
        self.tokens = []
        line_num = 1
        line_start = 0

        for match in re.finditer(self.token_regex, text):
            kind = match.lastgroup
            value = match.group()
            column = match.start() - line_start + 1
            if kind in ("WHITESPACE", "NEWLINE"):
                line_num += 1
                line_start = match.end()
                continue
            elif kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "STRING":
                value = value[1:-1]  # Remove quotes
            elif kind == "CHAR":
                value = value[1]  # Remove quotes
            elif kind == "CAST":
                value = value[1:-1].lower()  # turn "(string)" into "string", "(int)" into "int", etc.
            elif kind == "IDENTIFIER":
                if value == "true":
                    kind = "BOOLEAN"
                    value = "true"
                elif value == "false":
                    kind = "BOOLEAN"
                    value = "false"

            self.tokens.append(Token(kind, value, line_num, column))

        return self.tokens