import sys
from tokenizer import Tokenizer
from parser import (
    Term,
    Integer,
    Float,
    String,
    Identifier,
    PrintStatement,
    InputStatement,
    AssignmentStatement,
    ConditionalStatement,
    IfStatement,
    ElifStatement,
    ElseStatement,
    ArithmeticOperation,
    ComparisonOperation,
    Parser)

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
class Interpreter:
    def __init__(self):
        self.variables = Variables()

    def evaluate(self, node):
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
        
        elif isinstance(node, InputStatement):
            return self.handle_input_statement()
        
        elif isinstance(node, ConditionalStatement):
            return self.handle_conditional_statement(node)
    
    def handle_assignment_statement(self, node):
        name = node.identifier.value

        if isinstance(node.expression, Term):
            value = node.expression.value
        elif isinstance(node.expression, ArithmeticOperation):
            value = self.handle_arithmetic_operation(node.expression)
        elif isinstance(node.expression, InputStatement):
            value = self.handle_input_statement()
        
        self.variables.set_variable(name, value)
    
    def handle_conditional_statement(self, node):
        if_statement = node.if_statement
        elif_statements = node.elif_statements
        else_statement = node.else_statement

        if_body_statements = self.handle_if_statement(if_statement)
        if if_body_statements != []:
            return if_body_statements
        
        if elif_statements != None:
            elif_body_statements = []
            index = 0
            while elif_body_statements == [] and index < len(elif_statements):
                elif_body_statements = self.handle_if_statement(elif_statements[index])
                index += 1
            if elif_body_statements != []:
                return elif_body_statements
        
        if else_statement != None:
            else_body_statement = self.handle_else_statement(else_statement)
            return else_body_statement
        
        return []

    def handle_if_statement(self, node):
        condition = self.evaluate(node.condition)
        body_statements = []

        # If condition is True, evaluate body
        if condition:
            for statement in node.body:
                body_statements.append(self.evaluate(statement))
        
        return body_statements

    def handle_else_statement(self, node):
        body_statements = []
        for statement in node.body:
            body_statements.append(self.evaluate(statement))
        return body_statements

    def handle_input_statement(self):
        return input()

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