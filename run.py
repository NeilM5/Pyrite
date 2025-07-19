import os

from lexer import Lexer
from parser import Parser
from interpreter import Interpreter
from error import Error

interpreter = Interpreter()

def run(text):

    try:
        lexer = Lexer(text)
        tokens = lexer.tokenizer()

        parser = Parser(tokens)
        ast = parser.parse()

        result = None
        for stmt in ast:
            result = interpreter.visit(stmt)
        
        return format_result(result)
    
    except Error as e:
        return e
    except Exception as e:
        return f"Unhandled Error: {e}"

def run_file(path):
    if not path.endswith(".pyr"):
        return f"Error: File must be a .cat extension"
    
    if not os.path.exists(path):
        return f"Error: File '{path}' not found"
    
    try:
        with open(path, 'r') as file:
            code = file.read()

        print(run(code))

    except Exception as e:
        return f"Error: Failed to read file '{path}'. {str(e)}"
    
def format_result(value):
    if value is True:
        return "true"
    elif value is False:
        return "false"
    elif value is None:
        return "null"
    return value
    
def repl():
    while True:
        try:
            cmd = input("> ")

            if cmd.startswith("run "):
                run_file(cmd[4:].strip())
            elif cmd.strip() != "":
                result = run(cmd)
                if result is not None:
                    print(result)

        except KeyboardInterrupt:
            print("Exiting...")
            break

if __name__ == "__main__":
    repl()