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


class Bool(Expr_Node):
  def __init__(self, value):
    self.value = value
    self.type = Type_bool()


# name of function or variable, ex) main, a
class Id(Expr_Node):
  def __init__(self, name, value):
    self.name = name
    self.value = value # value: Expr_Node


class Pointer(Expr_Node):
  def __init__(self, addr, baseType):
    self.addr = addr
    self.type = Type_pointer(baseType)


class String(Expr_Node):
  def __init__(self, strAddr):
    self.strAddr = strAddr
    self.type = Type_pointer(Type_char())


class ArrayElem(Expr_Node):
  def __init__(self, array, idx):
    self.array = array # array: Expr_Node
    self.idx = idx


class FUN(Expr_Node):
  def __init__(self, argsType, returnType):
    self.type = Type_fun(argsType, returnType)


class FUNCALL(Expr_Node):
  pass


class IF(Expr_Node):
  pass


class FOR(Expr_Node):
  pass


class WHILE(Expr_Node):
  pass


