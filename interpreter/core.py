# interpreter.py
# Interpeter of our language

from typing import Dict, TypeVar, Union, Generic, List, Optional, Tuple, Generator, NamedTuple
from . import ast
from .context import *

def b2v(b: bool) -> Value:
  return 1 if b else 0

def v2b(v: Value) -> bool:
  return (v != 0)

def get_type(bt: BaseType, deco: Union[bool, int]) -> Type:
  if deco is False:
    return bt
  elif deco is True:
    return Type_Ptr(bt)
  else:
    return Type_Array(bt, deco)

class Interpreter:

  # some evaluation context
  program: Program
  ctx: Context

  def __init__(self, p: ast.Program) -> None:
    self.program = {}
    self.ctx = Context()

    for f in p:
      if f.name in self.program:
        raise InterpreterError(f'Duplicated function {f.name}')
      self.program[f.name] = f

  # run the given program
  # return: the return value of main function
  def run(self) -> Value:
    evaluation = self.eval_func('main', [])
    while True:
      try:
        next(evaluation)
      except StopIteration as e:
        return e.value
    
  def eval_stmt(self, stmt: ast.Stmt) -> \
    Evaluation[Tuple[CFD, Optional[Value]]]:

    # before actually evaluate statements,
    # yield our context.
    print (stmt)
    yield self.ctx

    if isinstance(stmt, ast.Stmt_Comp):
      body = stmt.body
      return (yield from self.eval_block(body))

    elif isinstance(stmt, ast.Stmt_For):
      init, cond, loop, (ln, body) = stmt
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

        cfd, ret = yield from self.eval_stmt(body)
        if cfd == CFD.Break:
          return (CFD.Go, None)
        elif cfd == CFD.Return:
          return (CFD.Return, ret)

        # if cfd is CFD.Continue or CFD.Go, just keep going
        if loop is not None:
          yield from self.eval_expr(loop)
      
      return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_If):
      cond, (ln, body) = stmt
      vcond = yield from self.eval_expr(cond)
      if vcond != 0:
        return (yield from self.eval_stmt(body))
      else:
        return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_Decl):
      basetype, names = stmt
      for name, deco in names:
        t = get_type(basetype, deco)
        self.ctx.add(name, t)
        
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
    
    
  def eval_block(self, block: List[ast.SpannedStmt]) -> \
    Evaluation[Tuple[CFD, Optional[Value]]]:
    
    for ln, stmt in block:
      cfd, ret = yield from self.eval_stmt(stmt)
      if cfd != CFD.Go:
        return (cfd, ret)
    
    return (CFD.Go, None)

  def eval_func(self, name: str, args: List[Value]) -> \
    Evaluation[Value]:
    f = self.program[name]
    if len(f.arguments) != len(args):
      raise InterpreterError(f'function {name} requires {len(f.arguments)} arguments, but you\'re calling with {len(args)} arguments.')

    fp = len(self.ctx.mem) # frame point
    frame = self.ctx.new_frame()
    for (tp, (arg_name, _)), arg in zip(f.arguments, args):
      if not isinstance(arg, {ast.Type.Int: int, ast.Type.Float: float}[tp]):
        raise InterpreterError(f'{arg} doesn\'t have type {tp}.')

      self.ctx.add(arg_name, tp)
      self.ctx.assign(arg_name, arg)

    cfd, ret = yield from self.eval_stmt(f.body[1])

    if ret == None:
      assert cfd != CFD.Return
      raise InterpreterError(f'function {name} stopped with unexpected control flow directive.')

    self.ctx.restore_frame(frame)
    return ret
  
  def eval_expr(self, expr: ast.Expr) -> Evaluation[Value]:
    if isinstance(expr, ast.Expr_Var):
      name = expr
      return self.ctx.get(name)

    elif isinstance(expr, ast.Expr_Lit):
      if isinstance(expr.val, str):
        raise InterpreterError('You cannot use string literal but in printf function.')
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

        if not isinstance(fstr, ast.Expr_Lit) or not isinstance(fstr.val, str):
          raise InterpreterError('First argument of printf function must be a string literal.')

        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg)
          vargs.append(varg)
        
        s = fstr.val % tuple(vargs)
        print(s)
        return len(s)

      else:
        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg)
          vargs.append(varg)
        
        return (yield from self.eval_func(name, vargs))
    
    else:
      raise NotImplementedError

  def binop(self, op: ast.BinOp, e1: ast.Expr, e2: ast.Expr) -> \
    Evaluation[Value]:
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
    elif op == ast.BinOp.Mod:
      return v1 % v2
    elif op == ast.BinOp.Eq:
      return v1 == v2
    elif op == ast.BinOp.Ne:
      return v1 != v2
    elif op == ast.BinOp.Lt:
      return b2v(v1 < v2)
    elif op == ast.BinOp.Gt:
      return b2v(v1 > v2)
    elif op == ast.BinOp.Le:
      return b2v(v1 <= v2)
    elif op == ast.BinOp.Ge:
      return b2v(v1 >= v2)
    # todo: short-circuit
    elif op == ast.BinOp.And:
      return b2v(v2b(v1) and v2b(v2))
    elif op == ast.BinOp.Or:
      return b2v(v2b(v1) or v2b(v2))
    elif op == ast.BinOp.Asgn:
      if isinstance(e1, ast.Expr_Var):
        v = yield from self.eval_expr(e2)
        self.ctx.assign(e1, v)
        return v
      else:
        raise InterpreterError(f'{e1} is not a l-value.')
    else:
      raise NotImplementedError
  
  def unop(self, op: ast.UnOp, e: ast.Expr) -> Evaluation[Value]:
    
    if op == ast.UnOp.Inc:
      if isinstance(e, ast.Expr_Var):
        v = self.ctx.get(e)
        self.ctx.assign(e, v + 1)
        return v
      else:
        raise InterpreterError(f'{e} is not a l-value.')

    elif op == ast.UnOp.Dec:
      if isinstance(e, ast.Expr_Var):
        v = self.ctx.get(e)
        self.ctx.assign(e, v - 1)
        return v
      else:
        raise InterpreterError(f'{e} is not a l-value.')

    else:
      raise NotImplementedError

    yield

#######################################################################
# Some test cases
#######################################################################

def test1():
  ex = ast.Func('test', [], ast.Type.Int, False, ast.Stmt_Comp([ast.Stmt_Return(ast.Expr_Lit(3))]))
  myint = Interpreter([ex])
  print(myint.eval_func('test', []))

def test2():
  ex = ast.Func('test', [], ast.Type.Int, False, ast.Stmt_Comp([ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Add, (ast.Expr_Lit(1), ast.Expr_Lit(4))))]))
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
  ex = ast.Func('fact', [(ast.Type.Int, ast.DecoratedName('x', False))], ast.Type.Int, False, ast.Stmt_Comp([ast.Stmt_If(ast.Expr_Bin(ast.BinOp.Le, (ast.Expr_Var('x'), ast.Expr_Lit(2))), ast.Stmt_Comp([ast.Stmt_Return(ast.Expr_Var('x'))])), ast.Stmt_Return(ast.Expr_Bin(ast.BinOp.Mul, (ast.Expr_Var('x'), ast.Expr_Call('fact', [ast.Expr_Bin(ast.BinOp.Sub, (ast.Expr_Var('x'), ast.Expr_Lit(1)))]))))]))

  myint = Interpreter([ex])
  return myint

if __name__ == '__main__':
  for t in tests:
    t()
