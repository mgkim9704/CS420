# (line number, value)


# function name : dic
class History():
	def __init__(self):
		self.stack = []
		self.curr = {}

	def new_scope(self):
		self.stack.append(self.curr)
		self.curr = {}

	def comeback(self):
		self.curr = self.stack.pop()

	def mkRecord(self, lineno, name, value):
		rdic = self.curr
		if name in rdic:
			rdic[name].append((lineno, value))
		else:
			rdic[name] = [(lineno, value)]

	def itrace(self, curr_lineno, name):
		rdic = self.curr
		if not name in rdic:
			print("%s does not exist" % name)
			return
		rlist = rdic[name]
		for r in rlist:
			if r[0] <= curr_lineno:
				if type(r[1]) is int:
					print("%s = %d at line %d" % (name, r[1], r[0]))
				elif type(r[1]) is float:
					print("%s = %f at line %d" % (name, r[1], r[0]))
				else:
					print("%s = %s at line %d" % (name, r[1], r[0]))
			else: return

	def iprint(self, curr_lineno, name):
		rdic = self.curr
		if not name in rdic:
			print("%s does not exist" % name)
			return
		rlist = rdic[name]
		temp = 0
		for r in rlist:
			if r[0] > curr_lineno:
				break
			else: temp = r[1]
		print(temp)

