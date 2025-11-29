# This class translates code into tokens for the parser
class Tokenizer:
    # Method to initialize object of class
    def __init__(self, code_string):
        self.code_string = code_string
        # Index in code_string
        self.index = 0
    
    def current_char(self):
        if self.index < len(self.code_string):
            return self.code_string[self.index]
        else:
            return "EOF"
    
    def next_char(self):
        if self.index + 1 < len(self.code_string):
            return self.code_string[self.index + 1]
        else:
            return "EOF"

    # Method that increments index
    def consume(self, increment_value = 1):
        self.index += increment_value

    def tokenize(self):
        # List of tuples holding type and value
        self.tokens = []
        # Dictionary of keywords
        keywords = {
            "output": "PRINT",
            "input": "INPUT",
            "if": "IF"
        }
        # List of arithmetic operators
        arithmetic_operators = ["+", "-", "*", "/", "%", "^"]
        # List of comparison operators
        comparison_operators = ["==", "!=", ">", "<", ">=", "<="]

        # Loop to iterate through code_string
        while self.current_char() != "EOF":
            # If current char is space, continue
            if self.current_char().isspace():
                self.consume()
                continue

            # If current char is the start of an identifier in camel case or keyword, append the identifer or keyword to tokens
            elif self.current_char().isalpha():
                start_index = self.index
                self.consume()
                while self.current_char() != "EOF" and self.current_char().isalpha():
                    self.consume()
                if self.code_string[start_index:self.index] in keywords:
                    keyword = self.code_string[start_index:self.index]
                    self.tokens.append((keywords[keyword], keyword))
                else:
                    self.tokens.append(("IDENTIFIER", self.code_string[start_index:self.index]))
                continue
            
            # If current char is a number, append the number to tokens
            elif self.current_char().isnumeric():
                start_index = self.index
                self.consume()
                while self.current_char() != "EOF" and (self.current_char().isnumeric() or self.current_char() == "."):
                    self.consume()
                number = self.code_string[start_index:self.index]
                if self.is_int(number):
                    self.tokens.append(("INTEGER", int(number)))
                elif self.is_float(number):
                    self.tokens.append(("FLOAT", float(number)))
                continue

            # If current char is start of a string, append the string to tokens
            elif self.current_char() == "\"" or self.current_char() == "'":
                self.consume()
                start_index = self.index
                while self.current_char() != "EOF" and self.current_char() != "\"" and self.current_char() != "'":
                    self.consume()
                self.tokens.append(("STRING", self.code_string[start_index:self.index]))
                self.consume()
                continue

            # If current char is variable assignment, append the assignment symbol to tokens
            elif self.current_char() == "=" and self.next_char() != "=":
                self.tokens.append(("ASSIGNMENT", self.current_char()))
                self.consume()
                continue

            # If current char is an arithmetic operator, append the arithmetic operator to tokens
            elif self.current_char() in arithmetic_operators:
                self.tokens.append(("ARITHMETIC_OPERATOR", self.current_char()))
                self.consume()
                continue

            # If current char is a comparison operator, append the comparison operator to tokens
            elif self.current_char() in comparison_operators:
                self.tokens.append(("COMPARISON_OPERATOR", self.current_char()))
                self.consume()
                continue

            # If current char is the start of a comparison operator, append the comparison operator to tokens
            elif self.current_char() + self.next_char() in comparison_operators:
                self.tokens.append(("COMPARISON_OPERATOR", self.current_char() + self.next_char()))
                self.consume(2)
                continue

            # If current char is open brace, append open brace to tokens
            elif self.current_char() == "{":
                self.tokens.append(("OPEN_BRACE", self.current_char()))
                self.consume()
                continue
            
            # If current char is close brace, append close brace to tokens
            elif self.current_char() == "}":
                self.tokens.append(("CLOSE_BRACE", self.current_char()))
                self.consume()
                continue

            # If current char is newline, append new line to tokens
            elif self.current_char() == "\n":
                self.tokens.append(("NEWLINE", self.current_char()))
                self.consume()
                continue

            # Increment index
            else:
                self.consume()
            
        return self.tokens
    
    def is_int(self, number):
        try:
            int(number)
            return True
        except ValueError:
            return False

    def is_float(self, number):
        try:
            float(number)
            return True
        except ValueError:
            return False