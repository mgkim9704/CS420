# interpreter/context.py
# Intermediate outcomes under evaluation

from typing import NamedTuple, Union, Dict, List, Tuple, Optional
from enum import Enum
from . import ast

Value = Union[int, float]

BaseType = ast.Type

class Type_Ptr(NamedTuple):
  alias_t: BaseType

class Type_Array(NamedTuple):
  elem_t: BaseType
  size: int

Type = Union[BaseType, Type_Ptr, Type_Array]

Program = Dict[str, ast.Func]

# Control Flow Directive
CFD = Enum('CFD', 'Break Continue Return Go')

class InterpreterError(Exception):

  message: str
  def __init__(self, message):
    self.message = message

class Context(NamedTuple):
  env: Dict[str, Tuple[int, Type]]
  mem: List[Optional[Value]]

  def add(self, var_name: str, t: Type):
    # None means 'not assgined yet'
    if var_name in self.env:
      raise InterpreterError(f'{var_name} is already declared vairable.')
        
    self.mem.append(None)
    self.env[var_name] = (len(self.mem) - 1, t)

  def assign(self, var_name: str, value: Value):
    x, t = self.env[var_name]
    self.mem[x] = value
    