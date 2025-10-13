from nodes import *

class Interpreter:
    def __init__(self):
        self.variables = {}  # symbol table

    def visit(self, node):
        """Dispatch method based on node type"""
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode): 
            return node.value
        elif isinstance(node, CharNode):
            return node.value
        elif isinstance(node, IdentifierNode):
            if node.name in self.variables:
                return self.variables[node.name]
            else:
                raise NameError(f"Undefined variable '{node.name}'")
                # Raise error here
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self.eval_binop(left, node.op, right)
        elif isinstance(node, DefineNode):
            value = self.visit(node.value)
            self.variables[node.name] = value
            return value
        else:
            raise TypeError(f"Unknown node type: {type(node)}")

    def eval_binop(self, left, op, right):
        if op == "ADD":
            return left + right
        elif op == "SUB":
            return left - right
        elif op == "MUL":
            return left * right
        elif op == "DIV":
            return left / right
        elif op == "FDIV":
            return left // right
        elif op == "MOD":
            return left % right
        elif op == "POW":
            return left ** right
        elif op == "=":  # for DEFINE expressions if used as BinOpNode
            return right
        elif op == "EQ":
            return left == right
        elif op == "NEQ":
            return left != right
        elif op == "LT":
            return left < right
        elif op == "LTE":
            return left <= right
        elif op == "GT":
            return left > right
        elif op == "GTE":
            return left >= right
        elif op == "AND":
            return left and right
        elif op == "OR":
            return left or right
        elif op == "NOT":
            return not left
        else:
            raise ValueError(f"Unknown operator {op}")