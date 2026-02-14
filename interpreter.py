import sys
from helpers import is_int, is_float
from tokenizer import Tokenizer
from parser import (
    Newline,
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
    Function,
    MainFunction,
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

# TODO: Add stack logic for nested blocks
# TODO: Raise errors
class Interpreter:
    def __init__(self):
        self.variables = Variables()
        self.code_file = open("code_file.py", "w")

    def evaluate(self, node):
        if isinstance(node, Newline):
            self.code_file.write(node.value)
            return print(node.value)

        elif isinstance(node, AssignmentStatement):
            return self.handle_assignment_statement(node)

        elif isinstance(node, Identifier):
            return self.variables.get_variable(node.value)

        elif isinstance(node, Term):
            if isinstance(node, String):
                return '"' + node.value + '"'
            else:
                return node.value
        
        elif isinstance(node, ArithmeticOperation):
            return self.handle_arithmetic_operation(node)
        
        elif isinstance(node, ComparisonOperation):
            return self.handle_comparison_operation(node)

        elif isinstance(node, PrintStatement):
            self.code_file.write("print(" + str(self.evaluate(node.expression)) + ")")
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
            for elif_statement in elif_statements:
                elif_body_statements = self.handle_if_statement(elif_statement)
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
        user_input = input()
        
        if user_input.isnumeric():
            if is_int(user_input):
                user_input = int(user_input)
            elif is_float(user_input):
                user_input = float(user_input)

        return user_input

    def handle_arithmetic_operation(self, node):
        first_term = self.evaluate(node.first_term)
        second_term = self.evaluate(node.second_term)

        if node.operator == "+" or node.operator == "-" or node.operator == "*" or node.operator == "/" or node.operator == "%":
            return f"{first_term} {node.operator} {second_term}"
        elif node.operator == "^":
            return f"{first_term} ** {second_term}"

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
    print(repr(code_string).strip("\'"))
    tokenizer = Tokenizer(repr(code_string).strip("\'"))
    tokens = tokenizer.tokenize()

    print("tokens:")
    for token in tokens:
        print(token)

    parser = Parser(tokens)
    ast = parser.parse()

    print("\nAbstract Syntax Tree nodes:")
    for node in ast:
        print(node)
    
    main_function = None
    for node in ast:
        if isinstance(node, MainFunction):
            main_function = node
            break
    
    if main_function == None:
        raise SyntaxError("Main function not found")

    interpreter = Interpreter()
    for statement in main_function.body:
        interpreter.evaluate(statement)

run_file()