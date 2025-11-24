import re
from typing import Any

# STANDARD LIBRARY FOR GIL
# This file contains built-in functions and definitions for the GIL language.

def printf(*args):
    """Prints a formatted string.
    """
    main_string = args[0]
    place_holder_values = args[1:]
    print(main_string.format(*place_holder_values))


def printfr(*args):
    """Prints a formatted string and returns it.
    Returns:
        str: The formatted string that was printed.
    """
    main_string = args[0]
    place_holder_values = args[1:]
    formatted = main_string.format(*place_holder_values)
    print(formatted)
    return formatted

def str_len(s: str) -> int:
    """Returns the length of the given string.
    Args:
        s (str): The input string.
    Returns:
        int: The length of the string.
    """
    return len(s)

def pow(base: float, exponent: float) -> float:
    """Returns the result of raising base to the power of exponent.
    Args:
        base (float): The base number.
        exponent (float): The exponent number.
    Returns:
        float: The result of base raised to the power of exponent.
    """
    return base ** exponent

