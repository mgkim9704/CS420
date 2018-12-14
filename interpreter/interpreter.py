# interpreter.py
# Interpeter of our language

from typing import Dict, TypeVar, Union, Generic, List, Optional
import ast

Value = Union[int, float]
T = TypeVar('T', int, float)

Program = Dict[str, ast.Func]

class Interpeter:

  # some evaluation context
  program: Program
  env: Dict[str, int]
  mem: List[Value]
  breakable: bool

  def __init__(self, p: ast.Program) -> None:
    self.program = {}
    self.env = {}
    self.mem = []

    for f in p:
      if f.name in self.program:
        raise 'NameError'

  # run the given program
  # return: the return value of main function
  def run(self) -> Optional[int]:
    return self.eval_func('main', [])

  def eval_stmt(self, stmt: ast.Stmt) -> Optional[Value]:

    if isinstance(stmt, ast.Stmt_For):
      init, cond, loop, body = stmt
      if init is not None:
        self.eval_expr(init)
      if cond is None:
        cond = ast.Expr_Lit(1)
      
      # TODO: check type of condition
      while self.eval_expr(cond) != 0:
        self.eval_block(body)
        if loop is not None:
          self.eval_expr(loop)
    
    elif isinstance(stmt, ast.Stmt_If):
      cond, body = stmt
      if self.eval_expr(cond) != 0:
        self.eval_block(body)
    
    elif isinstance(stmt, ast.Stmt_Decl):
      tp, names = stmt
      for name, _ in names:
        if name in self.env:
          raise f'{name} is already declared vairable.'
        
        self.mem.append(0xcc)
        self.env[name] = len(self.mem) - 1
    
    elif isinstance(stmt, ast.Stmt_Expr):
      return self.eval_expr(stmt)
    else:
      raise ''
    
    
  def eval_block(self, block: List[ast.Stmt]) -> Optional[Value]:
    
    v = None
    for stmt in block:
      v = self.eval_stmt(stmt)
    
    return v

  def eval_func(self, name: str, args: List[Value]) -> Optional[Value]:
    f = self.program[name]
    if len(f.arguments) != len(args):
      raise f'function {name} requires {len(f.arguments)} arguments, but' + \
        f'you\'re calling with {len(args)} arguments.'

    newenv = {}
    fp = len(self.mem) # frame point
    for (tp, (arg_name, _)), arg in zip(f.arguments, args):
      if not isinstance(arg, {ast.Type.Int: int, ast.Type.Float: float}[tp]):
        raise f'{arg} doesn\'t have type {tp}.'
      if arg in newenv:
        raise f'function {name} has duplicated arguments.'

      self.mem.append(arg)
      newenv[arg_name] = len(self.mem) - 1

    beforeenv = self.env
    self.env = newenv

    ret = self.eval_block(f.body)
    del self.mem[fp:]
    self.env = beforeenv
    return ret
  
  def eval_expr(self, expr: ast.Expr) -> Value:
    if isinstance(expr, ast.Expr_Var):
      name = expr.name
      return self.mem[self.env[name]]

    elif isinstance(expr, ast.Expr_Lit):
      val = expr.val
      return val
    
    elif isinstance(expr, ast.Expr_Bin):
      op, (e1, e2) = expr
      return self.binop(op, e1, e2)

    elif isinstance(expr, ast.Expr_Un):
      op, e = expr
      return self.unop(op, e)

    elif isinstance(expr, ast.Expr_Call):
      name, args = expr
      vars = [self.eval_expr(arg) for arg in args]
      return self.eval_func(name, vars)

  def binop(self, op: ast.BinOp, e1: ast.Expr, e2: ast.Expr) -> Value:
    if op == ast.BinOp.Add:
      return self.eval_expr(e1) + self.eval_expr(e2)
    elif op == ast.BinOp.Sub:
      return self.eval_expr(e1) - self.eval_expr(e2)
    elif op == ast.BinOp.Mul:
      return self.eval_expr(e1) * self.eval_expr(e2)
    elif op == ast.BinOp.Div:
      return self.eval_expr(e1) / self.eval_expr(e2)
    elif op == ast.BinOp.Gt:
      return self.eval_expr(e1) > self.eval_expr(e2)
    elif op == ast.BinOp.Le:
      return self.eval_expr(e1) < self.eval_expr(e2)
    elif op == ast.BinOp.And:
      return self.eval_expr(e1) and self.eval_expr(e2)
    elif op == ast.BinOp.Or:
      return self.eval_expr(e1) or self.eval_expr(e2)
    elif op == ast.BinOp.Asgn:
      if isinstance(e1, ast.Expr_Var):
        v = self.eval_expr(e2)
        self.mem[self.env[e1]] = v
        return v
      else:
        raise f'{e1} is not a l-value.'
    else:
      raise ''
  
  def unop(self, op: ast.UnOp, e: ast.Expr) -> Value:
    
    if op == ast.UnOp.Inc:
      if isinstance(e, ast.Expr_Var):
        v = self.mem[self.env[e]]
        self.mem[self.env[e]] = v + 1
        return v
    elif op == ast.UnOp.Dec:
      if isinstance(e, ast.Expr_Var):
        v = self.mem[self.env[e]]
        self.mem[self.env[e]] = v - 1
        return v
    else:
      raise ''
