class ASTNode:
    pass

class CastNode(ASTNode):
    def __init__(self, target_type: str, expression):
        self.target_type = target_type
        self.expression = expression

    def __repr__(self):
        return f"CastNode(to={self.target_type}, expr={self.expression})"

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value
        self.type_ = "INT" if isinstance(value, int) else "FLOAT"

    def __repr__(self):
        return f"NumberNode({self.type_}:{self.value})"

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"IdentifierNode({self.name})"
    
class NullableIdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"NullableIdentifierNode({self.name})"

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringNode({self.value})"
    
class BooleanNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"BooleanNode({self.value})"

class CharNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"CharNode({self.value})"
    
class DefineNode(ASTNode):
    def __init__(self, name, type_, value):
        self.name = name
        self.type_ = type_
        self.value = value

class AssignNode(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"DefineNode(name={self.name}, type={self.type_}, value={self.value})"

class BinOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"BinOpNode({self.left}, {self.op}, {self.right})"
    
class IncNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"IncNode({self.identifier})"

class DecNode(ASTNode):
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"DecNode({self.identifier})"
    
class UnaryOpNode(ASTNode):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

# Blocks for control flow, logic and loops, functions and classes, etc...

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements

class IfBlockNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block # Also considered an "else" block

class WhileBlockNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

# Keywords for output and input...

class OutputNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression