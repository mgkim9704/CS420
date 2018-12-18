import Parser
import sys, importlib
from interpreter.core import Interpreter


if __name__ == '__main__':
  testname = sys.argv[1]
  test = importlib.import_module(f'tests.{testname}')
    
  with open(f'tests/{testname}.c', 'r') as f:
    code = f.read()

  program = Parser.parse(code)
  interp = Interpreter(program)
  try:
    res = interp.run()
  except Exception as e:
    print(f'[FAIL] {testname}')
    print(e)
  else:
    if (res != test.res):
      print(f'[FAIL] {testname}')
    else:
      print(f'[PASS] {testname}')