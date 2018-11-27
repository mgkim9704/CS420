import LinkedList

class Expr_Node:
  pass
"""  def is_null(self):
    return False

  def is_number(self):
    return False"""


# NULL
class Null(Expr_Node):
  def __init__(self):
    self.type = Type_null()

"""  def is_null(self):
    return True"""


# ex) "5", "3.14"
class Num(Expr_Node):
  def __init__(self, value, type):
    self.value = value
    if type == "int":
      self.type = Type_int()
    elif type == "float":
      self.type = Type_float()

"""  def is_number(self):
    return True"""


# ex) True, False
class Bool(Expr_Node):
  def __init__(self, value):
    self.value = value
    self.type = Type_bool()


# name of function or variable, ex) main, a
class Id(Expr_Node):
  def __init__(self, name, value):
    self.name = name
    self.value = value # : Expr_Node


class Pointer(Expr_Node):
  def __init__(self, addr, baseType):
    self.addr = addr
    self.type = Type_pointer(baseType)


class String(Expr_Node):
  def __init__(self, string):
    self.str = string
    self.type = Type_pointer(Type_char())


# ex) a[3]
class ArrayElem(Expr_Node):
  def __init__(self, array, idx):
    self.array = array # : Expr_Node (Pointer)
    self.idx = idx


# function name: Id() ->(mapping) FunDef()
class FunDef(Expr_Node):
  def __init__(self, returnType, paramsType, funBody):
    self.funBody = funBody # : Expr_Node
    self.type = Type_fundef(paramsType, returnType)


class FunCall(Expr_Node):
  def __init__(self, funDef, args):
    self.funDef = funDef # : Expr_Node
    self.args = args


class Return(Expr_Node):
  def __init__(self, rtn):
    self.rtn = rtn


# need to include "cond? true : false"
class IfStmt(Expr_Node):
  def __init__(self, cond, thenStmt, elseStmt):
    self.cond = cond # : Expr_Node
    self.thenStmt = thenStmt # : Expr_Node
    self.elseStmt = elseStmt # : Expr_Node


class BreakStmt(Expr_Node):
  pass

class ContinueStmt(Expr_Node):
  pass

class ForLoop(Expr_Node):
  def __init__(self, init, cond, update):
    self.init = init # : Expr_Node
    self.cond = cond # : Expr_Node
    self.update = update # : Expr_Node


class WhileLoop(Expr_Node):
  def __init__(self, cond, stmt):
    self.cond = cond # : Expr_Node
    self.stmt = stmt # : Expr_Node


class DoWhileLoop(Expr_Node):
  def __init__(self, stmt, cond):
    self.stmt = stmt # : Expr_Node
    self.cond = cond # : Expr_Node


# ex) "int a;" "int max(int, int)"
class Declaration(Expr_Node):
  pass

# ex) "a = 10;"
class Initialization(Expr_Node):
  pass

"""
ArithmeticOperator: +, -, *, /, %, ++, --
RelationalOperator: ==, !=, >, <, <=, >=
LogicalOperator: &&, ||, !
BitwiseOperator: &, |, ^, ~, <<, >>
AssignmentOperator: =, +=, -=, /=, %=, <<=, >>=, &=, ^=, |=
MiscOperator: sizeof(), &a, *a
"""
class Operator(Expr_Node):
  def __init__(self, left, op, right):
    self.left = left
    self.op = op
    self.right = right

  def calculate(self):
    pass



# for parameter list, argument list, function body ...
class Expr_List(Expr_Node):
  def __init__(self):
    self.list = LinkedList()

  def add(self, n):
    self.list.insert_back(n)



