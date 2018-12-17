import sys
import Parser
import interpreter.core
from interpreter.trace import *

# Arguments
if len(sys.argv) == 1:
  print('No input files')
  print('Usage: ' + sys.argv[0] + ' <filename> [function] [arguments]')
  exit(-1)

filename = sys.argv[1]

if len(sys.argv) == 2:
  funcname = 'main'
  args = []
else:
  funcname = sys.argv[2]
  args = map(lambda x: int(x), sys.argv[3:])

# read file
filename = sys.argv[1]
with open(filename, 'r') as f:
  code = f.read()

history = History()
program = Parser.parse(code)
interp = interpreter.core.Interpreter(program)
evaluation = interp.eval_func(funcname, args)
lineno = 0

while True:
  try:
    ctx = next(evaluation)
    print (ctx)
  except StopIteration as e:
    print('Evaluation finished with ' + str(e.value))
    break

  i=input(">> ")
  iList = i.split()
  iListNum = len(iList)

  if iListNum==1 and iList[0] == "next":
    lineno = lineno +1
    print("next")
    continue
  elif iListNum==1 and iList[0] == "exit":
    break
  elif iListNum==2 and iList[0] == "next":
    lineno = iList[1]
    print("next", iList[1])
  elif iListNum==2 and iList[0] == "print":
    history.iprint(lineno, iList[1])
    print("print", iList[1])
  elif iListNum==2 and iList[0] == "trace":
    history.itrace(lineno, iList[1])
    print("trace", iList[1])
  else:
    print("Error: invalid command!")

