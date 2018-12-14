# ast.py
# type declarations of AST

from typing import List, Union, NamedTuple, Optional, NewType, Tuple
from enum import Enum

BinOp = Enum('BinOp', 'Add Sub Mul Div Gt Le Asgn Idx And Or')
UnOp = Enum('UnOp', 'Inc Dec Deref')

Type = Enum('Type', 'Int Float')

class DecoratedName(NamedTuple):
  name: str
  # false: No deco, true: pointer, (int): array length
  decorator: Union[bool, int]

Expr_Var = NewType('Expr_Var', str)
Expr_Lit = NewType('Expr_Lit', Union[int, float])

class Expr_Bin(NamedTuple):
  operator: BinOp
  operand: Tuple['Expr', 'Expr']

class Expr_Un(NamedTuple):
  operator: UnOp
  operand: 'Expr'

class Expr_Call(NamedTuple):
  func_name: str
  arguments: List['Expr']

Expr = Union[Expr_Var, Expr_Lit, Expr_Bin, Expr_Un, Expr_Call]

class Stmt_For(NamedTuple):
  init: Optional[Expr]
  cond: Optional[Expr]
  loop: Optional[Expr]
  body: List['Stmt']

class Stmt_If(NamedTuple):
  cond: Expr
  body: List['Stmt']

class Stmt_Decl(NamedTuple):
  basetype: Type
  names: List[DecoratedName]

Stmt_Return = NewType('Stmt_Return', Expr)
Stmt_Expr = NewType('Stmt_Expr', Expr)
Stmt_Break = NewType('Stmt_Break', None)
Stmt_Cont = NewType('Stmt_Cont', None)
Stmt_Mpty = NewType('Stmt_Mpty', None)

# first elem of tuple means the line number of this statement.
Stmt = Tuple[int, Union[Stmt_For, Stmt_If, Stmt_Return, Stmt_Decl, Stmt_Break, Stmt_Cont, Stmt_Expr, Stmt_Mpty]]

class Func(NamedTuple):
  name: str
  arguments: List[Tuple[Type, DecoratedName]]
  # 'void' => None
  ret_type: Optional[Type]
  ret_type_is_pointer: bool
  body: List[Stmt]

Program = List[Func]
