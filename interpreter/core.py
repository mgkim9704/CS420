# interpreter.py
# Interpeter of our language

from typing import Dict, TypeVar, Union, Generic, List, Optional, Tuple, Generator, NamedTuple
from enum import Enum
from . import ast

Value = Union[int, float]
T = TypeVar('T', int, float)

Program = Dict[str, ast.Func]

# Control Flow Directive
CFD = Enum('CFD', 'Break Continue Return Go')

class Context(NamedTuple):
  env: Dict[str, int]
  mem: List[Value]

class Interpreter:

  # some evaluation context
  program: Program
  ctx: Context

  def __init__(self, p: ast.Program) -> None:
    self.program = {}
    self.ctx = Context({}, [])

    for f in p:
      if f.name in self.program:
        raise f'Duplicated function {f.name}'
      self.program[f.name] = f

  # run the given program
  # return: the return value of main function
  def run(self) -> Value:
    return self.eval_func('main', [])

  def eval_stmt(self, stmt: ast.Stmt) -> \
    Generator[Context, None, Tuple[CFD, Optional[Value]]]:

    # before actually evaluate statements,
    # yield our context.
    print (stmt)
    yield self.ctx

    if isinstance(stmt, ast.Stmt_For):
      init, cond, loop, body = stmt
      if init is not None:
        yield from self.eval_expr(init)

      if cond is None:
        cond = ast.Expr_Lit(1)
      
      # TODO: check type of condition
      while True:

        # before evaluation of expression...
        yield self.ctx
        vcond = yield from self.eval_expr(cond)
        if vcond == 0:
          break

        cfd, ret = yield from self.eval_block(body)
        if cfd == CFD.Break:
          return (CFD.Go, None)
        elif cfd == CFD.Return:
          return (CFD.Return, ret)

        # if cfd is CFD.Continue or CFD.Go, just keep going
        if loop is not None:
          yield from self.eval_expr(loop)
      
      return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_If):
      cond, body = stmt
      vcond = yield from self.eval_expr(cond)
      if vcond != 0:
        return (yield from self.eval_block(body))
      else:
        return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_Decl):
      tp, names = stmt
      for name, _ in names:
        if name in self.ctx.env:
          raise f'{name} is already declared vairable.'
        
        self.ctx.mem.append(0xcc)
        self.ctx.env[name] = len(self.ctx.mem) - 1

      return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_Expr):
      yield from self.eval_expr(stmt.expr)
      return (CFD.Go, None)

    elif isinstance(stmt, ast.Stmt_Break):
      return (CFD.Break, None)
    
    elif isinstance(stmt, ast.Stmt_Cont):
      return (CFD.Continue, None)

    elif isinstance(stmt, ast.Stmt_Return):
      vret = yield from self.eval_expr(stmt.retval)
      return (CFD.Return, vret)
    
    
  def eval_block(self, block: List[ast.Stmt]) -> \
    Generator[Context, None, Tuple[CFD, Optional[Value]]]:
    
    for stmt in block:
      cfd, ret = yield from self.eval_stmt(stmt)
      if cfd != CFD.Go:
        return (cfd, ret)
    
    return (CFD.Go, None)

  def eval_func(self, name: str, args: List[Value]) -> \
    Generator[Context, None, Value]:
    f = self.program[name]
    if len(f.arguments) != len(args):
      raise f'function {name} requires {len(f.arguments)} arguments, but' + \
        f'you\'re calling with {len(args)} arguments.'

    newenv: Dict[str, int] = {}
    fp = len(self.ctx.mem) # frame point
    for (tp, (arg_name, _)), arg in zip(f.arguments, args):
      if not isinstance(arg, {ast.Type.Int: int, ast.Type.Float: float}[tp]):
        raise f'{arg} doesn\'t have type {tp}.'
      if arg in newenv:
        raise f'function {name} has duplicated arguments.'

      self.ctx.mem.append(arg)
      newenv[arg_name] = len(self.ctx.mem) - 1

    beforeenv = self.ctx.env
    self.ctx = Context(newenv, self.ctx.mem)

    cfd, ret = yield from self.eval_block(f.body)

    if ret == None:
      assert cfd != CFD.Return
      raise f'function {name} stopped with unexpected control flow directive.'

    del self.ctx.mem[fp:]
    self.ctx = Context(beforeenv, self.ctx.mem)
    return ret
  
  def eval_expr(self, expr: ast.Expr) -> Generator[Context, None, Value]:
    if isinstance(expr, ast.Expr_Var):
      name = expr
      return self.ctx.mem[self.ctx.env[name]]

    elif isinstance(expr, ast.Expr_Lit):
      if isinstance(expr.val, str):
        raise 'You cannot use string literal but in printf function.'
      val = expr.val
      return val
    
    elif isinstance(expr, ast.Expr_Bin):
      bop, (e1, e2) = expr
      return (yield from self.binop(bop, e1, e2))

    elif isinstance(expr, ast.Expr_Un):
      uop, e = expr
      return (yield from self.unop(uop, e))

    elif isinstance(expr, ast.Expr_Call):
      name, args = expr
      if name == 'printf':
        fstr = args[0]
        args = args[1:]

        if not isinstance(fstr, str):
          raise 'First argument of printf function must be a string literal.'

        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg)
          vargs.append(varg)
        
        s = fstr % tuple(vargs)
        print(s)
        return len(s)

      else:
        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg)
          vargs.append(varg)
        
        return (yield from self.eval_func(name, vargs))
    
    else:
      raise ''

  def binop(self, op: ast.BinOp, e1: ast.Expr, e2: ast.Expr) -> \
    Generator[Context, None, Value]:
    if op != ast.BinOp.Asgn:
      v1 = yield from self.eval_expr(e1)
      v2 = yield from self.eval_expr(e2)

    if op == ast.BinOp.Add:
      return v1 + v2
    elif op == ast.BinOp.Sub:
      return v1 - v2
    elif op == ast.BinOp.Mul:
      return v1 * v2
    elif op == ast.BinOp.Div:
      return v1 / v2
    elif op == ast.BinOp.Gt:
      return 1 if v1 > v2 else 0
    elif op == ast.BinOp.Le:
      return 1 if v1 < v2 else 0
    elif op == ast.BinOp.And:
      return v1 and v2
    elif op == ast.BinOp.Or:
      return v1 or v2
    elif op == ast.BinOp.Asgn:
      if isinstance(e1, ast.Expr_Var):
        v = yield from self.eval_expr(e2)
        self.ctx.mem[self.ctx.env[e1]] = v
        return v
      else:
        raise f'{e1} is not a l-value.'
    else:
      raise ''
  
  def unop(self, op: ast.UnOp, e: ast.Expr) -> Generator[Context, None, Value]:
    
    if op == ast.UnOp.Inc:
      if isinstance(e, ast.Expr_Var):
        v = self.ctx.mem[self.ctx.env[e]]
        self.ctx.mem[self.ctx.env[e]] = v + 1
        return v
      else:
        raise f'{e} is not a l-value.'

    elif op == ast.UnOp.Dec:
      if isinstance(e, ast.Expr_Var):
        v = self.ctx.mem[self.ctx.env[e]]
        self.ctx.mem[self.ctx.env[e]] = v - 1
        return v
      else:
        raise f'{e} is not a l-value.'

    else:
      raise ''

    yield

#######################################################################
# Some test cases
#######################################################################

def test1():
  ex = ast.Func('test', [], ast.Type.Int, False, [ast.Stmt_Return(ast.Expr_Lit(3))])
  myint = Interpreter([ex])
  print(myint.eval_func('test', []))

def test2():
  ex = ast.Func('test', [], ast.Type.Int, False, [ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Add, (ast.Expr_Lit(1), ast.Expr_Lit(4))))])
  myint = Interpreter([ex])
  print(myint.eval_func('test', []))

def test3():
  ex = ast.Func('twice', [(ast.Type.Int, ast.DecoratedName('f', False))], ast.Type.Int, False, [ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Mul, (ast.Expr_Var('f'), ast.Expr_Lit(2))))])
  myint = Interpreter([ex])
  print(myint.eval_func('twice', [2]))

def cfd_if():
  ex = ast.Func('choice', [(ast.Type.Int, ast.DecoratedName('x', False))], ast.Type.Int, False, [ast.Stmt_If(ast.Expr_Bin(ast.BinOp.Gt, (ast.Expr_Var('x'), ast.Expr_Lit(3))), [ast.Stmt_Return(ast.Expr_Lit(1))]), ast.Stmt_Return(ast.Expr_Lit(0))])

  myint = Interpreter([ex])
  print(myint.eval_func('choice', [4]))
  myint = Interpreter([ex])
  print(myint.eval_func('choice', [1]))

def fact():
  ex = ast.Func('fact', [(ast.Type.Int, ast.DecoratedName('x', False))], ast.Type.Int, False, [ast.Stmt_If(ast.Expr_Bin(ast.BinOp.Le, (ast.Expr_Var('x'), ast.Expr_Lit(2))), [ast.Stmt_Return(ast.Expr_Var('x'))]), ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Mul, (ast.Expr_Var('x'), ast.Expr_Call('fact', [ast.Expr_Bin(ast.BinOp.Sub, (ast.Expr_Var('x'), ast.Expr_Lit(1)))]))))])

  myint = Interpreter([ex])
  print(myint.eval_func('fact', [5]))

tests = [test1, test2, test3, cfd_if, fact]

def loadTest():
  ex = ast.Func('fact', [(ast.Type.Int, ast.DecoratedName('x', False))], ast.Type.Int, False, [ast.Stmt_If(ast.Expr_Bin(ast.BinOp.Le, (ast.Expr_Var('x'), ast.Expr_Lit(2))), [ast.Stmt_Return(ast.Expr_Var('x'))]), ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Mul, (ast.Expr_Var('x'), ast.Expr_Call('fact', [ast.Expr_Bin(ast.BinOp.Sub, (ast.Expr_Var('x'), ast.Expr_Lit(1)))]))))])

  myint = Interpreter([ex])
  return myint

if __name__ == '__main__':
  for t in tests:
    t()
