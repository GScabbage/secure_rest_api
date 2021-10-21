def add(number1, number2):
    number3 = number1 + number2
    return number3


def subtract(number1, number2):
    number3 = number1 - number2
    return number3


def multiply(number1, number2):
    number3 = number1 * number2
    return number3

def divide(number1, number2):
    if number2 == 0:
        return None
    else:
        number3 = number1 / number2
        return number3

def indices(number1, number2):
    number3 = number1 ** number2
    return number3

def process(number1, number2, operation):
    if operation == '+':
        return add(number1, number2)
    elif operation == '-':
        return subtract(number1, number2)
    elif operation == '*':
        return multiply(number1, number2)
    elif operation == '/':
        return divide(number1, number2)
    elif operation == 'nn':
        return indices(number1, number2)
    else:
        return "Operation isn't supported"
