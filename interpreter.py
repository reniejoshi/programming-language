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

# TODO: Raise errors
class Interpreter:
    def __init__(self):
        self.code_file = open("code_file.py", "w")

    def evaluate(self, node):
        if isinstance(node, Newline):
            self.code_file.write(node.value)
            return print(node.value)

        elif isinstance(node, AssignmentStatement):
            return self.handle_assignment_statement(node)

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
        elif isinstance(node.expression, ComparisonOperation):
            value = self.handle_comparison_operation(node.expression)
        elif isinstance(node.expression, InputStatement):
            value = self.handle_input_statement()

        self.code_file.write(f"{name} = {value}")
    
    def handle_conditional_statement(self, node):
        if_statement = node.if_statement
        elif_statements = node.elif_statements
        else_statement = node.else_statement

        self.handle_if_statement(if_statement)
        
        for statement in if_statement.body:
            self.code_file.write("\t")
            self.evaluate(statement)

        if elif_statements != None:
            for elif_statement in elif_statements:
                self.handle_elif_statement(elif_statement)

                for statement in elif_statement.body:
                    self.code_file.write("\t")
                    self.evaluate(statement)
        
        if else_statement != None:
            else_body_statement = self.handle_else_statement(else_statement)
            return else_body_statement
        
        return []

    def handle_if_statement(self, node):
        condition = self.evaluate(node.condition)
        self.code_file.write(f"if {condition}:")

    def handle_elif_statement(self, node):
        condition = self.evaluate(node.condition)
        self.code_file.write(f"elif {condition}:")
        

    def handle_else_statement(self, node):
        body_statements = []
        for statement in node.body:
            body_statements.append(self.evaluate(statement))
        return body_statements

    def handle_input_statement(self):
        return "input()"

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

        return f"{first_term} {node.operator} {second_term}"

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