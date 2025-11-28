# Abstract Syntax Tree node types

class Integer:
    def __init__(self, integer):
        self.integer = integer
    
    def __repr__(self):
        return f"Integer(integer={self.integer})"

class Float:
    def __init__(self, float):
        self.float = float
    
    def __repr__(self):
        return f"Float(float={self.float})"

class String:
    def __init__(self, string):
        self.string = string
    
    def __repr__(self):
        return f"String(string={self.string})"

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

class Identifier:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Identifier(name={self.name})"

class AssignmentStatement:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"AssignmentStatement(identifier={self.identifier}, expression={self.expression})"

class ArithmeticOperation:
    def __init__(self, first_number, operator, second_number):
        self.first_number = first_number
        self.operator = operator
        self.second_number = second_number
    
    def __repr__(self):
        return f"ArithmeticOperation(first_number={self.first_number}, operator={self.operator}, second_number={self.second_number})"

# This class translates tokens into Abstract Syntax Tree node types for the interpreter
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # Index in tokens
        self.index = 0
    
    # Method that returns the current token
    def current(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return ("EOF", "")

    def parse(self):
        # Loop to iterate through tokens
        while self.current()[0] != "EOF":
            if self.current()[0] == "INTEGER":
                self.parse_integer(self.current()[1])
            elif self.current()[0] == "FLOAT":
                self.parse_float(self.current()[1])
            elif self.current()[0] == "STRING":
                self.parse_string(self.current()[1])

            pass
            self.index += 1
    
    def parse_integer(self, integer):
        return Integer(integer)
    
    def parse_float(self, float):
        return Float(float)
    
    def parse_string(self, string):
        return String(string)
    
    def parse_print_statement(self, expression):
        return PrintStatement(expression)