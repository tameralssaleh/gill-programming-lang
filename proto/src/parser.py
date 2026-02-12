from nodes import *
from tokenclass import Token

class Parser:
    def __init__(self, tokens, debug=False):
        self.tokens = tokens
        self.position = 0
        self.debug = debug

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

        declared_size: int | None = None
        value_node = None

        if self.check("LBRACKET"):
            # Array definition
            self.eat("LBRACKET")
            size_token: Token = None
            if self.check("NUMBER"):
                size_token = self.eat("NUMBER")
            declared_size = size_token.value if size_token else None
            self.eat("RBRACKET")
            type_token = self.eat("TYPE").value
            value_node = self.parse_array(declared_size)
            return DefineNode(name, type_token, value_node)

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
        print(f"Parsing factor with token: {token}") if self.debug else None
        if token.kind == "NUMBER":
            self.eat("NUMBER")
            return NumberNode(token.value)
        
        elif token.kind == "IDENTIFIER":
            print(f"Parsing IDENTIFIER: {token}") if self.debug else None
            self.eat("IDENTIFIER")
            print(f"Current token after eating IDENTIFIER: {self.current_token}") if self.debug else None
            if self.check("LBRACKET"):
                return self.parse_array_access(token.value)
            variable_name = token.value

            if self.check("INC"):
                self.eat("INC")
                return IdentifierNode(variable_name)
            
            elif self.check("DEC"):
                self.eat("DEC")
                return IdentifierNode(variable_name)
            
            return IdentifierNode(variable_name, declared_type=None)
        
        elif token.kind == "STRING":
            self.eat("STRING")
            return StringNode(token.value)
        
        elif token.kind == "CHAR":
            self.eat("CHAR")
            return CharNode(token.value)
        
        elif token.kind == "LPAREN":
            self.eat("LPAREN")

            # Check if this is a cast: (type)expr
            if self.current_token and self.current_token.kind == "CAST":
                cast_token = self.eat("CAST").value
                expr_node = self.parse_factor()  # parse the value to cast
                self.expect("RPAREN")  # close the entire (type expr)
                return CastNode(cast_token, expr_node)
            else:
                # normal parenthesized expression
                node = self.parse_boolean()
                self.expect("RPAREN")
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
            return self.parse_output_expr()
        
        elif token.kind == "CAST":
            return self.parse_casting()
        
        elif token.kind == "EXECUTE":
            return self.parse_function_call()

        else:
            for token in self.tokens:
                print(token)

            raise SyntaxError(f"Unexpected token {token} (method:parse_factor)")
        
    def parse_output_expr(self):
        print(f"Parsing output expression, current token: {self.current_token}") if self.debug else None
        if self.check("EXECUTE"):
            func_call = self.parse_function_call()
            return OutputNode(func_call)
        else:
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
    
    def parse_function_definition(self):
        self.eat("FUNCTION")

        if not self.check("TYPE"):
            raise Exception("FunctionDefinitionError: Missing return type for function definition.")
        
        return_type = self.eat("TYPE").value
        name = self.eat("IDENTIFIER").value
        parameters: list[tuple[str, str]] = []
        self.eat("LPAREN")
        if not self.check("RPAREN"):
            while True:
                param_type = self.eat("TYPE").value
                param_name = self.eat("IDENTIFIER").value
                if self.check("DEFAULT"):
                    self.eat("DEFAULT")
                    default_value_node = self.parse_expr()
                    param_node = ParameterNode(param_name, param_type)
                    param_node.default_value = default_value_node
                else:
                    param_node = ParameterNode(param_name, param_type)
                parameters.append(param_node)
                if self.check("COMMA"):
                    self.eat("COMMA")
                else:
                    break

        self.eat("RPAREN")
        body = self.parse_block()
        return FunctionDefinitionNode(name, parameters, body, return_type)
    
    def parse_namespace_definition(self):
        self.eat("NAMESPACE")
        name = self.eat("IDENTIFIER").value
        body = self.parse_block()
        return NamespaceDefinitionNode(name, body)
    
    def parse_import(self):
        self.eat("IMPORT")
        module_name = self.eat("IDENTIFIER").value
        return ImportNode(module_name)
    
    def parse_function_call(self):
        self.eat("EXECUTE")

        if not self.check("IDENTIFIER"):
            raise SyntaxError("No function or method specified to execute.")

        # module::function(...)
        if (self.position + 1) < len(self.tokens) and self.tokens[self.position + 1].kind == "SCOPERESOP":
            module_name = self.eat("IDENTIFIER").value
            self.eat("SCOPERESOP")
            function_name = self.eat("IDENTIFIER").value

            args = []
            self.eat("LPAREN")
            if not self.check("RPAREN"):
                while True:
                    args.append(self.parse_expr())
                    if self.check("COMMA"):
                        self.eat("COMMA")
                    else:
                        break
            self.eat("RPAREN")

            return FunctionCallNode(function_name, args, module_name=module_name)

        # function(...)
        function_name = self.eat("IDENTIFIER").value
        args = []
        self.eat("LPAREN")
        if not self.check("RPAREN"):
            while True:
                args.append(self.parse_expr())
                if self.check("COMMA"):
                    self.eat("COMMA")
                else:
                    break
        self.eat("RPAREN")

        return FunctionCallNode(function_name, args)

    def parse_try_catch(self):
        self.eat("TRY")
        try_block = self.parse_block()
        catch_block = None
        finally_block = None
        if not self.check("CATCH"):
            raise SyntaxError("Try block must be followed by a catch block.")
        self.eat("CATCH")
        catch_block = self.parse_block()
        if self.check("FINALLY"):
            self.eat("FINALLY")
            finally_block = self.parse_block()
        
        # Later... parse Exception type to catch.
        return TryCatchNode(try_block, catch_block, Exception, finally_block)

    def parse_if(self):
        self.eat("IF")
        condition = self.parse_boolean()
        true_block = self.parse_block()
        false_block = None

        # Check the current token AFTER the true block
        if self.current_token and self.current_token.kind == "ELSE":
            false_block = self.parse_else()

        return IfBlockNode(condition, true_block, false_block)
    
    def parse_switch(self):
        self.eat("SWITCH")
        self.eat("LPAREN")
        expr_node: ASTNode = self.parse_expr()
        self.eat("RPAREN")
        self.eat("LCBRACE")
        cases: list[CaseBlockNode] = []
        default_case: DefaultBlockNode = None
        while not self.check("RCBRACE"):
            cases.append(self.parse_case())
            if self.check("DEFAULT"):
                self.eat("DEFAULT")
                default_case: DefaultBlockNode = DefaultBlockNode(self.parse_block())
                if self.check("CASE"):
                    # Error out... Default statement should be at the end
                    raise SyntaxError("default statements belong at the end of switch-case statements.")

        self.eat("RCBRACE")
        return SwitchCaseBlockNode(expr_node, cases, default_case)
    
    def parse_case(self):
        case_value_node = None
        case_block: BlockNode = None
        if self.check("CASE"):
            self.eat("CASE")
            self.eat("LPAREN")
            case_value_node = self.parse_expr()
            self.eat("RPAREN")
            case_block = self.parse_block() # This function automatically eats the LCBRACE and RCBRACE

        return CaseBlockNode(case_value_node, case_block)

    def parse_else(self):
        self.eat("ELSE")
        return self.parse_block()

    def parse_while(self):
        self.eat("WHILE")
        condition = self.parse_boolean()
        body = self.parse_block()
        return WhileLoopNode(condition, body)
    
    def parse_for(self):
        self.eat("FOR")
        self.eat("LPAREN")
        self.eat("DEFINE")
        initializer = self.eat("IDENTIFIER").value
        self.eat("TYPE")
        initializer_value = self.eat("NUMBER").value
        self.eat("COMMA")
        condition = self.parse_boolean()
        self.eat("COMMA")
        increment = self.parse_statement()
        self.eat("RPAREN")
        body = self.parse_block()
        return ForLoopNode(initializer, initializer_value, condition, increment, body)

    def parse_foreach(self):
        self.eat("FOREACH")
        self.eat("LPAREN")
        self.eat("DEFINE")
        iterator = self.eat("IDENTIFIER").value
        self.eat("TYPE")
        self.eat("COLON")
        iterable = self.parse_expr()
        self.eat("RPAREN")
        body = self.parse_block()
        return ForEachLoopNode(iterator, iterable, body)
    
    def parse_array(self, declared_size=None):
        self.eat("LBRACKET")
        elements = []
        if not self.check("RBRACKET"):
            while True:
                element_node = self.parse_expr()
                elements.append(element_node)
                if self.check("COMMA"):
                    self.eat("COMMA")
                else:
                    break
        arr_size = len(elements) if declared_size is None else declared_size
        if declared_size is not None and declared_size < arr_size:
            raise SyntaxError(f"Array size mismatch: declared size {declared_size}, but got {arr_size} elements.")
        self.eat("RBRACKET")
        return ArrayNode(elements, arr_size)
    
    def parse_array_access(self, array_name):
        self.eat("LBRACKET")
        index_node = self.parse_expr()
        self.eat("RBRACKET")
        return ArrayAccessNode(array_name, index_node)
    
    def parse_statement(self):
        tok = self.current_token

        if tok.kind == "NUMBER":
            print(f"Parsing NUMBER, current token: {self.current_token}") if self.debug else None
            return self.parse_expr()
        elif tok.kind == "DEFINE":
            print(f"Parsing DEFINE statement, current token: {self.current_token}") if self.debug else None
            return self.parse_define()
        elif tok.kind == "ASSIGN":
            print(f"Parsing ASSIGN statement, current token: {self.current_token}") if self.debug else None
            return self.parse_assign()
        elif tok.kind == "IDENTIFIER":
            next_tok: Token = self.peek()
            print(f"Next token after IDENTIFIER: {next_tok}") if self.debug else None
            if next_tok and next_tok.kind == "LBRACKET":
                print(f"Parsing ARRAY ACCESS statement, current token: {self.current_token}") if self.debug else None
                var_name = tok.value
                self.eat("IDENTIFIER")
                return self.parse_array_access(var_name)
            
            if next_tok and next_tok.kind == "INC":
                print(f"Parsing INC statement, current token: {self.current_token}") if self.debug else None
                var_name = tok.value
                self.eat("IDENTIFIER")
                self.eat("INC")
                return IncNode(var_name)
            
            elif next_tok and next_tok.kind == "DEC":
                print(f"Parsing DEC statement, current token: {self.current_token}") if self.debug else None
                var_name = tok.value
                self.eat("IDENTIFIER")
                self.eat("DEC")
                return DecNode(var_name)
            
            elif next_tok and next_tok.kind in ("ADD", "SUB", "MUL", "DIV", "FDIV", "EQ", "NEQ", "LT", "LTE", "GT", "GTE", "AND", "OR"):
                return self.parse_boolean()
            
        elif tok.kind == "FUNCTION":
            print(f"Parsing FUNCTION statement, current token: {self.current_token}") if self.debug else None
            return self.parse_function_definition()
        elif tok.kind == "NAMESPACE":
            print(f"Parsing NAMESPACE statement, current token: {self.current_token}") if self.debug else None
            return self.parse_namespace_definition()
        elif tok.kind == "IMPORT":
            print(f"Parsing IMPORT statement, current token: {self.current_token}") if self.debug else None
            return self.parse_import()
        elif tok.kind == "RETURN":
            print(f"Parsing RETURN statement, current token: {self.current_token}") if self.debug else None
            self.eat("RETURN")
            expr_node = self.parse_expr()
            return ReturnNode(expr_node)
        elif tok.kind == "EXECUTE":
            print(f"Parsing FUNCTION CALL statement, current token: {self.current_token}") if self.debug else None
            return self.parse_function_call()
        elif tok.kind == "LCBRACE":
            print(f"Parsing block, current token: {self.current_token}") if self.debug else None
            return self.parse_block()
        elif tok.kind == "IF":
            print(f"Parsing IF statement, current token: {self.current_token}") if self.debug else None
            return self.parse_if()
        elif tok.kind == "SWITCH":
            print(f"Parsing SWITCH statement, current token: {self.current_token}") if self.debug else None
            return self.parse_switch()
        elif tok.kind == "TRY":
            print(f"Parsing TRY-CATCH statement, current token: {self.current_token}") if self.debug else None
            return self.parse_try_catch()
        elif tok.kind == "WHILE":
            print(f"Parsing WHILE loop, current token: {self.current_token}") if self.debug else None
            return self.parse_while()
        elif tok.kind == "OUTPUT":
            print(f"Parsing OUTPUT statement, current token: {self.current_token}") if self.debug else None
            self.eat("OUTPUT")
            return self.parse_output_expr()
        elif tok.kind == "FOR":
            print(f"Parsing FOR loop, current token: {self.current_token}") if self.debug else None
            return self.parse_for()
        elif tok.kind == "FOREACH":
            print(f"Parsing FOREACH loop, current token: {self.current_token}") if self.debug else None
            return self.parse_foreach()
        else:
            raise SyntaxError(f"Unexpected token {tok} in statement parsing.\n{self.tokens}")

    def parse_block(self):
        self.expect("LCBRACE")
        statements = []

        while not self.check("RCBRACE"):
            stmt = self.parse_statement()  
            if stmt:
                statements.append(stmt)

        self.expect("RCBRACE")
        return BlockNode(statements)
