# Dictionary to store variables
variables = {}

# TODO: Refactor assignment and print logic into functions
# TODO: Add comments to explain code
# TODO: Rename variables for clarity
# TODO: Add logic to read file
while True:
    user_input = input()

    # To exit the while loop
    if user_input == "exit":
        break
    
    # For variable assignment
    elif "=" in user_input:
        user_input_array = user_input.split("=")
        name = user_input_array[0].strip()
        value = user_input_array[1].strip()
    
        # If the value is a number, convert to integer
        if value.isnumeric():
            variables[name] = int(value)
        # TODO: Add logic to convert to float
    
        # If the value contains an arithmetic operatator, evaluate the expression from a string and store the result
        elif "+" in value or "-" in value or "*" in value or "/" in value:
            variables[name] = eval(value, {}, variables)

        # If user input calls input(), call input()
        elif value.startswith("input(") and value.endswith(")"):
            # Extract the input prompt substring from the user input
            input_prompt = value[len("input("):-1].strip().strip("\"").strip("'")
            # Call input()
            user_input = input(input_prompt)
            # If the user input is a number, convert to integer
            if user_input.isnumeric():
                variables[name] = int(user_input)
            # Else store the value as a string
            else:
                variables[name] = user_input

        # Print variables dictionary for debugging
        print("variables: ", variables)

    # If the user input calls print(), call print()
    elif "print(" in user_input:
        # Extract the value to print
        startIndex = user_input.find("(")
        endIndex = user_input.find(")")
        value = user_input[startIndex + 1:endIndex].strip()
    
        # If the value is a number, print the value
        if value.isnumeric():
            print(value)

        # If the value is a variable in variables dictionary, print the value of the variable
        elif value in variables:
            print(variables[value])
    
        # If the variable to print is not in the variables dictionary, print error message
        else:
            print("Variable not declared:", value)
    
    # Print the user input for debugging
    print("user_input: " + user_input)