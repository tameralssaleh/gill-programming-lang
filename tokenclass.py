
class Token:
    def __init__(self, kind, value):
        self.kind = kind
        self.value = value

    def __repr__(self):
        return f"Token<kind:{self.kind}, value:{self.value}>"