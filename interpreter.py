from tokens import *
from error import Error

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.constants = set()

    def get(self, name):
        return self.symbols[name]
    
    def set(self, name, value, is_const = False):
        if name in self.constants:
            raise Error("Runtime Error", f"Cannot reassign constant '{name}'")
        
        self.symbols[name] = value

        if is_const:
            self.constants.add(name)

    def is_constant(self, name):
        return name in self.constants

class ReturnSignal(Exception):
    def __init__(self, value):
        super().__init__()
        self.value = value

class Interpreter:
    def __init__(self):
        self.symbol_table = SymbolTable()

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit)
        
        return method(node)

    def no_visit(self, node):
        raise Error("Runtime Error", f"No visit_{type(node).__name__} method defined")
    
    # Variable Visitor Methods
    
    def visit_VarAssignNode(self, node):
        var_name = node.var_name.value
        value = self.visit(node.value)

        if node.is_over:
            if var_name not in self.symbol_table.symbols:
                raise Error("Runtime Error", f"Cannot use 'over' to reassign undefined variable '{var_name}'")

        self.symbol_table.set(var_name, value)

        return value
    
    def visit_ConstAssignNode(self, node):
        const_name = node.const_name.value
        value = self.visit(node.value)

        self.symbol_table.set(const_name, value, is_const = True)

        return value
    
    def visit_VarAccessNode(self, node):
        var_name = node.var_name.value

        if var_name not in self.symbol_table.symbols:
            raise Error("Runtime Error", f"'{var_name}' not defined")

        return self.symbol_table.get(var_name)
    
    # Conditions Visiter Method

    def visit_IfNode(self, node):
        if self.visit(node.condition):
            result = None
            for expr in node.body:
                result = self.visit(expr)
            return result
        
        for cond, body in node.elif_clause:
            if self.visit(cond):
                result = None
                for expr in body:
                    result = self.visit(expr)
                return result
        
        if node.else_body:
            result = None
            for expr in node.else_body:
                result = self.visit(expr)
            return result
        
        return None
    
    # Loop Visitor Methods

    def visit_WhileNode(self, node):
        result = None

        while self.visit(node.condition):
            for expr in node.body:
                result = self.visit(expr)
        
        return result
    
    def visit_ForNode(self, node):
        var_name = node.var_name.value
        start_val = self.visit(node.init)

        self.symbol_table.set(var_name, start_val)

        while self.visit(node.condition):
            for expr in node.body:
                self.visit(expr)

            self.visit(node.update)
    
    # Number Visitor Method

    def visit_LiteralNode(self, node):
        return node.token.value
    
    def visit_ListNode(self, node):
        eval_elements = []

        for element in node.elements:
            eval_elements.append(self.visit(element))

        return eval_elements
    
    def visit_ListAccessNode(self, node):
        list_val = self.visit(node.name)
        index = self.visit(node.index)

        if type(list_val) != list:
            raise Error("Runtime Error", "Expected list")
        
        if type(index) != int:
            raise Error("Runtime Error", "Expected index as int")
        
        try:
            return list_val[index]
        except IndexError:
            raise Error("Runtime Error", "List index out of range")
    
    def visit_FunctionDefNode(self, node):
        self.symbol_table.set(node.name, node)
        return None
    
    def visit_FunctionCallNode(self, node):
        args = []
        for arg in node.args:
            args.append(self.visit(arg))

        if node.name.type == T_RETURN:
            if len(args) > 0:
                return_val = args[0]
            else:
                return_val = None

            raise ReturnSignal(return_val)

        if node.name.type == T_EXEC:
            output = "\n".join(map(str, args))
            print(output)
            return None
        
        elif node.name.type == T_INPUT:
            prompt = None
            if args:
                prompt = "> " + str(args[0])
            else:
                prompt = "> "

            user = input(prompt)

            if user.isdigit():
                return int(user)
            try:
                return float(user)
            except ValueError:
                return user
            
        elif node.name.type == T_LEN:
            return len(args[0])
        
        elif node.name.type == T_TYPE:
            return str(type(args[0]).__name__)
        
        elif node.name.type == T_STRCON:
            return str(args[0])
        elif node.name.type == T_INTCON:
            return int(args[0])
        elif node.name.type == T_FLOATCON:
            return float(args[0])
        elif node.name.type == T_BOOLCON:
            return bool(args[0])
        
        elif node.name.type == T_ABS:
            return abs(args[0])
        
        elif node.name.type == T_POW:
            return args[0] ** args[1]
        
        
        func = self.symbol_table.get(node.name.value)

        prev_symbols = self.symbol_table.symbols.copy()

        for i in range(len(func.params)):
            param_name = func.params[i].value
            self.symbol_table.set(param_name, args[i])

        result = None
        try:
            for expr in func.body:
                result = self.visit(expr)
        except ReturnSignal as rs:
            result = rs.value

        self.symbol_table.symbols = prev_symbols
        
        return result
    
    def visit_IncrNode(self, node):
        var_name = node.var_name.value

        if var_name not in self.symbol_table.symbols:
            raise Error("Runtime Error", f"Undefined variable '{var_name}'")

        current_val = self.symbol_table.get(var_name)

        if node.is_prefix:
            self.symbol_table.set(var_name, current_val + 1)
            return current_val + 1
        else:
            self.symbol_table.set(var_name, current_val + 1)
            return current_val
    
    def visit_DecrNode(self, node):
        var_name = node.var_name.value

        if var_name not in self.symbol_table.symbols:
            raise Error("Runtime Error", f"Undefined variable '{var_name}'")

        current_val = self.symbol_table.get(var_name)

        if node.is_prefix:
            self.symbol_table.set(var_name, current_val - 1)
            return current_val - 1
        else:
            self.symbol_table.set(var_name, current_val - 1)
            return current_val
    
    # Bin Op Visitor Method

    def visit_BinOpNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == T_PLUS:
            return left + right
        elif node.op.type == T_MINUS:
            return left - right
        elif node.op.type == T_MUL:
            return left * right
        elif node.op.type == T_EXP:
            return left ** right
        elif node.op.type == T_DIV:
            if right == 0:
                raise Error("Zero Division Error", "Cannot divide by 0")
            return left / right
        elif node.op.type == T_FDIV:
            if right == 0:
                raise Error("Zero Division Error", "Cannot divide by 0")
            return left // right
        elif node.op.type == T_MOD:
            if right == 0:
                raise Error("Zero Division Error", "Cannot divide by 0")
            return left % right
        
        elif node.op.type == T_AVERAGE:
            return (left + right) / 2
        
        elif node.op.type == T_EQ:
            return left == right
        elif node.op.type == T_NEQ:
            return left != right
        elif node.op.type == T_LT:
            return left < right
        elif node.op.type == T_LTE:
            return left <= right
        elif node.op.type == T_GT:
            return left > right
        elif node.op.type == T_GTE:
            return left >= right
        elif node.op.type == T_APPROX:
            return abs(left - right) <= 0.01
        
        elif node.op.type == T_AND:
            return left and right
        elif node.op.type == T_OR:
            return left or right
        
        raise Error("Runtime Error", f"Unsupported operator '{node.op.type}'")
    
    # Unary Op Visitor Method
    
    def visit_UnaryOpNode(self, node):
        value = self.visit(node.right)

        if node.op.type == T_MINUS:
            return -value
        
        if node.op.type == T_NOT:
            return not self.visit(node.right)
        
        return value