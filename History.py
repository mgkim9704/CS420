from LinkedList import *

class HistoryEntry:
  def __init__(self, codeLine, value):
    self.codeLine = codeLine
    self.value = value


class History:
  def __init__(self, name):
    self.name = name
    self.list = LinkedList()

  def add(self, n):
    self.list.insert_back(n)
  
  def printHistory(self):
    p = self.list.begin()
    while not self.list.is_end(p):
      print(self.name, "=", p.el.value, "at line", p.el.codeLine)
      p = p.next
