# CS420: Compiler Design Term Project

20140223 박상욱, 20150122 김민경

## Abstraction

다음과 같은 mini-C 컴파일러를 개발했습니다.

- 언어: Python 3 을 사용했습니다. 조원 모두에게 익숙하고 관련 라이브러리가 많이 존재했습니다.
- 라이브러리: Parser에 [PLY](https://www.dabeaz.com/ply/)를 사용했습니다. 개발 도중에 [mypy][mypy] 를 이용하여 type error가 있는 지 확인했습니다.
- 역할 분담
  - 김민경: Lexer & Parser, tracking memories
  - 박상욱: Interpreter, testing, CLI
- 주요 기능
  - syntax error 를 검출하고 어느 line에서 발생했는 지 추적할 수 있음
  - [C--](https://www2.cs.arizona.edu/~debray/Teaching/CSc453/DOCS/cminusminusspec.html)의 대부분의 기능 구현
  - statement 별로 실행하면서 변수의 값을 출력할 수 있음
  - 변수의 값 변화 기록을 출력할 수 있음
  - Recursive function call 가능 (optional feature)

## Implementation

### Common

Python class로 AST node들을 구현했습니다. Python은 쉽고 단순한 언어이지만 static typing을 지원하지 않습니다. 그러나 python 3.5 이후부터 [type hint](https://www.python.org/dev/peps/pep-0484/) 나 [mypy][mypy] 를 통해 제한적으로 type safety를 검사할 수 있습니다. AST 또한 typing 모듈에 있는 `Union, NamedTuple, Optional` 등을 사용하여 선언하였습니다.

AST는 크게 세 종류의 노드로 나누어지며, 첫째는 expression, 둘째는 statement, 셋째는 function입니다. Expression은 값을 가질 수 있는 표현식입니다. `3 + 4`, `a[4] + foo(7)` 등이 해당됩니다. Statement 는 semicolon으로 구분되는 실행의 기본 단위입니다. 여기에는 `for` , `if`구문이 포함됩니다. Statement 중 `Stmt_Comp` 는 여러 개의 Statement를 중괄호로 묶은 코드를 나타내는 재귀적인 노드입니다. Function 은 함수의 그 인자의 이름, 인자와 리턴 값의 타입, 그리고 내부 statements로 이루어집니다. 프로그램은 function의 집합입니다.[^1]

### Lexer & Parser

`Lexer.py`, `Parser.py`, `parserSupport.py`

_PLY_ 는 David Beazley 가 개발한 lex & yacc의 python 구현체입니다. PLY는 설정한 regular expression 정의를 바탕으로 input string을 받아 토큰화 작업을 수행해줍니다. 또한 입력한 BNF rule을 기반으로 `LALR(1)` 파서를 생성합니다. 처음에는 c 문법을 기초로 lexer와 parser의 rule을 작성하였으나 이후 저희 프로젝트의 scope에 맞추기 위해 일부분을 기각하는 방식으로 수정하였습니다. 코드 상에 '<-remove'로 표시된 부분 또는 NotImplementedError를 일으킨 부분이 이에 해당하며 아예 지워진 부분도 존재합니다.  

각 production rule 은 앞에서 정의된 AST를 생성하도록 만들어졌습니다. 또한 모든 statement 는 토큰에 저장된 line number를 통해 자신의 위치 (줄 번호)를 저장하도록 되어 있습니다. 처음부터 scope에 맞추지 않고 기각하는 방식을 사용하였기 때문에 불필요하게 토큰만을 전달하는 중간 단계들이 존재합니다. parserSupport에 rule에 따른 결과 값을 전달하는 과정을 효율적으로 도울 class를 정의하여 사용하였습니다. 만약 파싱 도중 문법 오류가 발생하였을 경우 발생한 위치를 알려주고 실행을 종료합니다.  

### Interpreter

`interpreter/core.py`

Interpreter는, term presentation에서 말씀드렸던 대로, 일련의 type check나 IR로 변환을 거치지 않고 AST를 바로 실행합니다. 이는 분명 비효율적이지만 단순하고 빠르게 개발할 수 있습니다. 따라서 AST 자체로 Control flow graph가 되며, Symbol table은 실행하는 도중에 변수가 추가/삭제됩니다.

Interpreter는 처음에 재귀적으로 작성되었으나 나중에 statement 별 실행을 지원하기 위해서 Generator를 도입했습니다. 모든 `eval_*` 메서드는 실행하고 나서 얻은 값이 아니라 일련의 실행 결과를 반환하는 일종의 Iterator를 리턴합니다. 각각의 결과는 statement가 한 번 실행될 때마다 얻을 수 있습니다. 이를 테면 사용자는 프로그램이 종료할 때까지 기다리기 위해서 다음과 같이 작성할 수 있습니다.

```python
evaluation = interp.eval_func('main', [], 0)
for ctx in evaluation:
    pass
```

여기서 evaluation이 `yield` 하는 값 `ctx` 는 인터프리터의 중간 상태를 나타내는 `Context` 입니다. 사용자는 `Context` 에 접근하여 어느 변수가 선언되었고, 그 타입과 값은 무엇인지 알아낼 수 있습니다.

`eval_expr` 이나 `eval_lvalue`, `binop` 등은 이름에 맞게 해당하는 계산 결과 혹은 lvalue가 가리키는 주소를 리턴합니다. `eval_stmt` 가 리턴하는 값은 _CFD_(Control Flow Directive)로, 인터프리터가 이 statement가 실행하고 나서의 행동을 결정합니다. `CFD.Go` (다음 statement 실행) 이 아닌 경우 이 값은 `eval_block`에서 투명하게 밖으로 전달되며  `eval_func` 혹은 `for`, `if` 문을 실행 중인 `eval_stmt`가 받아 처리합니다. (예외가 call stack을 거슬러 올라가 밖으로 전달되는 것과 유사합니다.)

#### Type and Environment 

변수가 가질 수 있는 타입에는 `int`, `float`, `int *`, `float *`. `int []`, `float []` 이 있으나, 그 중 배열은 1st-class citizen 이 될 수 없습니다. 배열을 나타내는 변수는 계산될 때 자동으로 그 원소를 가리키는 포인터 형으로 변환됩니다. 따라서 모든 연산 결과는 `int`, `float`, `int *`, `float *` 타입 중 하나입니다. 명시적인 타입 캐스팅 (예: `(int)3.7`)은 지원하지 않습니다. 그러나 mini-C 프로그래머는 다음과 같이 어떤 값이든 원하는 타입으로 값을 캐스팅할 수 있습니다. (초기화는 생략)

```c
int i, *pi;
float f, *pf;
i = f; /* Valid */
f = i; /* Valid */
*pi = f; /* Valid */
*pf = i; /* Valid */
i = pf; /* Valid */
f = pi; /* Valid */
pi = &i; /* Valid */
```

단, 다음은 경고를 출력합니다.

```c
pi = i; /* Warning: converting an integer into a pointer may be harmful. */
pi = pf; /* Warning: converting a pointer to different object type causes */
		 /* undefined behavior. */
```

그리고 float을 바로 포인터로 바꿀 수는 없습니다.

```c
pi = f; /* Cannot convert any float into a pointer. */
i = f; pi = i; /* But this is ok. (Not recommended) */
```

#### Context

`interpreter/context.py`

Context는 프로그램을 실행하는 동안 인터프리터가 가지고 있는 중간 상태를 나타냅니다. Context는 크게 두 개의 정보를 가지고 있는데, 하나는 `environment` 로 현재 block에서 접근할 수 있는 변수들의 이름과 타입을 저장하고 있습니다. 나머지 하나는 `memory` 으로, 변수의 값을 저장하는 가상의 스택입니다. `memory` 는 아래에 있는 `trace` 명령어를 구현하기 위해 값 변화를 모두 기록하고 있는 `Record`를 원소로 가집니다. `Record` 에는 해당 주소의 값이 수정된 statement의 줄 번호와 그 값이 리스트로 저장되어 있습니다. 이 둘은 근본적으로 변수들의 symbol table을 나타내고 있습니다.

#### Shadowing variables

중괄호로 둘러 싼 statement block에는 두 가지 종류가 있는 데, 하나는 function의 body로 사용된 것이고 다른 하나는 그를 제외한 나머지입니다. 첫 번째 블럭은 실행될 때 context의 environment를 비우고 그 안에 함수의 인자를 채워 넣습니다. 다른 블럭은, _environment fragment_를 environment에 추가합니다. 동일한 이름을 가지고 있는 변수는 같은 environment fragment에서는 정의될 수 없지만, 다른 environment fragment라면 나중에 정의된 쪽이 이전에 정의된 변수를 가립니다. 가려진 변수는 해당 블럭을 빠져나오기 전까지 접근할 수 없습니다. 이를 위해 environment 는 environment fragment의 리스트로 정의되었으며, environment fragment는 문자열에서 (타입, 스택 주소) 튜플로 가는 딕셔너리 (hashed map) 으로 정의했습니다.

### CLI

다음과 같이 실행할 수 있습니다: `python3 main.py <filename>`

요구 사항에 있었던 대로, `next`, `print`, `trace` 명령어를 구현했습니다. 

- `next n`: n개 (생략되면 하나)의 statement를 실행합니다. 이때 주의할 것은, 하나의 라인이 아니라 하나의 statement를 실행한다는 것입니다. 제시된 예제와 같이 한 줄에 하나의 문장이 있는 경우에는 동일한 동작을 합니다. for 문과 if 문은 한번에 실행되지 않고 그 내부로 들어가 더 이상 나눌 수 없는 statement 하나를 실행합니다.
- `print v`: 변수 `v` 의 값을 출력합니다. `v` 가 배열이면 배열 전체가 출력되며, 포인터라면 포인터가 가리키는 값도 출력됩니다.
- `trace v`: 변수 `v` 의 변경 이력을 출력합니다. 어느 라인에서 선언되었는 지 (값이 N/A로 나타나짐), 어느 라인에서 변경되었는지 알 수 있습니다.

추가로 `verbose` 명령어를 입력하면 디버깅에 도움이 되도록, 매 `next` 마다 실행하기 직전의 statement와 현재 context 에 있는 변수들을 모두 보여줍니다.

`main` 함수가 리턴하면 그 리턴값을 보여줍니다. 프로그램의 실행이 완료되어도 `main` 함수 내의, 리턴 직전의 context는 계속 확인할 수 있습니다.

## Test

`tests/` 폴더 안에는 직접 테스트한 몇 개의 테스트 케이스가 있습니다. `python3 test.py <testcase-name>` 을 통해 확인해 볼 수 있습니다. 단 `error`로 끝나는 것은 실행 시 오류가 나는 것을 의도한 테스트 케이스입니다.

[^1]: 여기서는 전역 변수를 지원하지 않습니다.

[mypy]: (http://mypy-lang.org/)
