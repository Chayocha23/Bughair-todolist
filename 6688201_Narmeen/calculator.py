def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def main():
    print("Simple Calculator")
    print("Operations: +, -, *, /")
    print("Enter 'q' to quit")

    while True:
        try:
            num1 = input("Enter first number (or 'q' to quit): ")
            if num1.lower() == 'q':
                break
            num1 = float(num1)

            op = input("Enter operation (+, -, *, /): ")
            if op not in ['+', '-', '*', '/']:
                print("Invalid operation. Please use +, -, *, or /")
                continue

            num2 = input("Enter second number: ")
            num2 = float(num2)

            if op == '+':
                result = add(num1, num2)
            elif op == '-':
                result = subtract(num1, num2)
            elif op == '*':
                result = multiply(num1, num2)
            elif op == '/':
                result = divide(num1, num2)

            print(f"Result: {result}")

            cont = input("Continue? (y/n): ")
            if cont.lower() != 'y':
                break

        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except ZeroDivisionError as e:
            print(e)

if __name__ == "__main__":
    main()