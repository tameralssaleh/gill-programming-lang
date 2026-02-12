from dataclasses import dataclass
from typing import Literal
from environment import Env

### Runtime System (RTS) Classes for Gill
# These classes represent the runtime entities in the Gill programming language, such as variables and functions. 
# They are used by the interpreter to manage the execution of Gill programs.
#
# If you are creating your own native modules in Python, you will need to create instances of these classes to represent the variables and functions you want to expose to Gill code.
# Use NativeVariable for simple variables and NativeFunction for functions. The Interpreter will look up these entities in the global environment when executing Gill code.
# ParameterSpec is used to define the parameters of native functions, including their types and default values.

class NativeVariable:
    def __init__(self, name, type_, py_impl):
        self.name = name
        self.type_ = type_
        self.py_impl = py_impl

class ParameterSpec:
    POSITIONAL = "positional"
    VARARGS = "varargs"
    KEYWORDS = "keywords"
    KWARGS = "kwargs"
    NO_DEFAULT = object()

    def __init__(self, name, type_, default_value=NO_DEFAULT, kind=POSITIONAL):
        self.name = name
        self.type_ = type_
        self.default_value = default_value
        self.kind = kind  # "positional", "varargs", later "kwargs", etc.

    @property
    def has_default(self):
        return self.default_value is not self.NO_DEFAULT

class NativeFunction:
    def __init__(self, name, parameters, py_impl):
        self.name = name
        self.parameters = parameters
        self.py_impl = py_impl

# MemberRef is not meant to be used for developing native modules, but it is used internally by the interpreter to represent references to variables and functions in the environment.
@dataclass(frozen=True)
class MemberRef:
    kind: Literal["function", "variable"]
    env: Env
    name: str
