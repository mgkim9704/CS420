# this is doublylinked list

class EmptyListError(Exception):
  pass

class Node:
  def __init__(self, el, next=None, prev=None):
    self.el = el
    self.next = next
    self.prev = prev

  def __repr__(self):
    return "<" + repr(self.el) + ">"

class LinkedList:
  def __init__(self):
    self._front = Node(None)
    self._rear = Node(None, prev=self._front)
    self._front.next = self._rear
  
  def is_empty(self):
    return self._front.next == self._rear

  def is_end(self, n):
    if n == self._rear:
      return True
    return False

  def begin(self):
    if self.is_empty():
      raise EmptyListError
    return self._front.next

  def __repr__(self):
    res = "["
    p = self._front.next
    while p != self._rear:
      res += str(p.el)
      if p.next != self._rear:
        res += ", "
      p = p.next
    res += "]"
    return res

  def __len__(self):
    p = self._front.next
    count = 0
    while p != self._rear:
      count += 1
      p = p.next
    return count

  def insert_after(self, n, el):
    p = Node(el, n.next, n)
    n.next.prev = p
    n.next = p

  def insert_front(self, el):
    self.insert_after(self._front, el)
  
  def insert_back(self, el):
    self.insert_after(self._rear.prev, el)

  def remove(self, n):
    n.prev.next = n.next
    n.next.prev = n.prev

  def find_first(self, x):
    p = self._front.next
    while p != self._rear:
      if p.el == x:
        return p
      p = p.next
    return None

  def find_last(self, x):
    p = self._rear.prev
    while p != self._front:
      if p.el == x:
        return p
      p = p.prev
    return None

  def remove_all(self, x):
    p = self._front.next
    while p != self._rear:
      if p.el == x:
        p.prev.next = p.next
        p.next.prev = p.prev
      p = p.next
    return

  def __eq__(self, other):
    p = self._front.next
    q = other._front.next
    while p != self._rear and q != other._rear:
      if p.el != q.el:
        return False
      p = p.next
      q = q.next
    if p == self._rear and q == other._rear:
      return True
    return False
