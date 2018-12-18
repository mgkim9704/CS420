# ast.py
# type declarations of AST

from typing import List, Union, NamedTuple, Optional, NewType, Tuple
from enum import Enum

BinOp = Enum('BinOp', 'Add Sub Mul Div Mod Eq Ne Lt Gt Le Ge Asgn Idx And Or')
UnOp = Enum('UnOp', 'Inc Dec Deref')

Type = Enum('Type', 'Int Float')

class DecoratedName(NamedTuple):
  name: str
  decorator: Union[bool, int] # false: No deco, true: pointer, (int): array length

Expr_Var = str

class Expr_Lit(NamedTuple):
  val: Union[int, float, str]

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

class Stmt_Comp(NamedTuple):
  body: List['SpannedStmt']

class Stmt_For(NamedTuple):
  init: Optional[Expr]
  cond: Optional[Expr]
  loop: Optional[Expr]
  body: 'SpannedStmt'

class Stmt_If(NamedTuple):
  cond: Expr
  body: 'SpannedStmt'

class Stmt_Decl(NamedTuple):
  basetype: Type
  names: List[DecoratedName]

class Stmt_Return(NamedTuple):
  retval: Optional[Expr]

class Stmt_Expr(NamedTuple):
  expr: Expr

class Stmt_Break:
  pass

class Stmt_Cont:
  pass

class Stmt_Mpty:
  pass

# first elem of tuple means the line number of this statement.
Stmt = Union[Stmt_Comp, Stmt_For, Stmt_If, Stmt_Return, Stmt_Decl, Stmt_Break, Stmt_Cont, Stmt_Expr, Stmt_Mpty]
SpannedStmt = Tuple[int, Stmt]
class Func(NamedTuple):
  name: str
  arguments: List[Tuple[Type, DecoratedName]]
  # 'void' => None
  ret_type: Optional[Type]
  ret_type_is_pointer: bool
  body: Tuple[int, Stmt_Comp]

Program = List[Func]
