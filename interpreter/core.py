# interpreter.py
# Interpeter of our language

from typing import Dict, TypeVar, Union, Generic, List, Optional, Tuple, Generator, NamedTuple
from . import ast
from .context import *

def b2v(b: bool) -> Value:
  return 1 if b else 0

def v2b(v: Value) -> bool:
  return (v != 0)

def devoid(v: Optional[TypedValue]) -> TypedValue:
  if v is None:
    raise InterpreterError('Cannot use result of void function.')
  return v

class Interpreter:

  # some evaluation context
  program: Program
  ctx: Context
  verbose: bool

  def __init__(self, p: ast.Program) -> None:
    self.program = {}
    self.ctx = Context()
    self.verbose = False

    for f in p:
      if f.name in self.program:
        raise InterpreterError(f'Duplicated function {f.name}')
      self.program[f.name] = f

  # run the given program
  # return: the return value of main function
  def run(self) -> TypedValue:
    evaluation = self.eval_func('main', [], 0)
    while True:
      try:
        next(evaluation)
      except StopIteration as e:
        return e.value
    
  def eval_stmt(self, stmt: ast.Stmt, ln: int) -> \
    Evaluation[Tuple[CFD, Optional[TypedValue]]]:

    # before actually evaluate statements,
    # yield our context.
    print (stmt) if self.verbose else ()
    yield self.ctx

    if isinstance(stmt, ast.Stmt_Comp):
      body = stmt.body

      # Any function call doesn't use eval_stmt(Stmt_Comp(...)) but
      # directly call eval_block because they have to manage their
      # own environment.
      # Here, when we evaluate a statement block, we have to make
      # additional empty environment supporting variable shadowing.
      # Also, allocated stack inside of this block will be free after
      # exiting the block.

      fp = self.ctx.new_nested_env()
      ret = yield from self.eval_block(body)
      self.ctx.drop_innermost_env(fp)
      return ret

    elif isinstance(stmt, ast.Stmt_For):
      init, cond, loop, (ln_inner, body) = stmt
      if init is not None:
        yield from self.eval_expr(init, ln)

      if cond is None:
        cond = ast.Expr_Lit(1)
      
      # TODO: check type of condition
      while True:

        # before evaluation of expression...
        yield self.ctx
        vcond = yield from self.eval_expr(cond, ln)
        bcond = v2b(cast(devoid(vcond), BaseType.Int))
        if bcond == False:
          break

        cfd, ret = yield from self.eval_stmt(body, ln_inner)
        if cfd == CFD.Break:
          return (CFD.Go, None)
        elif cfd == CFD.Return:
          return (CFD.Return, ret)

        # if cfd is CFD.Continue or CFD.Go, just keep going
        if loop is not None:
          yield from self.eval_expr(loop, ln)
      
      return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_If):
      cond, (ln_inner, body) = stmt
      vcond = yield from self.eval_expr(cond, ln)
      bcond = v2b(cast(devoid(vcond), BaseType.Int))
      if bcond:
        return (yield from self.eval_stmt(body, ln_inner))
      else:
        return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_Decl):
      basetype, names = stmt
      for name, deco in names:
        if basetype == None:
          raise InterpreterError('You cannot declare void type variable')
        t = get_type(basetype, deco)
        self.ctx.add(name, t, ln)
        
      return (CFD.Go, None)
    
    elif isinstance(stmt, ast.Stmt_Expr):
      yield from self.eval_expr(stmt.expr, ln)
      return (CFD.Go, None)

    elif isinstance(stmt, ast.Stmt_Break):
      return (CFD.Break, None)
    
    elif isinstance(stmt, ast.Stmt_Cont):
      return (CFD.Continue, None)

    elif isinstance(stmt, ast.Stmt_Return):
      vret = None
      if stmt.retval != None:
        vret = yield from self.eval_expr(stmt.retval, ln)
      return (CFD.Return, devoid(vret))
    
    raise NotImplementedError
    
  def eval_block(self, block: List[ast.SpannedStmt]) -> \
    Evaluation[Tuple[CFD, Optional[TypedValue]]]:
    
    for ln, stmt in block:
      cfd, ret = yield from self.eval_stmt(stmt, ln)
      if cfd != CFD.Go:
        return (cfd, ret)
    
    return (CFD.Go, None)

  def eval_func(self, name: str, args: List[TypedValue], ln: int, \
    cleanup: bool = True) -> Evaluation[Optional[TypedValue]]:
    f = self.program[name]
    if f.ret_type == None and f.ret_type_is_pointer:
      raise InterpreterError('We don\'t support a void pointer.')

    if len(f.arguments) != len(args):
      raise InterpreterError(f'function {name} requires {len(f.arguments)} arguments, but you\'re calling with {len(args)} arguments.')

    frame = self.ctx.new_frame()
    for (bt, (arg_name, deco)), arg in zip(f.arguments, args):
      t = get_type(bt, deco)
      addr = self.ctx.add(arg_name, t, ln)
      self.ctx.write(addr, cast(arg, t), ln)

    block = f.body[1]
    assert isinstance(block, ast.Stmt_Comp)
    cfd, ret = yield from self.eval_block(block.body)

    if cfd in [CFD.Break, CFD.Continue]:
      raise InterpreterError(f'function {name} stopped with unexpected control flow directive.')
    if cfd == CFD.Return and ret != None and f.ret_type == None:
      raise InterpreterError(f'Void function {name} returned somewhat strange.')
    if f.ret_type != None and ret == None:
      if name == 'main':
        # main function, specially, regarded as returning 0 if it didn't returned anything.
        ret = (BaseType.Int, 0)
      else:
        raise InterpreterError(f'Non-void function {name} didn\'t return anything.')

    if cleanup:
      self.ctx.restore_frame(frame)

    if ret != None:
      ret_t: Type = BaseType.Int
      if f.ret_type_is_pointer:
        ret_t = Type_Ptr(f.ret_type)
      else:
        ret_t = f.ret_type
      return (ret_t, cast(ret, ret_t))
    else:
      return None

  def eval_expr(self, expr: ast.Expr, ln: int) -> Evaluation[Optional[TypedValue]]:
    if isinstance(expr, ast.Expr_Var):
      name = expr
      t, addr = self.ctx.where(name)

      # evaluation of array variable automatically converted into a pointer
      # to the 0-th element of array.
      if isinstance(t, Type_Array):
        return (Type_Ptr(t.elem_t), addr)
      else:
        return (t, self.ctx.read(addr))

    elif isinstance(expr, ast.Expr_Lit):
      if isinstance(expr.val, str):
        raise InterpreterError('You cannot use string literal but in printf function.')
      val = expr.val
      return ({int: BaseType.Int, float: BaseType.Float}[type(val)], val)
    
    elif isinstance(expr, ast.Expr_Bin):
      bop, (e1, e2) = expr
      return (yield from self.binop(bop, e1, e2, ln))

    elif isinstance(expr, ast.Expr_Un):
      uop, e = expr
      return (yield from self.unop(uop, e, ln))

    elif isinstance(expr, ast.Expr_Call):
      name, args = expr
      if name == 'printf':
        fstr = args[0]
        args = args[1:]

        if not isinstance(fstr, ast.Expr_Lit) or not isinstance(fstr.val, str):
          raise InterpreterError('First argument of printf function must be a string literal.')

        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg, ln)
          vargs.append(devoid(varg))
        
        s = fstr.val % tuple(map(lambda a: a[1], vargs))
        print(s)
        return (BaseType.Int, len(s))

      else:
        vargs = []
        for arg in args:
          varg = yield from self.eval_expr(arg, ln)
          vargs.append(devoid(varg))
        
        return (yield from self.eval_func(name, vargs, ln))
    
    else:
      raise NotImplementedError

  def eval_lvalue(self, expr: ast.Expr, ln: int) -> Evaluation[Tuple[Type, int]]:
    if isinstance(expr, ast.Expr_Var):
      return self.ctx.where(expr)
    elif isinstance(expr, ast.Expr_Bin):
      op, (e1, e2) = expr
      if op == ast.BinOp.Idx:
        base = yield from self.eval_expr(e1, ln)
        delta = yield from self.eval_expr(e2, ln)
        base_t, baseaddr = devoid(base)
        delta_t, deltaaddr = devoid(delta)
        target_t = None
        if isinstance(base_t, Type_Ptr) and delta_t == BaseType.Int:
          target_t = base_t.alias_t 
        elif isinstance(delta_t, Type_Ptr) and base_t == BaseType.Int:
          target_t = delta_t.alias_t
        
        if target_t is None:
          raise InterpreterError(f'One of {e1} and {e2} should be an integer and the other should be a pointer.')
        
        assert type(baseaddr) == int and type(deltaaddr) == int
        return (target_t, baseaddr + deltaaddr)
      
    elif isinstance(expr, ast.Expr_Un):
      op, e = expr
      if op == ast.UnOp.Deref:
        pointer = yield from self.eval_expr(e, ln)
        t, addr = devoid(pointer)
        return (t.alias_t, addr)
      
    raise InterpreterError(f'{expr} is not a l-value.')

  # Evaluate a binary operation.
  # For simplicity, any pointers in e1 and/or e2 are regarded as an integer.
  def binop(self, op: ast.BinOp, e1: ast.Expr, e2: ast.Expr, ln: int) -> \
    Evaluation[TypedValue]:
    if op != ast.BinOp.Asgn:
      value1 = yield from self.eval_expr(e1, ln)
      value2 = yield from self.eval_expr(e2, ln)
      t1, v1 = devoid(value1)
      t2, v2 = devoid(value2)

    if op == ast.BinOp.Add:
      if t1 == BaseType.Float or t2 == BaseType.Float:
        return (BaseType.Float, v1 + v2)
      else:
        return (BaseType.Int, v1 + v2)
    elif op == ast.BinOp.Sub:
      if t1 == BaseType.Float or t2 == BaseType.Float:
        return (BaseType.Float, v1 - v2)
      else:
        return (BaseType.Int, v1 - v2)
    elif op == ast.BinOp.Mul:
      if t1 == BaseType.Float or t2 == BaseType.Float:
        return (BaseType.Float, v1 * v2)
      else:
        return (BaseType.Int, v1 * v2)
    elif op == ast.BinOp.Div:
      if t1 == BaseType.Float or t2 == BaseType.Float:
        return (BaseType.Float, v1 / v2)
      else:
        return (BaseType.Int, int(v1 / v2))
    elif op == ast.BinOp.Mod:
      if t1 == BaseType.Float or t2 == BaseType.Float:
        return (BaseType.Float, v1 % v2)
      else:
        return (BaseType.Int, v1 % v2)
    elif op == ast.BinOp.Eq:
      return (BaseType.Int, b2v(v1 == v2))
    elif op == ast.BinOp.Ne:
      return (BaseType.Int, b2v(v1 != v2))
    elif op == ast.BinOp.Lt:
      return (BaseType.Int, b2v(v1 < v2))
    elif op == ast.BinOp.Gt:
      return (BaseType.Int, b2v(v1 > v2))
    elif op == ast.BinOp.Le:
      return (BaseType.Int, b2v(v1 <= v2))
    elif op == ast.BinOp.Ge:
      return (BaseType.Int, b2v(v1 >= v2))
    # todo: short-circuit
    elif op == ast.BinOp.And:
      return (BaseType.Int, b2v(v2b(v1) and v2b(v2)))
    elif op == ast.BinOp.Or:
      return (BaseType.Int, b2v(v2b(v1) or v2b(v2)))
    elif op == ast.BinOp.Asgn:
      t, addr = yield from self.eval_lvalue(e1, ln)
      value = yield from self.eval_expr(e2, ln)
      v = cast(devoid(value), t)
      self.ctx.write(addr, v, ln)
      return (t, v)

    elif op == ast.BinOp.Idx:
      t, addr = yield from self.eval_lvalue(ast.Expr_Bin(op, (e1, e2)), ln)
      return (t, self.ctx.read(addr))
    
    raise NotImplementedError
  
  def unop(self, op: ast.UnOp, e: ast.Expr, ln: int) -> \
    Evaluation[TypedValue]:
    
    if op == ast.UnOp.Inc:
      t, addr = yield from self.eval_lvalue(e, ln)
      v = self.ctx.read(addr)
      self.ctx.write(addr, v + 1, ln)
      return (t, v)

    elif op == ast.UnOp.Dec:
      t, addr = yield from self.eval_lvalue(e, ln)
      v = self.ctx.read(addr)
      self.ctx.write(addr, v - 1, ln)
      return (t, v)

    elif op == ast.UnOp.Deref:
      t, addr = yield from self.eval_expr(e, ln)
      if isinstance(t, Type_Ptr):
        return (t.alias_t, self.ctx.read(addr))
      else:
        raise InterpreterError('You cannot derefer non-pointer value.')

    elif op == ast.UnOp.Ref:
      t, addr = yield from self.eval_lvalue(e, ln)
      if isinstance(t, BaseType):
        return (Type_Ptr(t), addr)
      else:
        raise InterpreterError('You cannot refer complex typed value.')
    
    raise NotImplementedError
