import art

def add(n1, n2):
    return n1 + n2


def subtract(n1, n2):
    return n1 - n2


def multiply(n1, n2):
    return n1 * n2


def divide(n1, n2):
    return n1 / n2


operation_dictionary = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide
}

# print(operation_dictionary["*"](4, 8))
def calculator():
    print(art.logo)
    should_accumulate= True
    num1 = float(input("Enter first number: "))

    while should_accumulate:
        for symbol in operation_dictionary:
            print(symbol)
        operation_symbol = input("Enter operation: ")
        num2 = float(input("Enter second number: "))
        answer = operation_dictionary[operation_symbol](num1, num2)
        print(f"{num1} + {num2} = {answer}")
        choice = input("Do you want to continue? (y/n): ")
        if choice == "y":
            num1 = answer
        else:
            should_accumulate = False
            print("\n" * 20)
            calculator()

calculator()

