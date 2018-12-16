import sys
import interpreter.core


# read file
#filename = sys.argv[1]
#f=open(filename, 'r')
#lines = f.readlines()
#for l in lines:

engine = interpreter.core.loadTest()
evaluation = engine.eval_func('fact', [4])

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
    print("next")
    continue
  elif iListNum==1 and iList[0] == "exit":
    break
  elif iListNum==2 and iList[0] == "next":
    print("next", iList[1])
  elif iListNum==2 and iList[0] == "print":
    print("print", iList[1])
  elif iListNum==2 and iList[0] == "trace":
    print("trace", iList[1])
  else:
    print("Error: invalid command!")

