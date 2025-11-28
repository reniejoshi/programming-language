# This class translates code into tokens for the parser
class Tokenizer:
    # Method to initialize object of class
    def __init__(self, code_string):
        self.code_string = code_string

    def tokenize(self):
        code_string = self.code_string
        # List of tuples holding type and value
        self.tokens = []
        # Dictionary of keywords
        keywords = {
            "output": "PRINT",
            "input": "INPUT",
            "if": "IF"
        }
        # List of arithmetic operators
        arithmetic_operators = ["+", "-", "*", "/", "^"]
        # List of comparision operators
        comparision_operators = ["==", "!=", ">", "<", ">=", "<="]

        # Index in code_string
        self.i = 0

        # Loop to iterate through code_string
        while self.i < len(code_string):
            char = code_string[self.i]

            # If char is space, continue
            if char.isspace():
                self.i += 1
                continue

            # If char is the start of an identifier in camel case or keyword, append the identifer or keyword to tokens
            elif char.isalpha():
                start_index = self.i
                self.i += 1
                while self.i < len(code_string) and code_string[self.i].isalpha():
                    self.i += 1
                if code_string[start_index:self.i] in keywords:
                    token_type = code_string[start_index:self.i]
                    self.tokens.append((keywords[token_type], code_string[start_index:self.i]))
                else:
                    self.tokens.append(("IDENTIFIER", code_string[start_index:self.i]))
                continue
            
            # If char is a number, append the number to tokens
            elif char.isnumeric():
                start_index = self.i
                self.i += 1
                while self.i < len(code_string) and (code_string[self.i].isnumeric() or code_string[self.i] == "."):
                    self.i += 1
                number = code_string[start_index:self.i]
                if Tokenizer.is_int(number):
                    self.tokens.append(("INTEGER", number))
                elif Tokenizer.is_float(number):
                    self.tokens.append(("FLOAT", number))
                continue

            # If char is start of a string, append the string to tokens
            elif char == "\"" or char == "'":
                self.i += 1
                start_index = self.i
                while self.i < len(code_string) and code_string[self.i] != "\"" and code_string[self.i] != "'":
                    self.i += 1
                self.tokens.append(("STRING", code_string[start_index:self.i]))
                self.i += 1
                continue

            # If char is variable assignment, append the assignment symbol to tokens
            elif char == "=" and code_string[self.i + 1] != "=":
                self.tokens.append(("ASSIGNMENT", code_string[self.i]))
                self.i += 1
                continue

            # If char is an arithmetic operator, append the arithmetic operator to tokens
            elif char in arithmetic_operators:
                self.tokens.append(("ARITHMETIC_OPERATOR", code_string[self.i]))
                self.i += 1
                continue

            # If char is the start of a comparision operator, append the comparision operator to tokens
            elif char + code_string[self.i] in comparision_operators:
                self.tokens.append(("COMPARISION_OPERATOR", char + code_string[self.i]))
                self.i += 2
                continue

            # If char is open brace, append open brace to tokens
            elif char == "{":
                self.tokens.append(("OPEN_BRACE", code_string[self.i]))
                self.i += 1
                continue
            
            # If char is close brace, append close brace to tokens
            elif char == "}":
                self.tokens.append(("CLOSE_BRACE", code_string[self.i]))
                self.i += 1
                continue

            # If char is newline, append new line to tokens
            elif char == "\n":
                self.tokens.append(("NEWLINE", code_string[self.i]))
                self.i += 1
                continue

            # Increment i
            self.i += 1
            
        return self.tokens
    
    def is_int(num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    def is_float(num):
        try:
            float(num)
            return True
        except ValueError:
            return False