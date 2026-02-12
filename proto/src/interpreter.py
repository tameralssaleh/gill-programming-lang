from nodes import *
from rts import *
from environment import Env, ModuleEnv
import os
import importlib.util
from typing import Dict
from exceptions import ReturnException

class Interpreter:
    def __init__(self, global_env: Env):
        self.global_env: Env = global_env
        self.module_paths: Dict[str, str] = {
            "stdlib": "./proto/src/packages/stdlib.py",
        }

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
            # Prefer variables in the current environment, then check modules for member references.
            try:
                return self.global_env.variables[node.name]["value"]
            except NameError:
                # If not found in current environment, check if it's referencing a module.
                if node.name in self.global_env.modules:
                    return self.global_env.modules[node.name]
                raise
            
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
            current = self.global_env.variables[node.identifier]
            current["value"] += 1
            self.global_env.variables[node.identifier] = current
            return current["value"]
            
        elif isinstance(node, DecNode):
            current = self.global_env.variables[node.identifier]
            current["value"] -= 1
            self.global_env.variables[node.identifier] = current
            return current["value"]
            
        elif isinstance(node, IfBlockNode):
            condition = self.visit(node.condition)
            if condition:
                return self.visit(node.true_block)
            elif node.false_block:
                return self.visit(node.false_block)
            return None
        
        elif isinstance(node, SwitchCaseBlockNode):
            expression = self.visit(node.expression)
            for case in node.cases:
                if expression == self.visit(case.case_value):
                    return self.visit(case.body)
            if node.default_block:
                # Only executes if loop terminated with no expression being equal to any case value.
                return self.visit(node.default_block.body)
        
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
        
        elif isinstance(node, NamespaceDefinitionNode):
            namespace_env = Env(parent=self.global_env)
            for stmt in node.body.statements:
                self.visit(stmt)
            self.global_env.variables[node.name] = {"type": "namespace", "value": namespace_env}
            return None
            
        elif isinstance(node, FunctionDefinitionNode):
            # Store the function definition in the global environment
            self.global_env.functions[node.name] = node
            node.global_environment = self.global_env
            return None
        
        elif isinstance(node, FunctionCallNode):
            # Resolve fumction object from global environment or module scope.
            if node.module_name:
                if node.module_name not in self.global_env.modules:
                    raise NameError(f"Module '{node.module_name}' not found.")
                module_env = self.global_env.modules[node.module_name]
                if node.name not in module_env.functions:
                    raise NameError(f"Function '{node.name}' not found in module '{node.module_name}'.")
                function_obj = module_env.functions[node.name]
                parent_env = module_env
            else:
                if node.name not in self.global_env.functions:
                    raise NameError(f"Function '{node.name}' not found.")
                function_obj = self.global_env.functions[node.name]
                parent_env = self.global_env
            
            # Native functions
            if isinstance(function_obj, NativeFunction):
                arg_values = [self.visit(arg) for arg in node.arguments]
                return function_obj.py_impl(*arg_values)
            
            # User defined functions
            if isinstance(function_obj, FunctionDefinitionNode):
                function_def = function_obj
                call_env = Env(parent=parent_env)
                if len(node.arguments) != len(function_def.parameters):
                    raise TypeError(f"Argument count mismatch in call to '{function_def.name}': expected {len(function_def.parameters)}, got {len(node.arguments)}")
                for param in function_def.parameters:
                    call_env.variables[param.name] = {"type": param.type_, "value": self.visit(param.default_value) if param.has_default else None}
                for i, arg_node in enumerate(node.arguments):
                    call_env.variables[function_def.parameters[i].name]["value"] = self.visit(arg_node)
                prev_env = self.global_env
                self.global_env = call_env
                try:
                    return self.visit(function_def.body)
                except ReturnException as e:
                    return e.value
                finally:
                    self.global_env = prev_env
            raise TypeError(f"Object '{node.name}' is not callable.")
        
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
        
        ###
        ### # Import and module handling
        ###

        elif isinstance(node, ImportNode):
            module_name = node.module_name
            module_env: ModuleEnv = self.load_python_module_env(module_name)
            self.global_env.modules[module_name] = module_env
            self.global_env.variables[module_name] = {"type": "module", "value": module_env}
            return None
    
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
        elif op == "SCOPERESOP":
            if isinstance(left, ModuleEnv):
                if right in left.functions:
                    return MemberRef(kind="function", env=left, name=right)
                if right in left.variables:
                    return MemberRef(kind="variable", env=left, name=right)
                raise NameError(f"'{right}' not found in scope.")
            raise TypeError(f"Left operand of scope resolution operator must be a module, got {type(left).__name__}.")
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
    
    def load_python_module_env(self, module_name: str) -> ModuleEnv:
        # Check cache.
        if module_name in self.global_env.variables:
            return self.global_env.variables[module_name]
        
        # Find file if cache returns nothing.
        if module_name not in self.module_paths:
            if f"{module_name}.py" in os.listdir("./proto/src/packages/"):
                self.module_paths[module_name] = f"./proto/src/packages/{module_name}.py"
            else:
                raise ImportError(f"Module '{module_name}' is not a standard GILL module, library, or a third party installed module, library.")
        
        module_path = self.module_paths[module_name]

        if not os.path.exists(module_path):
            raise ImportError(f"Module '{module_name}' does not exist -> '{module_path}'")
        
        # Load native Python module dynamically (this will later be done in C for C based modules, libraries, etc).
        spec = importlib.util.spec_from_file_location(f"gill_mod_{module_name}", module_path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Failed to create a module spec for '{module_name}")
        
        py_module = importlib.util.module_from_spec(spec)

        try:
            spec.loader.exec_module(py_module)
        except Exception as e:
            raise ImportError(f"Error loading module '{module_name}': {e}") from None
        
        # Validate it exports module_env.
        if not hasattr(py_module, "module_env"):
            raise ImportError(f"Python module '{module_name}' must define a 'module_env' variable")
        
        module_env: ModuleEnv = py_module.module_env

        # Check type.
        if not isinstance(module_env, ModuleEnv):
            raise ImportError(f"'module_env' in '{module_name}' is not a ModuleEnv instance")        

        # Cache in global environment.
        self.global_env.modules[module_name] = module_env

        return module_env