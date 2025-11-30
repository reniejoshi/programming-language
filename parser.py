# Abstract Syntax Tree node types

# Parent class for terms to inherit from
class Term:
    def __init__(self, value):
        self.value = value

# Child classes of Term class

class Integer(Term):
    def __repr__(self):
        return f"Integer(value={self.value})"

class Float(Term):
    def __repr__(self):
        return f"Float(value={self.value})"

class String(Term):
    def __repr__(self):
        return f"String(value={self.value})"

class Identifier(Term):
    def __repr__(self):
        return f"Identifier(name={self.value})"

# Parent class for operations to inherit from
class Operation:
    def __init__(self, first_term, operator, second_term):
        self.first_term = first_term
        self.operator = operator
        self.second_term = second_term

# Child classes of Operation class

class ArithmeticOperation(Operation):
    def __repr__(self):
        return f"ArithmeticOperation(first_term={self.first_term}, operator={self.operator}, second_term={self.second_term})"

class ComparisonOperation(Operation):
    def __repr__(self):
        return f"ComparisionOperation(first_term={self.first_term}, operator={self.operator}, second_term={self.second_term})"

# Statements

class PrintStatement:
    def __init__(self, expression):
        self.expression = expression
    
    def __repr__(self):
        return f"PrintStatement(expression={self.expression})"

class InputStatement:
    def __repr__(self):
        return f"InputStatement()"

class AssignmentStatement:
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression
    
    def __repr__(self):
        return f"AssignmentStatement(identifier={self.identifier}, expression={self.expression})"

class ConditionalStatement:
    def __init__(self, if_statement, elif_statements, else_statement):
        self.if_statement = if_statement
        self.elif_statements = elif_statements
        self.else_statement = else_statement
    
    def __repr__(self):
        return f"ConditionalStatement(if_statement={self.if_statement}, elif_statements={self.elif_statements}, else_statement={self.else_statement})"

class IfStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"IfStatement(condition={self.condition}, body={self.body})"

class ElifStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"ElifStatement(condition={self.condition}, body={self.body})"

class ElseStatement:
    def __init__(self, body):
        self.body = body
    
    def __repr__(self):
        return f"ElseStatement(body={self.body})"

# This class translates tokens into Abstract Syntax Tree node types for the interpreter
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # Index in tokens
        self.index = 0
    
    # Method that returns the current token
    def current_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return ("EOF", "")

    # Method that returns the next token    
    def next_token(self):
        if self.index + 1 < len(self.tokens):
            return self.tokens[self.index + 1]
        else:
            return ("EOF", "")
    
    # Method that increments index if the current token is the token type
    def consume(self, token_type):
        if self.current_token()[0] == token_type:
            self.index += 1
        else:
            raise SyntaxError(f"Expected {token_type} but found {self.current_token()[0]}")

    def parse(self):
        # List to store parsed AST nodes
        statements = []

        # Loop to iterate through tokens
        while self.current_token()[0] != "EOF":
            match self.current_token()[0]:
                case "INTEGER":
                    statements.append(self.parse_integer(self.current_token()[1]))
                case "FLOAT":
                    statements.append(self.parse_float(self.current_token()[1]))
                case "STRING":
                    statements.append(self.parse_string(self.current_token()[1]))
                case "IDENTIFIER" if self.next_token()[0] == "ASSIGNMENT":
                    statements.append(self.parse_assignment_statement())
                case "PRINT":
                    statements.append(self.parse_print_statement())
                case "INPUT":
                    statements.append(self.parse_input_statement())
                case "IF":
                    statements.append(self.parse_if_statement())
                case _:
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
        expression = self.parse_expression()
        return PrintStatement(expression)
    
    def parse_input_statement(self):
        self.consume("INPUT")
        return InputStatement()

    def parse_if_statement(self):
        self.consume("IF")
        condition = self.parse_expression()
        body = self.parse()
        return IfStatement(condition, body)
    
    def parse_elif_statement(self):
        self.consume("ELIF")
        condition = self.parse_expression()
        body = self.parse()
        return ElifStatement(condition, body)
    
    def parse_else_statement(self):
        self.consume("ELSE")
        body = self.parse()
        return ElseStatement(body)
    
    def parse_assignment_statement(self):
        name = self.parse_identifier(self.current_token()[1])
        self.consume("IDENTIFIER")
        self.consume("ASSIGNMENT")
        if self.current_token()[0] == "INPUT":
            expression = self.parse_input_statement()
        else:
            expression = self.parse_expression()
        return AssignmentStatement(name, expression)
    
    def parse_term(self):
        token_type = self.current_token()[0]
        token_value = self.current_token()[1]

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
    
    def parse_expression(self):
        expression = self.parse_term()

        while self.current_token()[0] == "ARITHMETIC_OPERATOR":
            operator = self.current_token()[1]
            self.consume("ARITHMETIC_OPERATOR")
            next_term = self.parse_term()
            expression = ArithmeticOperation(expression, operator, next_term)
        
        while self.current_token()[0] == "COMPARISON_OPERATOR":
            operator = self.current_token()[1]
            self.consume("COMPARISON_OPERATOR")
            next_term = self.parse_term()
            expression = ComparisonOperation(expression, operator, next_term)
        
        return expression