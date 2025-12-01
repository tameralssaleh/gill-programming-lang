import re
import sys
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

def sizeof(object: Any) -> int:
    """Returns the size of the given object in bytes.
    Args:
        object (Any): The input object.
    Returns:
        int: The size of the object in bytes.
    """
    return sys.getsizeof(object)

def pow(base: float, exponent: float) -> float:
    """Returns the result of raising base to the power of exponent.
    Args:
        base (float): The base number.
        exponent (float): The exponent number.
    Returns:
        float: The result of base raised to the power of exponent.
    """
    return base ** exponent

class Conversion:
    @staticmethod
    def to_int(value: Any) -> int:
        """Converts the given value to an integer.
        Args:
            value (Any): The input value.
        Returns:
            int: The converted integer value.
        """
        return int(value)

    @staticmethod
    def to_float(value: Any) -> float:
        """Converts the given value to a float.
        Args:
            value (Any): The input value.
        Returns:
            float: The converted float value.
        """
        return float(value)

    @staticmethod
    def to_string(value: Any) -> str:
        """Converts the given value to a string.
        Args:
            value (Any): The input value.
        Returns:
            str: The converted string value.
        """
        return str(value)
