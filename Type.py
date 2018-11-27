class TYPE():
  def __init__(self):
    self.type = 0
  def is_null(self):
    return False
  def is_int(self):
    return False
  def is_float(self):
    return False
  def is_bool(self):
    return False
  def is_char(self):
    return False
  def is_pointer(self):
    return False
  def is_fun(self):
    return False

  def __eq__(self, other):
    if self.type == other.type:
      return True
    return False


class Type_null(TYPE):
  def __init__(self):
    self.type = 0

  def is_null(self):
    return True


class Type_int(TYPE):
  def __init__(self):
    self.type = 1

  def is_int(self):
    return True


class Type_float(TYPE):
  def __init__(self):
    self.type = 2

  def is_float(self):
    return True


class Type_bool(TYPE):
  def __init__(self):
    self.type = 3

  def is_bool(self):
    return True


class Type_char(TYPE):
  def __init__(self):
    self.type = 4

  def is_char(self):
    return True


class Type_pointer(TYPE):
  def __init__(self, baseType):
    self.type = 5
    self.baseType = baseType # baseType: TYPE, ex) baseType of "int*" is Type_int

  def is_pointer(self):
    return True

  def __eq__(self, other):
    if self.type == other.type && self.baseType == other.baseType:
      return True
    return False


class Type_fundef(TYPE):
  def __init__(self, paramsType, returnType):
    self.type = 6
    self.paramsType = paramsType
    self.returnType = returnType

  def is_fun(self):
    return True

  def __eq__(self, other):
    if self.type == other.type && self.paramsType == other.paramsType && self.returnType == other.returnType:
      return True
    return False

class Type_list(TYPE):
  def __init__(self):
    self.type = 7
    self.list = LinkedList()

  def add(self, n):
    self.list.insert_back(n)

  def __eq__(self, other):
    if self.type == self.other && self.list == other.list:
      return True
    return False
