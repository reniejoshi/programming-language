import sys
from tokenizer import Tokenizer
from parser import Term, Integer, Float, String, PrintStatement, Identifier, AssignmentStatement, IfStatement, ArithmeticOperation, ComparisonOperation, Parser

class Variables:
    def __init__(self):
        # Dictionary to store variables
        self.variables = {}
    
    def set_variable(self, name, value):
        self.variables[name] = value
    
    def get_variable(self, name):
        if name in self.variables:
            return self.variables[name]
        else:
            raise NameError(f"Variable '{name}' not defined")

# TODO: Require main() method
# TODO: Raise errors
# TODO: Handle comments
# TODO: Handle input
class Interpreter:
    def __init__(self):
        self.variables = Variables()

    def evaluate(self, node):
        print("evaluate() node", node)
        
        if isinstance(node, AssignmentStatement):
            return self.handle_assignment_statement(node)

        elif isinstance(node, Identifier):
            return self.variables.get_variable(node.value)

        elif isinstance(node, Term):
            return node.value
        
        elif isinstance(node, ArithmeticOperation):
            return self.handle_arithmetic_operation(node)
        
        elif isinstance(node, ComparisonOperation):
            return self.handle_comparison_operation(node)

        elif isinstance(node, PrintStatement):
            return print(self.evaluate(node.expression))
        
        elif isinstance(node, IfStatement):
            return self.handle_if_statement(node)
    
    def handle_assignment_statement(self, node):
        if isinstance(node.expression, Term):
            self.variables.set_variable(node.identifier.value, node.expression.value)
        elif isinstance(node.expression, ArithmeticOperation):
            value = self.handle_arithmetic_operation(node.expression)
            self.variables.set_variable(node.identifier.value, value)
    
    def handle_if_statement(self, node):
        # If the condition is True, evaluate body
        condition = self.evaluate(node.condition)
        print("handle_if_statement() condition", condition)
        if condition:
            return self.evaluate(node.body)
        # Else return
        else:
            return

    def handle_arithmetic_operation(self, node):
        first_term = self.evaluate(node.first_term)
        second_term = self.evaluate(node.second_term)
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

    def handle_comparison_operation(self, node):
        first_term = self.evaluate(node.first_term)
        second_term = self.evaluate(node.second_term)
        match node.operator:
            case "==":
                return first_term == second_term
            case "!=":
                return first_term != second_term
            case ">":
                return first_term > second_term
            case "<":
                return first_term < second_term
            case ">=":
                return first_term >= second_term
            case "<=":
                return first_term <= second_term

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