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

def dump_var(name):
  try:
    t, addr = ctx.where(name)
  except interpreter.core.InterpreterError as e:
    print(e.message)
  else:
    if isinstance(t, interpreter.core.Type_Array):
      print(f'An array from {addr}, size={t.size}')
    else:
      try:
        v = ctx.read(addr)
      except interpreter.core.InterpreterError as e:
        print('N/A')
      else:
        if isinstance(t, interpreter.core.Type_Ptr):
          print(f'Pointer to address {v}')
        else:
          print(str(v))

def proceed(num: int):
  global ctx
  try:
    for _ in range(num):
      ctx = next(evaluation)
  except StopIteration as e:
    print('Evaluation finished with ' + str(e.value))
    exit(0)

ctx = next(evaluation)

while True:
  i=input(">> ")
  iList = i.split()
  iListNum = len(iList)

  if iListNum==1 and iList[0] == "next":
    proceed(1)

  elif iListNum==1 and iList[0] == "exit":
    exit(0)

  elif iListNum==2 and iList[0] == "next":
    lineno = iList[1]
    
    
  elif iListNum==2 and iList[0] == "print":
    varname = iList[1]
    dump_var(varname)
    
  elif iListNum==2 and iList[0] == "trace":
    history.itrace(lineno, iList[1])
    print("trace", iList[1])
  elif iListNum==1 and iList[0] == "verbose":
    interp.verbose = not interp.verbose
    print("Verbose mode is switched.")
  elif iListNum==0 and interp.verbose: # no input => regard as continue
    break
  else:
    print("Error: invalid command!")

