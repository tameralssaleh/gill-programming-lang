from nodes import *
from environment import Env
from exceptions import ReturnException

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
            return self.global_env.get(node.name)["value"]
            
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
            current = self.global_env.get(node.identifier)
            current["value"] += 1
            self.global_env.set(node.identifier, current)
            return current["value"]
            
        elif isinstance(node, DecNode):
            current = self.global_env.get(node.identifier)
            current["value"] -= 1
            self.global_env.set(node.identifier, current)
            return current["value"]
            
        elif isinstance(node, IfBlockNode):
            condition = self.visit(node.condition)
            if condition:
                return self.visit(node.true_block)
            elif node.false_block:
                return self.visit(node.false_block)
            return None
        
        elif isinstance(node, TryCatchNode):
            try:
                return self.visit(node.try_block)
            except node.catch_exception as e:
                return self.visit(node.catch_block)
            finally:
                if node.finally_block:
                    self.visit(node.finally_block)
        
        elif isinstance(node, WhileLoopNode):
            while self.visit(node.condition):
                self.visit(node.body)  # just execute the body, ignore the return

        elif isinstance(node, ForLoopNode):
            loop_env = Env(parent=self.global_env)
            loop_env.variables[node.initializer] = {
                "type": type(node.initializer_value).__name__,
                "value": node.initializer_value
            }
            prev_env = self.global_env
            self.global_env = loop_env
            try:
                while self.visit(node.condition):
                    self.visit(node.body)
                    self.visit(node.increment)
            finally:
                self.global_env = prev_env

        elif isinstance(node, ForEachLoopNode):
            loop_env = Env(parent=self.global_env)
            loop_env.variables[node.iterator] = {
                "type": type(node.iterator).__name__,
                "value": None
            }
            prev_env = self.global_env
            self.global_env = loop_env
            try:
                iterable = self.visit(node.iterable)
                for item in iterable:
                    loop_env.variables[node.iterator]["value"] = item
                    self.visit(node.body)
            except Exception as e:
                raise RuntimeError(f"Error during foreach loop: {e}\n{node.iterable}")
            finally:
                self.global_env = prev_env

        elif isinstance(node, OutputNode):
            value = self.visit(node.expression)
            print(value)
            return value  # or None
        
        elif isinstance(node, DefineNode):
            value = self.visit(node.value)

            if isinstance(value, list):
                declared_type = node.type_
                for i, element in enumerate(value):
                    if not self.check_type(element, declared_type):
                        raise TypeError(f"Type mismatch in array at index {i}: Expected {declared_type}, got {type(element).__name__}")
                    
                self.global_env.variables[node.name] = {"type": f"{declared_type}[]", "value": value}

                return value

            if self.check_type(value, node.type_):
                self.global_env.variables[node.name] = {"type": node.type_, "value": value}
            else:
                raise TypeError(f"Type mismatch: Expected {node.type_}, got {type(value).__name__}")
            
            return value
        
        elif isinstance(node, AssignNode):
            value = self.visit(node.value)
            current = self.global_env.get(node.name)
            current["value"] = value
            self.global_env.set(node.name, current)
            return value
                        
        elif isinstance(node, BlockNode):
            last_result = None
            for stmt in node.statements:
                last_result = self.visit(stmt)  # OutputNode prints internally
            return last_result 
        
        elif isinstance(node, FunctionDefinitionNode):
            # Store the function definition in the global environment
            self.global_env.functions[node.name] = node
            node.global_environment = self.global_env
            return None
        
        elif isinstance(node, FunctionCallNode):
            if node.name not in self.global_env.functions:
                raise NameError(f"Undefined function '{node.name}'")
            
            func_def: FunctionDefinitionNode = self.global_env.functions[node.name]
            call_env = Env(parent=self.global_env)

            if len(node.arguments) > len(func_def.parameters):
                raise TypeError(f"Function '{node.name}' expected at most {len(func_def.parameters)} arguments, got {len(node.arguments)} instead.")
            elif len(node.arguments) < len(func_def.parameters):
                raise TypeError(f"Function '{node.name}' expected at least {len(func_def.parameters)} arguments, got {len(node.arguments)} instead.")

            for param in func_def.parameters:
                call_env.variables[param.name] = {"type": param.type_, "value": self.visit(param.default_value)} if param.default_value else {"type": param.type_, "value": None}

            for i, arg_node in enumerate(node.arguments):
                call_env.variables[func_def.parameters[i].name]["value"] = self.visit(arg_node)

            prev_env = self.global_env
            self.global_env = call_env
            try:
                return self.visit(func_def.body)
            except ReturnException as ret:
                return ret.value
            finally:
                self.global_env = prev_env

        elif isinstance(node, ReturnNode):
            value = self.visit(node.expression)
            raise ReturnException(value)
        
        elif isinstance(node, ArrayNode):
            elements = [self.visit(elem) for elem in node.elements]
            if len(elements) != node.size: # This should not execute... as this error is caught during parsing.
                raise ValueError(f"Array size mismatch: expected {node.size}, got {len(elements)}")
            return elements
        
        elif isinstance(node, ArrayAccessNode):
            array_name = self.global_env.get(node.array_name)
            index = self.visit(node.index)
            if not isinstance(array_name["value"], list):
                raise TypeError(f"Variable '{node.array_name}' is not an array.")
            elif not isinstance(index, int):
                raise TypeError(f"Array index must be an integer, got {type(index).__name__}.")
            elif index < 0 or index >= len(array_name["value"]):
                raise IndexError(f"Array index {index} out of bounds for array '{node.array_name}' of size {len(array_name['value'])}.")
            return array_name["value"][index]

    
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
        
    def check_type(self, value, expected_type):
        type_map = {
            "int": int,
            "float": float,
            "string": str,
            "char": str,
            "bool": bool,
            "void": type(None)
        }
        if expected_type not in type_map:
            raise ValueError(f"Unknown type: {expected_type}")
        if isinstance(value, str) and expected_type == "char":
            return len(value) == 1
        return isinstance(value, type_map[expected_type])