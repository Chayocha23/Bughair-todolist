"""
Simple calculator that supports add, subtract, multiply, and divide operations.
"""


class Calculator:
    """A simple calculator class for basic arithmetic operations."""

    def add(self, a, b):
        """Add two numbers."""
        return a + b

    def subtract(self, a, b):
        """Subtract b from a."""
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b


def divide(a, b):
    """Divide two numbers."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def calculate_velocity(distance: float, time: float) -> float:
    """Calculate velocity from distance and time."""
    # Check for invalid input: time must be greater than zero [cite: 405, 419]
    if time <= 0:
        raise ValueError("Time must be greater than zero") [cite: 420]
    return distance / time

def main():
    """Main function to run the calculator interactively."""
    calc = Calculator()
    
    print("Simple Calculator")
    print("=" * 40)
    print("Operations: add, subtract, multiply, divide")
    print("Type 'quit' to exit\n")
    
    while True:
        try:
            operation = input("Enter operation (add/subtract/multiply/divide) or 'quit': ").strip().lower()
            
            if operation == 'quit':
                print("Goodbye!")
                break
            
            if operation not in ['add', 'subtract', 'multiply', 'divide']:
                print("Invalid operation. Please try again.\n")
                continue
            
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if operation == 'add':
                result = calc.add(num1, num2)
            elif operation == 'subtract':
                result = calc.subtract(num1, num2)
            elif operation == 'multiply':
                result = calc.multiply(num1, num2)
            else:  # divide
                result = calc.divide(num1, num2)
            
            print(f"Result: {num1} {operation[0]} {num2} = {result}\n")
            
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Invalid input. Please enter valid numbers.\n")


if __name__ == "__main__":
    main()
