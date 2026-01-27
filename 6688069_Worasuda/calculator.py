"""
Simple calculator module for basic arithmetic operations.
"""


class Calculator:
    """A simple calculator class that supports basic arithmetic operations."""

    @staticmethod
    def add(a: float, b: float) -> float:
        """Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Subtract two numbers.
        
        Args:
            a: First number
            b: Second number (to be subtracted from a)
            
        Returns:
            Difference of a and b
        """
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        """Divide two numbers.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Quotient of a divided by b
            
        Raises:
            ValueError: If attempting to divide by zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


def main():
    """Interactive calculator CLI."""
    print("=== Simple Calculator ===")
    print("Operations: add, subtract, multiply, divide, exit")
    print()

    calc = Calculator()

    while True:
        try:
            operation = input("Enter operation (add/subtract/multiply/divide/exit): ").strip().lower()

            if operation == "exit":
                print("Thank you for using the calculator!")
                break

            if operation not in ["add", "subtract", "multiply", "divide"]:
                print("Invalid operation. Please try again.\n")
                continue

            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if operation == "add":
                result = calc.add(num1, num2)
            elif operation == "subtract":
                result = calc.subtract(num1, num2)
            elif operation == "multiply":
                result = calc.multiply(num1, num2)
            elif operation == "divide":
                result = calc.divide(num1, num2)

            print(f"Result: {result}\n")

        except ValueError as e:
            print(f"Error: {e}\n")
        except ValueError:
            print("Please enter valid numbers.\n")


if __name__ == "__main__":
    main()
