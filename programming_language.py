variables = {}

# TODO: Refactor assignment and print logic into functions
# TODO: Add comments to explain code
# TODO: Add logic to read file
while True:
    user_input = input()

    if user_input == "exit":
        break
    
    elif "=" in user_input:
        user_input_array = user_input.split("=")
        name = user_input_array[0].strip()
        value = user_input_array[1].strip()
    
        if value.isnumeric():
            variables[name] = int(value)
    
        elif "+" in value or "-" in value or "*" in value or "/" in value:
            variables[name] = eval(value, {}, variables)

        elif value.startswith("input(") and value.endswith(")"):
            input_prompt = value[len("input("):-1].strip().strip("\"").strip("'")
            user_input = input(input_prompt)
            if user_input.isnumeric():
                variables[name] = int(user_input)
            else:
                variables[name] = user_input

        print("variables: ", variables)

    elif "print(" in user_input:
        startIndex = user_input.find("(")
        endIndex = user_input.find(")")
        value = user_input[startIndex + 1:endIndex].strip()
    
        if value.isnumeric():
            print(value)

        elif value in variables:
            print(variables[value])
    
        else:
            print("Variable not declared:", value)
    
    print("user_input: " + user_input)