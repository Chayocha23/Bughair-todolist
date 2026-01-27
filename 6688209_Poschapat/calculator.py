"""A simple calculator module with basic arithmetic operations."""


def add(a, b):
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The sum of a and b
    """
    return a + b


def subtract(a, b):
    """Subtract two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The difference of a and b
    """
    return a - b


def multiply(a, b):
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        The product of a and b
    """
    return a * b


def divide(a, b):
    """Divide two numbers.
    
    Args:
        a: Dividend
        b: Divisor
    
    Returns:
        The quotient of a and b
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def calculate_velocity(distance: float, time: float) -> float:
    if time <= 0:
        raise ValueError("Time must be greater than zero")
    return distance / time



def main():
    """Interactive calculator."""
    print("Simple Calculator")
    print("-" * 30)
    
    while True:
        print("\nOperations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("Enter choice (1/2/3/4/5): ").strip()
        
        if choice == "5":
            print("Thank you for using the calculator!")
            break
        
        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please try again.")
            continue
        
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
            continue
        
        if choice == "1":
            print(f"{num1} + {num2} = {add(num1, num2)}")
        elif choice == "2":
            print(f"{num1} - {num2} = {subtract(num1, num2)}")
        elif choice == "3":
            print(f"{num1} * {num2} = {multiply(num1, num2)}")
        elif choice == "4":
            try:
                print(f"{num1} / {num2} = {divide(num1, num2)}")
            except ValueError as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
