# Abstract Syntax Tree node types

# Parent class for terms to inherit from
class Term:
    def __init__(self, value):
        self.value = value

class Integer(Term):
    def __repr__(self):
        return f"Integer(value={self.value})"

class Float(Term):
    def __repr__(self):
        return f"Float(value={self.value})"

class String(Term):
    def __repr__(self):
        return f"String(value={self.value})"

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

class Identifier(Term):
    def __repr__(self):
        return f"Identifier(name={self.value})"

class AssignmentStatement:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"AssignmentStatement(identifier={self.identifier}, expression={self.expression})"

class ArithmeticOperation:
    def __init__(self, first_term, operator, second_term):
        self.first_number = first_term
        self.operator = operator
        self.second_number = second_term
    
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
    
    def next_index(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]
        else:
            return ("EOF", "")
    
    def consume(self, token_type):
        if self.current()[0] == token_type:
            self.index += 1

    def parse(self):
        # List to store parsed AST nodes
        statements = []

        # Loop to iterate through tokens
        while self.current()[0] != "EOF":
            match self.current()[0]:
                case "INTEGER":
                    statements.append(self.parse_integer(self.current()[1]))
                case "FLOAT":
                    statements.append(self.parse_float(self.current()[1]))
                case "STRING":
                    statements.append(self.parse_string(self.current()[1]))
                case "IDENTIFIER" if self.next_index()[0] == "ASSIGNMENT":
                    statements.append(self.parse_assignment_statement())
                case "PRINT":
                    statements.append(self.parse_print_statement())

            self.index += 1
        
        return statements
    
    def parse_integer(self, integer):
        return Integer(integer)
    
    def parse_float(self, float):
        return Float(float)
    
    def parse_string(self, string):
        return String(string)
    
    def parse_identifier(self, name):
        return Identifier(name)

    def parse_print_statement(self):
        self.consume("PRINT")
        expression = self.parse_arithmetic_operation()
        #print("parse_print_statement() expression:", expression)
        return PrintStatement(expression)
    
    def parse_assignment_statement(self):
        name = self.parse_identifier(self.current()[1])
        self.consume("IDENTIFIER")
        self.consume("ASSIGNMENT")
        expression = self.parse_arithmetic_operation()
        return AssignmentStatement(name, expression)
    
    def parse_term(self):
        token_type = self.current()[0]
        token_value = self.current()[1]

        match token_type:
            case "INTEGER":
                self.consume("INTEGER")
                return self.parse_integer(token_value)
            case "FLOAT":
                self.consume("FLOAT")
                return self.parse_float(token_value)
            case "STRING":
                self.consume("STRING")
                return self.parse_string(token_value)
            case "IDENTIFIER":
                self.consume("IDENTIFIER")
                return self.parse_identifier(token_value)
    
    def parse_arithmetic_operation(self):
        expression = self.parse_term()
        while self.current()[0] == "ARITHMETIC_OPERATOR":
            operator = self.current()[1]
            self.consume("ARITHMETIC_OPERATOR")
            next_term = self.parse_term()
            expression = ArithmeticOperation(expression, operator, next_term)
        return expression