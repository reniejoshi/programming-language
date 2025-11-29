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
        #print("get_variable() was called")
        if name in self.variables:
            #print("variable value", self.variables[name])
            return self.variables[name]
        else:
            #self.print_variables()
            raise NameError(f"Variable '{name}' not defined")
    
    # Method to print variables for debugging
    def print_variables(self):
        print("\nvariables: ")
        for name in self.variables:
            print(f"Name: {name}, Value: {self.variables[name]}")

class Interpreter:
    def __init__(self):
        self.variables = Variables()

    def evaluate(self, node):
        #print("evaluate() node:", node)

        if isinstance(node, AssignmentStatement):
            return self.handle_assignment_statement(node)

        elif isinstance(node, Identifier):
            return self.variables.get_variable(node.value)

        elif isinstance(node, Term):
            return node.value
        
        elif isinstance(node, ArithmeticOperation):
            return self.handle_arithmetic_operation(node)

        elif isinstance(node, PrintStatement):
            return print(self.evaluate(node.expression))
    
    def handle_assignment_statement(self, node):
        if isinstance(node.expression, Term):
            self.variables.set_variable(node.identifier.value, node.expression.value)
        elif isinstance(node.expression, ArithmeticOperation):
            value = self.handle_arithmetic_operation(node.expression)
            self.variables.set_variable(node.identifier.value, value)
    
    def handle_arithmetic_operation(self, node):
            first_term = self.evaluate(node.first_number)
            second_term = self.evaluate(node.second_number)
            match node.operator:
                case "+":
                    return first_term + second_term
                case "-":
                    return first_term - second_term
                case "*":
                    return first_term * second_term
                case "/":
                    return first_term / second_term
                case "%":
                    return first_term % second_term
                case "^":
                    return first_term ** second_term

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
    #print("\nevaluated statements:")
    for statement in ast:
        interpreter.evaluate(statement)
        #evaluated_statement = interpreter.evaluate(statement)
        #print(evaluated_statement)
    
    interpreter.variables.print_variables()

run_file()