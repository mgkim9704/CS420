# ----------------------------------------------------------------------
# Lexer.py
# ----------------------------------------------------------------------

import re
import lex


# Reserved words

reserved = (
	'CHAR', 'ELSE', 'EXTERN', 'FLOAT', 'FOR', 'IF', 'INT', 'RETURN', 'STATIC' 'VOID', 'WHILE',
)

tokens = reserved + (
	# Literals (identifier, integer constant, float constant, string constant, char const)
	'ID', 'TYPEID', 'INUM', 'FNUM', 'STRING', 'CHARACTER',

	# Operators (+,-,*,/,% |, &, ~, ^, <<, >>, ||, &&, !, <, <=, >, >=, ==, !=)
	'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',
	'OR', 'AND', 'NOT', 'XOR', 'LSHIFT', 'RSHIFT',
	'LOR', 'LAND', 'LNOT',
	'LT', 'LE', 'GT', 'GE', 'EQ', 'NE',

	# Assignment (=)
	'EQUALS', 

	# Increment/decrement (++,--)
	'INCREMENT', 'DECREMENT',

	# Delimeters ( ) [ ] { } , . ; :
	'LPAREN', 'RPAREN',
	'LBRACKET', 'RBRACKET',
	'LBRACE', 'RBRACE',
	'COMMA', 'PERIOD', 'SEMI', 'COLON',
)

reserved_map = {}
for r in reserved:
	reserved_map[r.lower()] = r

#-------------------------------------------------------------------------------

# New lines
def t_NEWLINE(t):
	r'\n+'
	t.lexer.lineno += t.value.count("\n")

# Operators
t_PLUS             = r'\+'
t_MINUS            = r'-'
t_TIMES            = r'\*'
t_DIVIDE           = r'/'
t_AND              = r'&'
t_LOR              = r'\|\|'
t_LAND             = r'&&'
t_LNOT             = r'!'
t_LT               = r'<'
t_GT               = r'>'
t_LE               = r'<='
t_GE               = r'>='
t_EQ               = r'=='
t_NE               = r'!='

# Assignment operators
t_EQUALS           = r'='

# Increment/decrement
t_INCREMENT        = r'\+\+'
t_DECREMENT        = r'--'

# Delimeters
t_LPAREN           = r'\('
t_RPAREN           = r'\)'
t_LBRACKET         = r'\['
t_RBRACKET         = r'\]'
t_LBRACE           = r'\{'
t_RBRACE           = r'\}'
t_COMMA            = r','
t_PERIOD           = r'\.'
t_SEMI             = r';'
t_COLON            = r':'

# Identifiers
def t_ID(t):
	r'[A-Za-z_][\w_]*'
	t.type = reserved_map.get(t.value, "ID")
	return t

# Integer literal
t_INUM = r'\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'

# Floating literal
t_FNUM = r'((\d+)(\.\d+)(e(\+|-)?(\d+))? | (\d+)e(\+|-)?(\d+))([lL]|[fF])?'

# String literal
t_STRING = r'\"([^\\\n]|(\\.))*?\"'

# Character constant 'c' or L'c'
t_CHARACTER = r'(L)?\'([^\\\n]|(\\.))*?\''

# Comment (C-Style)
def t_COMMENT(t):
	r'/\*(.|\n)*?\*/'
	t.lexer.lineno += t.value.count('\n')
	pass

# Comment (C++-Style)
def t_CPPCOMMENT(t):
	r'//.*\n'
	t.lexer.lineno += 1
	pass

# whitespace
def t_WHITESPACE(t):
	r'[ \t]+'
	pass

# Error
def t_error(t):
	print("Line %d: Illegal character %s" % (t.lineno, t.value[0]))
	t.lexer.skip(1)

lexer = lex.lex()

if __name__ == '__main__':
	import sys
	f = open(sys.argv[1])
	lines = f.readlines()
	code = ""
	for l in lines:
		code += l
	lexer.input(code)
	while 1:
		token = lexer.token()
		if not token: break
		print("<%s, %s, %d>" % (token.type, token.value, token.lineno))
