def add(number1,number2):
    return float(number1) + float(number2)

def sub(number1,number2):
    return float(number1) - float(number2)

def mul(number1,number2):
    return float(number1) * float(number2)

def div(number1,number2):
    if number2 ==0:
        return None
    else:
        return float(number1) / float(number2)
