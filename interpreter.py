import sys
from tokenizer import Tokenizer
from parser import Term, Integer, Float, String, PrintStatement, Identifier, AssignmentStatement, ArithmeticOperation, Parser

class Variables:
    def __init__(self):
        # Dictionary to store variables
        self.variables = {}
    
    def set_variable(self, name, value):
        self.variables[name] = value
    
    def get_variable(self, name):
        return self.variables[name]

class Interpreter:
    def __init__(self):
        self.variables = Variables()

    def evaluate(self, node):
        if isinstance(node, Term):
            return node.value
        
        elif isinstance(node, Identifier):
            return self.variables.get_variable(node.name)
        
        elif isinstance(node, ArithmeticOperation):
            pass

        elif isinstance(node, AssignmentStatement):
            return self.handle_assignment_statement(node)

        elif isinstance(node, PrintStatement):
            return print(node.expression)
    
    def handle_assignment_statement(self, node):
        self.variables.set_variable(node.identifier, node.expression.value)

def run_file():
    filename = sys.argv[1]
    file = open(filename, "r")
    code_string = file.read()
    tokenizer = Tokenizer(code_string)
    tokens = tokenizer.tokenize()

    print("tokens:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAbstract Syntax Tree nodes:")
    for node in ast:
        print(node)
    
    interpreter = Interpreter()
    for statement in ast:
        interpreter.evaluate(statement)

run_file()