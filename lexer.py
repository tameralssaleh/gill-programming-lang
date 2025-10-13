import re
from tokenclass import Token

class Lexer:
    def __init__(self):
        self.position = 0
        self.current_char = None
        self.text = ""
        self.tokens = []
        self.token_specs = [
            ("DEFINE", r"DEFINE"),
            ("TYPE", r"INT|FLOAT|STRING|CHAR"),
            ("NUMBER", r"\d+(\.\d*)?"),
            ("STRING", r'"[^"]*"'),
            ("CHAR", r"'.'"),
            ("IDENTIFIER", r"[A-Za-z_][A-Za-z0-9_]*"),
            ("COMMENT", r";"),
            ("LPAREN", r"\("),
            ("RPAREN", r"\)"),
            ("COMMA", r","),
            ("ADD", r"\+"),
            ("SUB", r"-"),
            ("MUL", r"\*"),
            ("DIV", r"/"),
            ("FDIV", r"//"),
            ("MOD", r"%"),
            ("POW", r"\^"),
            ("EQ", r"=="),
            ("NEQ", r"!="),
            ("LT", r"<"),
            ("LTE", r"<="),
            ("GT", r">"),
            ("GTE", r">="),
            ("AND", r"&&"),
            ("OR", r"\|\|"),
            ("NOT", r"!"),
            ("ASSIGN", r"="),
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

        for match in re.finditer(self.token_regex, text):
            kind = match.lastgroup
            value = match.group()
            if kind in ("WHITESPACE", "NEWLINE"):
                continue
            elif kind == "NUMBER":
                value = float(value) if '.' in value else int(value)
            elif kind == "STRING":
                value = value[1:-1]  # Remove quotes
            elif kind == "CHAR":
                value = value[1]  # Remove quotes
            self.tokens.append(Token(kind, value))

        return self.tokens