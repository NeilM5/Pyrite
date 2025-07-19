from tokens import *
from error import Error


class LiteralNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"
    
class ListNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self):
        return f"[{", ".join(self.elements)}]"
    
class ListAccessNode:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __repr__(self):
        return f"{self.name}[{self.index}]"

class BinOpNode:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.left}, {self.op}, {self.right})"
    
class UnaryOpNode:
    def __init__(self, op, right):
        self.op = op
        self.right = right

    def __repr__(self):
        return f"({self.op}, {self.right})"
    
class IncrNode:
    def __init__(self, var_name, is_prefix = False):
        self.var_name = var_name
        self.is_prefix = is_prefix

    def __repr__(self):
        return f"{self.var_name}++"
    
class DecrNode:
    def __init__(self, var_name, is_prefix = False):
        self.var_name = var_name
        self.is_prefix = is_prefix

    def __repr__(self):
        return f"{self.var_name}--"
    
# Variable Nodes
class VarAccessNode:
    def __init__(self, var_name):
        self.var_name = var_name

    def __repr__(self):
        return f"{self.var_name}"
    
class VarAssignNode:
    def __init__(self, var_name, value, is_over = False):
        self.var_name = var_name
        self.value = value
        self.is_over = is_over

    def __repr__(self):
        return f"({self.var_name} = {self.value})"
    
class ConstAssignNode:
    def __init__(self, const_name, value):
        self.const_name = const_name
        self.value = value

    def __repr__(self):
        return f"({self.const_name} = {self.value})"

# Conditions Nodes
class IfNode:
    def __init__(self, condition, body, elif_clause = None, else_body = None):
        self.condition = condition
        self.body = body
        self.elif_clause = elif_clause or []
        self.else_body = else_body

    def __repr__(self):
        elif_part = " ".join(
            [f"elif {cond} {{ {body} }}" for cond, body in self.elif_clause]
        )
        
        else_part = None
        if self.else_body:
            else_part = f"else {{ {self.else_body} }}"
        else:
            else_part = ""
        
        return f"(if {self.condition} {{ {self.body} }} {elif_part} {else_part})"
    
# Loop Nodes
class WhileNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"(while {self.condition} {{ {self.body} }})"
    
class ForNode:
    def __init__(self, var_name, init, condition, update, body):
        self.var_name = var_name
        self.init = init
        self.condition = condition
        self.update = update
        self.body = body

    def __repr__(self):
        return f"(for {self.var_name} = {self.init} as {self.condition} do {self.update} {{ {self.body} }})"
   
# Function Node
class FunctionDefNode:
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __repr__(self):
        return f"(func {self.name}({self.params}) {{ {self.body} }})"
    
class FunctionCallNode:
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name.value}({", ".join(map(str, self.args))})"
    

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = -1
        self.current_token = None
        self.advance()

    def advance(self):
        self.index += 1

        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]

        return self.current_token

    def parse(self):
        expr = self.statements()

        if self.current_token.type != T_EOF:
            raise Error("Syntax Error", f"Unexpected token '{self.current_token}'")

        return expr

    def factor(self):
        token = self.current_token

        # Unary Operators
        if token.type in (T_PLUS, T_MINUS, T_NOT):
            self.advance()
            factor = self.factor()

            return UnaryOpNode(token, factor)

        # Literals
        if token.type in (T_INT, T_FLOAT, T_BOOL, T_STRING, T_NULL):
            self.advance()

            return LiteralNode(token)
        
        # List
        if token.type == T_LSQUARE:
            return self.list_expr()
        
        # Built In Functions
        if token.type in (T_RETURN, T_EXEC, T_INPUT, T_LEN, T_TYPE, T_STRCON, T_INTCON, T_FLOATCON, T_BOOLCON, T_ABS, T_POW):
            func_token = token
            self.advance()

            self.expect(T_LPAREN, "(")

            args = self.parse_func_args()

            self.expect(T_RPAREN, ")")

            return FunctionCallNode(func_token, args)
        
        # ID (var access)
        if token.type == T_ID:
            var_name = self.current_token
            self.advance()

            if self.current_token.type == T_LPAREN:
                return self.function_call(token)
            
            if self.current_token.type == T_LSQUARE:
                self.advance()
                index = self.expr()
                self.expect(T_RSQUARE, "]")

                return ListAccessNode(VarAccessNode(var_name), index)
            
            if self.current_token.type == T_INCR:
                self.advance()
                return IncrNode(var_name)
            
            if self.current_token.type == T_DECR:
                self.advance()
                return DecrNode(var_name)

            return VarAccessNode(token)
        
        if token.type == T_INCR:
            self.advance()

            if self.current_token.type == T_ID:
                var_name = self.current_token

                return IncrNode(var_name, True)
            
        if token.type == T_DECR:
            self.advance()

            if self.current_token.type == T_ID:
                var_name = self.current_token

                return DecrNode(var_name, True)
        
        # Parentheses
        if token.type == T_LPAREN:
            self.advance()
            expr = self.expr()

            self.expect(T_RPAREN, ")")

            return expr

        raise Error("Syntax Error", f"Unexpected token '{token.type}'")  

    def term(self):
        return self.bin_op(self.factor, (T_MUL, T_EXP, T_DIV, T_FDIV, T_MOD))
    
    def expr(self):
        # If Statements
        if self.current_token.type == T_IF:
            self.advance()

            condition = self.expr()

            self.expect(T_LBRACE, "{")

            body = self.statements()

            self.expect(T_RBRACE, "}")

            elif_clause = []
            while self.current_token.type == T_ELIF:
                self.advance()

                elif_condition = self.expr()
                
                self.expect(T_LBRACE, "{")

                elif_body = self.statements()

                self.expect(T_RBRACE, "}")

                elif_clause.append((elif_condition, elif_body))

            else_body = None               
            if self.current_token.type == T_ELSE:
                self.advance()

                self.expect(T_LBRACE, "{")

                else_body = self.statements()

                self.expect(T_RBRACE, "}")
            
            return IfNode(condition, body, elif_clause, else_body)
        
        if self.current_token.type == T_WHILE:
            self.advance()

            condition = self.expr()

            self.expect(T_LBRACE, "{")

            body = self.statements()

            self.expect(T_RBRACE, "}")

            return WhileNode(condition, body)
        
        if self.current_token.type == T_FOR:
            self.advance()

            self.expect(T_VAR, "var")
            var_name = self.current_token
            self.expect(T_ID, "variable name")
            self.expect(T_ASSIGN, "=")
            init_val = self.expr()

            self.expect(T_AS, "as")
            condition = self.expr()

            self.expect(T_DO, "do")
            update = self.expr()

            self.expect(T_LBRACE, "{")
            body = self.statements()
            self.expect(T_RBRACE, "}")

            return ForNode(var_name, init_val, condition, update, body)
        
        # Function Defining 
        if self.current_token.type == T_FUNC:
            return self.function_def()
        
        if self.current_token.type == T_VAR:
            self.advance()

            var_name = self.current_token

            self.expect(T_ID, "variable name")

            self.expect(T_ASSIGN, "=")

            value = self.expr()

            return VarAssignNode(var_name, value)
        
        if self.current_token.type == T_OVER:
            self.advance()

            var_name = self.current_token

            self.expect(T_ID, "variable name")

            self.expect(T_ASSIGN, "=")

            value = self.expr()

            return VarAssignNode(var_name, value, True)
        
        if self.current_token.type == T_CONST:
            self.advance()

            const_name = self.current_token

            self.expect(T_ID, "contant name")

            self.expect(T_ASSIGN, "=")

            value = self.expr()

            return ConstAssignNode(const_name, value)

        return self.bin_op(self.term, (T_PLUS, T_MINUS, T_AVERAGE, T_EQ, T_NEQ, T_LT, T_LTE, T_GT, T_GTE, T_APPROX, T_AND, T_OR))
    
    def statements(self):
        statements = []

        while self.current_token.type not in (T_RBRACE, T_EOF):

            statements.append(self.expr())

        return statements
    
    def list_expr(self):
        elements = []
        self.advance()

        # empty
        if self.current_token.type == T_RSQUARE:
            self.advance()
            return ListNode(elements)
        
        elements.append(self.expr())

        while self.current_token.type == T_COMMA:
            self.advance()
            elements.append(self.expr())

        self.expect(T_RSQUARE, "]")

        return ListNode(elements)
    
    def function_def(self):
        self.advance()

        if self.current_token.type != T_ID:
            raise Error("Syntax Error", "Expected function name after 'func'")
        
        func_name_token = self.current_token
        self.advance()
        
        if self.current_token.type != T_LPAREN:
            raise Error("Syntax Error", "Expected '(' after function name")
        
        self.advance()

        params = []

        if self.current_token.type != T_RPAREN:
            if self.current_token.type == T_ID:
                params.append(self.current_token)
                self.advance()
                while self.current_token.type == T_COMMA:
                    self.advance()
                    if self.current_token.type != T_ID:
                        raise Error("Syntax Error", "Expected parameter after comma")
                    params.append(self.current_token)
                    self.advance()

        if self.current_token.type != T_RPAREN:
            raise Error("Syntax Error", f"Expected ')' after parameters {params}")
        
        self.advance()
        
        if self.current_token.type != T_LBRACE:
            raise Error("Syntax Error", "Expected '{' after function parameters")
        
        self.advance()

        body = self.statements()

        if self.current_token.type != T_RBRACE:
            raise Error("Syntax Error", "Expected '}' after function body")
        
        self.advance()

        return FunctionDefNode(func_name_token.value, params, body)
    
    def function_call(self, func_name_token):
        self.advance()
        args = self.parse_func_args()       

        if self.current_token.type != T_RPAREN:
            raise Error("Syntax Error", f"Expected ')' after arguments")
        
        self.advance()

        return FunctionCallNode(func_name_token, args)
    
    def parse_func_args(self):
        args = []

        if self.current_token.type != T_RPAREN:
            args.append(self.expr())
            while self.current_token.type == T_COMMA:
                self.advance()
                args.append(self.expr())
        return args
    
    def expect(self, token_type, expected_val = None):
        if self.current_token.type not in token_type:
            val = expected_val or self.current_token.value
            raise Error("Syntax Error", f"Expected '{val}'")

        token = self.current_token
        self.advance()
        return token 
    
    def bin_op(self, func, ops):
        left = func()

        while self.current_token.type in ops:
            op = self.current_token
            self.advance()
            right = func()

            left = BinOpNode(left, op, right)

        return left