from tokens import *
from error import Error

# Token Representation
class Token:
    def __init__(self, type, value = None):
        self.type = type
        self.value = value

    def matches(self, type, value = None):
        return self.type == type and self.value == value

    def __repr__(self):
        if self.value:
            return f"{self.type}: {self.value}"

        else:
            return f"{self.type}"

# Lexer
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1

        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]

        else:
            self.current_char = None

    def tokenizer(self):
        tokens = []

        while self.current_char != None:

            # Ignoring Spaces, Tabs, and Newlines
            if self.current_char == " ":
                self.advance()
            elif self.current_char == "\t":
                self.advance()
            elif self.current_char == "\n":
                self.advance()

            # Comments
            elif self.current_char == "#":
                while self.current_char != None and self.current_char != "\n":
                    self.advance()

            elif self.current_char == "/" and self.peek() == "#":
                self.advance()
                self.advance()

                while self.current_char != None:
                    if self.current_char == "#" and self.peek() == "/":
                        self.advance()
                        self.advance()

                        break
                    
                    self.advance()

            # Check Digits & Letters
            elif self.current_char in DIGITS:
                tokens.append(self.digitizer())
            elif self.current_char in LETTERS:
                tokens.append(self.identifier())
            elif self.current_char in "\"\'":
                tokens.append(self.stringer())

            # Assignment & Comparison Operators
            elif self.current_char == "=":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(T_EQ))
                    self.advance()
                else:
                    tokens.append(Token(T_ASSIGN))

            elif self.current_char == "!":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(T_NEQ))
                    self.advance()

            elif self.current_char == "<":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(T_LTE))
                    self.advance()
                else:
                    tokens.append(Token(T_LT))

            elif self.current_char == ">":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(T_GTE))
                    self.advance()
                else:
                    tokens.append(Token(T_GT))

            elif self.current_char == "~":
                self.advance()
                if self.current_char == "=":
                    tokens.append(Token(T_APPROX))
                    self.advance()
                else:
                    tokens.append(Token(T_AVERAGE))

            # Logical Operators
            elif self.current_char == "&":
                tokens.append(Token(T_AND))
                self.advance()
            elif self.current_char == "|":
                tokens.append(Token(T_OR))
                self.advance()
            elif self.current_char == "!":
                tokens.append(Token(T_NOT))
                self.advance()

            # Arithmetic Operators
            elif self.current_char == "+":
                self.advance()
                if self.current_char == "+":
                    tokens.append(Token(T_INCR))
                    self.advance()
                else:
                    tokens.append(Token(T_PLUS))

            elif self.current_char == "-":
                self.advance()
                if self.current_char == "-":
                    tokens.append(Token(T_DECR))
                    self.advance()
                else:
                    tokens.append(Token(T_MINUS))

            elif self.current_char == "*":
                tokens.append(Token(T_MUL))
                self.advance()

            elif self.current_char == "^":
                tokens.append(Token(T_EXP))
                self.advance()

            elif self.current_char == "/":
                self.advance()
                if self.current_char == "/":
                    tokens.append(Token(T_FDIV))
                    self.advance()
                else:
                    tokens.append(Token(T_DIV))

            elif self.current_char == "%":
                tokens.append(Token(T_MOD))
                self.advance()

            # Brackets
            elif self.current_char == "(":
                tokens.append(Token(T_LPAREN))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(T_RPAREN))
                self.advance()

            elif self.current_char == "{":
                tokens.append(Token(T_LBRACE))
                self.advance()
            elif self.current_char == "}":
                tokens.append(Token(T_RBRACE))
                self.advance()

            elif self.current_char == "[":
                tokens.append(Token(T_LSQUARE))
                self.advance()
            elif self.current_char == "]":
                tokens.append(Token(T_RSQUARE))
                self.advance()

            elif self.current_char == ",":
                tokens.append(Token(T_COMMA))
                self.advance()

            # Illegal Char Error
            else:
                char = self.current_char
                self.advance()
                
                # raise Exception(f"Illegal Character: '{char}'")
                raise Error("Syntax Error", f"Illegal character '{char}'")

        tokens.append(Token(T_EOF, None))
        return tokens
    
    def peek(self):
        if self.pos + 1 < len(self.text):
            return self.text[self.pos + 1]
        
        return None

    def digitizer(self): # Making Numbers
        num_str = ""
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break

                dot_count += 1
                num_str += "."

            else:
                num_str += self.current_char

            self.advance()

        if dot_count == 0:
            return Token(T_INT, int(num_str))
        else:
            return Token(T_FLOAT, float(num_str))
        
    def identifier(self):
        id_str = ""

        while self.current_char != None and self.current_char in LETTER_DIGITS + "_":
            id_str += self.current_char
            self.advance()

        if id_str in KEYWORDS:
            token_type = KEYWORDS[id_str]

            return Token(token_type, id_str)
        
        elif id_str in BUILTIN:
            token_type = BUILTIN[id_str]

            return Token(token_type, id_str)

        return Token(T_ID, id_str)
    
    def stringer(self):
        self.advance()
        str_val = ""

        while self.current_char not in "\"\'":
            if self.current_char == None:
                raise Error("Syntax Error", "Unterminated string")
            
            str_val += self.current_char
            self.advance()

        self.advance()

        return Token(T_STRING, str_val)