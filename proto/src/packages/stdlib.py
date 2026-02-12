import sys
from environment import ModuleEnv
from rts import *
from typing import Any

# STANDARD LIBRARY FOR GIL
# This file contains built-in functions and definitions for the GIL language.

### Variables
version = "0.0.1"  # Version of the GIL language

### Functions

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

"""
REGISTER ALL STDLIB FUNCTIONS AND VARIABLES IN THE MODULE ENVIRONMENT
"""

# Create a module environment for the standard library to register functions
# The module name should reflect the python file...
# Every single function name for the key in the functions dict should reflect the name of the Python implementation of the function.
# -- -- To further clarify.. This technically is not critical, but it is nice to have some consistency here.
# NativeFunctionNode takes the function name, parameters (as list of ParameterSpec), and the python implementation.
# ParameterSpec takes in a 'kind' parameter. Note that this parameter is optional and defaults to literal "positional".
# Note that the parameters can be an empty list if there are no parameters.

#                    Module Name (should reflect name of python file) (i.e. stdlib.py)
#                         |
module_env = ModuleEnv("stdlib")

# Functions to register in the stdlib module
module_env.functions = {
    "printf": NativeFunction("printf", [ParameterSpec("format", "string", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL), ParameterSpec("args", "varargs", kind=ParameterSpec.VARARGS)], printf),
    "printfr": NativeFunction("printfr", [ParameterSpec("format", "string", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL), ParameterSpec("args", "varargs", kind=ParameterSpec.VARARGS)], printfr),
    "str_len": NativeFunction("str_len", [ParameterSpec("s", "string", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL)], str_len),
    "sizeof": NativeFunction("sizeof", [ParameterSpec("object", "var", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL)], sizeof),
    "pow": NativeFunction("pow", [ParameterSpec("base", "float", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL), ParameterSpec("exponent", "float", ParameterSpec.NO_DEFAULT, ParameterSpec.POSITIONAL)], pow)
}

# Variables to register in the stdlib module
# Just like functions, the variable name should match the same of the variable's python implementation.
module_env.variables = {
    "version": NativeVariable("version", "string", version)
}
