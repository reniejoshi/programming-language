# This class translates code into tokens for the parser
class Tokenizer:
    # TODO: Add tokenizing logic for the following types:
    # IDENTIFIER
    # INTEGER
    # FLOAT
    # STRING
    # KEYWORD
    # OPERATOR (arithmetic and comparision)
    # ASSIGNMENT
    # OPEN_BRACE
    # CLOSE_BRACE
    # NEWLINE
    # KEYWORD e.g. print, input, if
    def tokenize(code_string):
        # List of tuples holding type and value
        tokens = []
        # Index in code_string
        i = 0

        # Loop to iterate through code_string
        while i < len(code_string):
            char = code_string[i]

            # If char is space, continue
            if char.isspace():
                i += 1
                continue

            # If char is the start of an identifier in camel case, append the identifer to tokens
            elif char.isalpha():
                start_index = i
                i += 1
                while i < len(code_string) and code_string[i].isalpha():
                    i += 1
                tokens.append(("IDENTIFIER", code_string[start_index:i]))
                continue
            
            # If char is a number, append the number to tokens
            elif char.isnumeric():
                start_index = i
                i += 1
                while i < len(code_string) and code_string[i].isnumeric():
                    i += 1
                number = code_string[start_index:i]
                if Tokenizer.is_int(number):
                    tokens.append(("INTEGER", number))
                elif Tokenizer.is_float(number):
                    tokens.append(("FLOAT", number))
                continue

            # If char is variable assignment, append the assignment symbol to tokens
            elif char == "=":
                tokens.append(("ASSIGNMENT", code_string[i]))
                i += 1
                continue
            
            # If char is open brace, append open brace to tokens
            elif char == "{":
                tokens.append(("OPEN_BRACE", code_string[i]))
                i += 1
                continue
            
            # If char is close brace, append close brace to tokens
            elif char == "}":
                tokens.append(("CLOSE_BRACE", code_string[i]))
                i += 1
                continue

            # If char is newline, append new line to tokens
            elif char == "\n":
                tokens.append(("NEWLINE", code_string[i]))
                i += 1
                continue

            # Increment i
            i += 1
            
        return tokens
    
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