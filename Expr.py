from LinkedList import *
from Type import *

class Expr_Node:
  pass


# ex) "5", "3.14"
class Num(Expr_Node):
  def __init__(self, value, type):
    self.value = value
    if type == "int":
      self.type = Type_int()
    elif type == "float":
      self.type = Type_float()


# ex) True, False
class Bool(Expr_Node):
  def __init__(self, value):
    self.value = value
    self.type = Type_bool()


class Pointer(Expr_Node):
  def __init__(self, baseType, value):
    self.type = Type_pointer(baseType)
    self.value = value


class String(Expr_Node):
  def __init__(self, string):
    self.str = string
    self.type = Type_pointer(Type_char())


# name of function or variable, ex) main, a
class Id(Expr_Node):
  def __init__(self, name, value):
    self.name = name
    self.value = value # : Expr_Node, Type: void, int, float, bool, char, pointer, fun, 


# ex) a[3]
class ArrayElem(Expr_Node):
  def __init__(self, array, idx):
    self.array = array # : Expr_Node, Type: pointer
    self.idx = idx # : Expr_Node


# function name: Id() ->(mapping) FunDef()
class FunDef(Expr_Node):
  def __init__(self, returnType, paramsType, funBody):
    self.funBody = funBody # : Expr_Node
    self.type = Type_fun(paramsType, returnType)


class FunCall(Expr_Node):
  def __init__(self, funDef, args):
    self.funDef = funDef # : Expr_Node, Type: fun
    self.args = args # : Expr_List, Type: Type_list


class IfStmt(Expr_Node):
  def __init__(self, cond, thenStmt, elseStmt):
    self.cond = cond # : Expr_Node, Type: bool
    self.thenStmt = thenStmt # : Expr_List
    self.elseStmt = elseStmt # : Expr_List


class ForLoop(Expr_Node):
  def __init__(self, init, cond, update):
    self.init = init # : Expr_List
    self.cond = cond # : Expr_Node, Type: bool
    self.update = update # : Expr_List


# ex) "int a"
class VarDeclaration(Expr_Node):
  def __init__(self, varType, names):
    self.varType = varType
    self.names = names


# ex) "a = 10;"
class VarAssignment(Expr_Node):
  def __init__(self, name, value):
    self.name = name
    self.value = value


class Printf(Expr_Node):
  def __init__(self, string, value=None):
    self.string = string # : Expr_Node, Type: pointer
    self.value = value # : Expr_Node, Type: int, float


# Calculation: +, -, *, /, ++
# comparison: >, <
class Operator(Expr_Node):
  def __init__(self, op, left=None, right=None):
    self.left = left # : Expr_Node
    self.op = op
    self.right = right # : Expr_Node

  def calculate(self):
    pass



# for parameter list, argument list, function body ...
class Expr_List:
  def __init__(self):
    self.list = LinkedList()

  def add(self, n):
    self.list.insert_back(n)



