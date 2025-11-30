def is_int(number):
    try:
        int(number)
        return True
    except ValueError:
        return False

def is_float(number):
    try:
        float(number)
        return True
    except ValueError:
        return False