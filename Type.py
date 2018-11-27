class TYPE():
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

class Type_null(TYPE):
  def is_int(self):
    return True

class Type_int(TYPE):
  def is_int(self):
    return True

class Type_float(TYPE):
  def is_float(self):
    return True

class Type_bool(TYPE):
  def is_bool(self):
    return True

class Type_char(TYPE):
  def is_char(self):
    return True

class Type_pointer(TYPE):
  def __init__(self, baseType):
    self.baseType = baseType # baseType: TYPE, ex) baseType of "int*" is Type_int
  def is_pointer(self):
    return True

class Type_fun(TYPE):
  def __init__(self, argsType, returnType):
    self.argsType = argsType
    self.returnType = returnType
  def is_fun(self):
    return True

