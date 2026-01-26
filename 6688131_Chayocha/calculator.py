"""
Simple Calculator Application

Supports: addition, subtraction, multiplication, and division operations.
"""


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract two numbers."""
    return a - b


def multiply(a, b):
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
    """Main calculator loop."""
    print("=" * 40)
    print("        Simple Calculator")
    print("=" * 40)
    print("\nOperations:")
    print("  + : Add")
    print("  - : Subtract")
    print("  * : Multiply")
    print("  / : Divide")
    print("  q : Quit")
    print("=" * 40 + "\n")
    
    while True:
        try:
            # Get operation from user
            operation = input("Enter operation (+, -, *, /, q): ").strip()
            
            if operation.lower() == 'q':
                print("Goodbye!")
                break
            
            if operation not in ['+', '-', '*', '/']:
                print("Invalid operation. Please use +, -, *, or /\n")
                continue
            
            # Get numbers from user
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            # Perform calculation
            if operation == '+':
                result = add(num1, num2)
            elif operation == '-':
                result = subtract(num1, num2)
            elif operation == '*':
                result = multiply(num1, num2)
            elif operation == '/':
                result = divide(num1, num2)
            
            print(f"\nResult: {num1} {operation} {num2} = {result}\n")
        
        except ValueError as e:
            print(f"Error: {e}\n")
        except Exception as e:
            print(f"Invalid input. Please enter valid numbers.\n")


if __name__ == "__main__":
    main()
