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
    
    def parse(self):
        # Index in tokens
        self.i = 0

        # Loop to iterate through tokens
        while self.i < len(self.tokens):
            pass
            self.i += 1