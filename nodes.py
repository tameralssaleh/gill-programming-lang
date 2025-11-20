from environment import Env

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
    def __init__(self, name, declared_type=None):
        self.name = name
        self.declared_type = declared_type

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
        self.false_block = false_block # Also considered an "else" block.

class WhileLoopNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class ForLoopNode(ASTNode):
    def __init__(self, initializer, condition, increment, body):
        self.initializer = initializer
        self.condition = condition
        self.increment = increment
        self.body = body

class ForEachLoopNode(ASTNode):
    def __init__(self, iterator, iterable, body):
        self.iterator = iterator
        self.iterable = iterable
        self.body = body

# Blocks for functions...

class ParameterNode(ASTNode):
    def __init__(self, name, type_):
        self.name = name
        self.type_ = type_
        self.default_value = None  # Optional default value for the parameter

class FunctionDefinitionNode(ASTNode):
    def __init__(self, name, parameters, body, return_type):
        self.name = name
        self.parameters: list[ParameterNode] = parameters
        self.local_environment: Env = None # Defined later in the interpreter. Stores the functions local variables including parameter values.
        self.global_environment: Env = None # Defined later in the interpreter. Points to the global environment where the function was defined.
        self.body: BlockNode = body
        self.return_type = None if return_type == "void" or return_type == "VOID" else return_type

class FunctionCallNode(ASTNode):
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

# Keywords for return, break, continue, etc...

class ReturnNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

# Keywords for output and input...

class OutputNode(ASTNode):
    def __init__(self, expression):
        self.expression = expression

# Nodes for arrays & other data structures...

class ArrayNode(ASTNode):
    def __init__(self, elements, size):
        self.elements = elements
        self.size = size

    def __repr__(self):
        return f"ArrayNode(size={self.size})"