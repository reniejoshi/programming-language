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

class Function:
    def __init__(self, identifier, parameters, body):
        self.identifier = identifier
        self.parameters = parameters
        self.body = body
    
    def __repr__(self):
        return f"Function(body={self.body})"

class MainFunction(Function):
    def __init__(self, body):
        super().__init__("main", [], body)

    def __repr__(self):
        return f"MainFunction(body={self.body})"

# This class translates tokens into Abstract Syntax Tree node types for the interpreter
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        # Index in tokens
        self.index = 0
        # Boolean representing if main function is found
        self.is_main_function_defined = False
    
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
            print("parser() self.current_token()[0]:", self.current_token()[0])
            print("parser() self.current_token()[1]", self.current_token()[1])
            statements.append(self.parse_statement())
         
        return statements
    
    def parse_statement(self):
        match self.current_token()[0]:
            case "INTEGER":
                return self.parse_integer(self.current_token()[1])
            case "FLOAT":
                return self.parse_float(self.current_token()[1])
            case "STRING":
                return self.parse_string(self.current_token()[1])
            case "IDENTIFIER" if self.next_token()[0] == "ASSIGNMENT":
                return self.parse_assignment_statement()
            case "PRINT":
                return self.parse_print_statement()
            case "INPUT":
                return self.parse_input_statement()
            case "IF":
                return self.parse_conditional_statement()
            case "FUNCTION":
                if self.next_token()[0] == "MAIN":
                    if self.is_main_function_defined:
                        raise SyntaxError("Multiple main functions found")
                    else:
                        self.is_main_function_defined = True
                        return self.parse_main_function()
            case _:
                self.index += 1
                return

    def parse_main_function(self):
        self.consume("FUNCTION")
        self.consume("MAIN")
        self.consume("OPEN_PARENTHESIS")
        self.consume("CLOSE_PARENTHESIS")
        body = self.parse_body()
        return MainFunction(body)

    def parse_body(self):
        body = []
        self.consume("OPEN_BRACE")
        while self.current_token()[0] != "CLOSE_BRACE":
            body.append(self.parse_statement())
        self.consume("CLOSE_BRACE")
        return body

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
        self.consume("OPEN_PARENTHESIS")
        expression = self.parse_expression()
        self.consume("CLOSE_PARENTHESIS")
        return PrintStatement(expression)
    
    def parse_input_statement(self):
        self.consume("INPUT")
        return InputStatement()

    def parse_conditional_statement(self):
        if_statement = self.parse_if_statement()

        elif_statements = []
        while self.current_token()[0] == "ELIF":
            elif_statements.append(self.parse_elif_statement())
        
        else_statement = None
        if self.current_token()[0] == "ELSE":
            else_statement = self.parse_else_statement()
        
        return ConditionalStatement(if_statement, elif_statements, else_statement)

    def parse_if_statement(self):
        self.consume("IF")
        condition = self.parse_expression()
        body = self.parse_body()
        return IfStatement(condition, body)
    
    def parse_elif_statement(self):
        self.consume("ELIF")
        condition = self.parse_expression()
        body = self.parse_body()
        return ElifStatement(condition, body)
    
    def parse_else_statement(self):
        self.consume("ELSE")
        body = self.parse_body()
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