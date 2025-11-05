from nodes import *
from environment import Env

class Interpreter:
    def __init__(self, global_env: Env):
        self.global_env: Env = global_env

    def visit(self, node):
        """Dispatch method based on node type"""
        if isinstance(node, NumberNode):
            return node.value
        elif isinstance(node, StringNode): 
            return node.value
        elif isinstance(node, CharNode):
            return node.value
        elif isinstance(node, BooleanNode):
            return self.eval_boolean(node.value)
        elif isinstance(node, CastNode):
            target_type = node.target_type.lower()
            
            if node.expression in self.global_env.variables: # Check if the expression is an identifier/variable
                value = self.global_env.variables[node.expression]
            else:
                value = self.visit(node.expression)

            if target_type == "int":
                return int(value)
            elif target_type == "float":
                return float(value)
            elif target_type == "string":
                return str(value)
            elif target_type == "char":
                return str(value)[0]  # take first character
            elif target_type == "bool":
                return bool(value)
            elif target_type == "void":
                return None
            else:
                raise ValueError(f"Unknown cast type: {target_type}")        
        elif isinstance(node, IdentifierNode):
            if node.name in self.global_env.variables:
                return self.global_env.variables[node.name]
            else:
                raise NameError(f"Undefined variable '{node.name}'")
        elif isinstance(node, BinOpNode):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return self.eval_binop(left, node.op, right)
        elif isinstance(node, UnaryOpNode):
            value = self.visit(node.operand)
            if node.op == "NOT":
                return not value
            else:
                raise ValueError(f"Unknown unary operator {node.op}") 
        elif isinstance(node, IncNode):
            if node.identifier in self.global_env.variables:
                self.global_env.variables[node.identifier] += 1
                return self.global_env.variables[node.identifier]
            else:
                raise NameError(f"Undefined variable '{node.identifier}'")
        elif isinstance(node, DecNode):
            if node.identifier in self.global_env.variables:
                self.global_env.variables[node.identifier] -= 1
                return self.global_env.variables[node.identifier]
            else:
                raise NameError(f"Undefined variable '{node.identifier}'")
        elif isinstance(node, IfBlockNode):
            condition = self.visit(node.condition)
            if condition:
                return self.visit(node.true_block)
            elif node.false_block:
                return self.visit(node.false_block)
            return None
        elif isinstance(node, WhileBlockNode):
            while self.visit(node.condition):
                self.visit(node.body)  # just execute the body, ignore the return
        elif isinstance(node, OutputNode):
            value = self.visit(node.expression)
            print(value)
            return value  # or None
        elif isinstance(node, DefineNode):
            value = self.visit(node.value)
            self.global_env.variables[node.name] = value
            return value
        elif isinstance(node, AssignNode):
            value = self.visit(node.value)
            if node.name in self.global_env.variables:
                self.global_env.variables[node.name] = value
                return value
            else:
                raise NameError(f"Undefined variable '{node.name}' must be defined before assignment.")
        elif isinstance(node, BlockNode):
            last_result = None
            for stmt in node.statements:
                last_result = self.visit(stmt)  # OutputNode prints internally
            return last_result
        elif isinstance(node, FunctionDefinitionNode):
            # Store the function definition in the global environment
            self.global_env.functions[node.name] = node
            function_env = Env()
            node.local_environment = function_env
            node.global_environment = self.global_env
            if node.parameters:
                for param in node.parameters:
                    if param.default_value is not None:
                        function_env.variables[param.name] = self.visit(param.default_value)
                    else:
                        function_env.variables[param.name] = None  # Initialize parameters to None
            return None
        elif isinstance(node, FunctionCallNode):
            if node.name not in self.global_env.functions:
                raise NameError(f"Undefined function '{node.name}'")
            
            func_def: FunctionDefinitionNode = self.global_env.functions[node.name]

            # Create a new environment for the call
            call_env = Env(parent=func_def.local_environment)

            # Evaluate and bind arguments
            for i, arg_node in enumerate(node.arguments):
                arg_value = self.visit(arg_node)
                param_name = func_def.parameters[i].name
                call_env.variables[param_name] = arg_value

            prev_env = self.global_env
            self.global_env = call_env
            try:
                result = None
                for stmt in func_def.body.statements:
                    result = self.visit(stmt)
                return result
            finally:
                self.global_env = prev_env

        elif isinstance(node, ReturnNode):
            return self.visit(node.expression)

    
    def eval_binop(self, left, op, right):
        if op == "ADD":
            if isinstance(left, str) or isinstance(right, str):
                return str(left) + str(right)
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
            return bool(left) and bool(right)
        elif op == "OR":
            return bool(left) or bool(right)
        elif op == "NOT":
            return not left
        else:
            raise ValueError(f"Unknown operator {op}")
        
    def eval_boolean(self, value):
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError(f"Invalid boolean value: {value}")