import string

# Tokens
LETTERS = string.ascii_letters
DIGITS = "0123456789"
LETTER_DIGITS = LETTERS + DIGITS

# Data Types
T_INT = "INT"
T_FLOAT = "FLOAT"
T_STRING = "STRING"
T_BOOL = "BOOL"
T_NULL = "NULL"

# Arithmetic
T_PLUS = "PLUS"
T_MINUS = "MINUS"
T_MUL = "MUL"
T_EXP = "EXP"
T_DIV = "DIV"
T_FDIV = "FDIV"
T_MOD = "MOD"
T_AVERAGE = "AVERAGE"

T_INCR = "INCR"
T_DECR = "DECR"

# Comparison
T_EQ = "EQ"
T_NEQ = "NEQ"
T_APPROX = "APPROX"
T_LT = "LT"
T_GT = "GT"
T_LTE = "LTE"
T_GTE = "GTE"

# Logical Operator
T_AND = "AND"
T_OR = "OR"
T_NOT = "NOT"

# Bracket Types
T_LPAREN = "LPAREN"
T_RPAREN = "RPAREN"

T_LBRACE = "LBRACE"
T_RBRACE = "RBRACE"

T_LSQUARE = "LSQUARE"
T_RSQUARE = "RSQUARE"


T_COMMA = "COMMA"

# End of File
T_EOF = "EOF"

# Importation
T_IMPORT = "IMPORT"
T_FROM = "FROM"

# Variable
T_VAR = "VAR"
T_CONST = "CONST"
T_ID = "ID"
T_ASSIGN = "ASSIGN"
T_OVER = "OVER"

# Conditions
T_IF = "IF"
T_ELIF = "ELIF"
T_ELSE = "ELSE"

# Loops
T_WHILE = "WHILE"
T_FOR = "FOR"
T_AS = "AS"
T_DO = "DO"

# Functions
T_FUNC = "FUNC"

# Built in Functions
T_EXEC = "EXEC"
T_RETURN = "RETURN"
T_INPUT = "INPUT"
T_LEN = "LEN"
T_TYPE = "TYPE"
T_STRCON = "STRCON"
T_INTCON = "INTCON"
T_FLOATCON = "FLOATCON"
T_BOOLCON = "BOOLCON"
T_ABS = "ABS"
T_POW = "POW"

# Comment
T_COMMENT = "COMMENT" 

# Keywords
KEYWORDS = {
    "var": T_VAR,
    "con": T_CONST,
    "over": T_OVER,
    "true": T_BOOL,
    "false": T_BOOL,
    "null": T_NULL,
    "if": T_IF,
    "elif": T_ELIF,
    "else": T_ELSE,
    "while": T_WHILE,
    "for": T_FOR,
    "as": T_AS,
    "do": T_DO,
    "func": T_FUNC,
    "import": T_IMPORT,
    "from": T_FROM
}

BUILTIN = {
    "exec": T_EXEC,
    "return": T_RETURN,
    "input": T_INPUT,
    "len": T_LEN,
    "type": T_TYPE,
    "str": T_STRCON,
    "int": T_INTCON,
    "flt": T_FLOATCON,
    "bool": T_BOOLCON,
    "abs": T_ABS,
    "pow": T_POW
}