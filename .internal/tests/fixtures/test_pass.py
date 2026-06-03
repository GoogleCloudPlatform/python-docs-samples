# test_pass.py
import os


def calculate_square(number: int) -> int:
    """Calculates the square of a given integer."""
    result = number * number
    print(f"The result is: {result}")
    return result


if __name__ == "__main__":
    # Ensure a basic execution works cleanly
    current_directory = os.getcwd()
    calculate_square(5)
