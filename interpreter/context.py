# interpreter/context.py
# Intermediate outcomes under evaluation

from typing import NamedTuple, Union, Dict, List, Tuple, Optional, TypeVar, Generator
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

# TypedValue is the result of evaluation of expression.
# The type in TypedValue must not be Type_Array (not 1st-class type)
TypedValue = Tuple[Type, Value]

Program = Dict[str, ast.Func]

# Control Flow Directive
CFD = Enum('CFD', 'Break Continue Return Go')

def get_type(bt: BaseType, deco: Union[bool, int]) -> Type:
  if deco is False:
    return bt
  elif deco is True:
    return Type_Ptr(bt)
  else:
    return Type_Array(bt, deco)

def cast(value: TypedValue, to_t: Type) -> Value:
  from_t, v = value
  assert not isinstance(from_t, Type_Array)
  if isinstance(to_t, Type_Array):
    raise InterpreterError('Cannot convert any value into an array.')
  if isinstance(to_t, Type_Ptr) and from_t == BaseType.Float:
    raise InterpreterError('Cannot convert any float into a pointer.')
  
  if isinstance(to_t, Type_Ptr) and from_t == BaseType.Int:
    print('Warning: converting an integer into a pointer may be harmful.')
  if isinstance(to_t, Type_Ptr) and isinstance(from_t, Type_Ptr) and \
    to_t.alias_t != from_t.alias_t:
    print('Warning: converting a pointer to different object type causes \n undefined behavior. (References: C11 spec ISO/IEC 9899:201x, 6.3.2.3.7)')
  
  if to_t == BaseType.Float:
    return float(v)
  else:
    return int(v)

class InterpreterError(Exception):

  message: str
  def __init__(self, message):
    self.message = message

class Context():
  env: Dict[str, Tuple[Type, int]]
  mem: List[Optional[Value]]

  def __init__(self):
    self.env = {}
    self.mem = []

  # Declare a new variable and return its address. 
  def add(self, var_name: str, t: Type) -> int:
    # None means 'not assgined yet'
    if var_name in self.env:
      raise InterpreterError(f'{var_name} is already declared vairable.')
      
    addr = len(self.mem)
    if isinstance(t, Type_Array):
      if t.size < 0:
        raise InterpreterError('An array must have non-negative size.')
      self.mem += [None] * t.size
    else:
      self.mem.append(None)
    self.env[var_name] = (t, addr)
    return addr

  def read(self, addr: int) -> Value:
    if addr >= len(self.mem):
      raise InterpreterError('Segmentation Fault')
    else:
      v = self.mem[addr]
      if v is None:
        raise InterpreterError('Cannot read uninitalized memory')
      else:
        return v

  def write(self, addr: int, v: Value):
    if addr >= len(self.mem):
      raise InterpreterError('Segmentation Fault')
    
    self.mem[addr] = v

  def new_frame(self) -> Tuple[Dict[str, Tuple[int, Type]], int]:
    ret = (self.env, len(self.mem))
    self.env = {}
    return ret

  def restore_frame(self, frame: Tuple[Dict[str, Tuple[int, Type]], int]):
    self.env, fp = frame
    del self.mem[fp:]

  def __repr__(self):
    return f'({self.env}, {self.mem})'
  

T = TypeVar('T')
Evaluation = Generator[Context, None, T]
