# ----------------------------------------------------------------------
# Parser.py
# ----------------------------------------------------------------------

import sys, codecs
import yacc
import Lexer
from interpreter.ast import *
from parserSupport import *

# Get the token map
tokens = Lexer.tokens


# ---------------------------------------------------------------
# translation-unit:
#	external-declaration
#	translation-unit external-declaration
# ---------------------------------------------------------------
def p_translation_unit_1(t):
	'translation_unit : external_declaration'
	t[0] = [t[1]]

def p_translation_unit_2(t):
	'translation_unit : translation_unit external_declaration'
	t[1].append(t[2])
	t[0] = t[1]


# ---------------------------------------------------------------
# external-declaration:
#	function-definition
#	declaration
# ---------------------------------------------------------------
def p_external_declaration_1(t):
	'external_declaration : function_definition'
	t[0] = t[1]

def p_external_declaration_2(t):
	'external_declaration : declaration'
	raise NotImplementedError


# ---------------------------------------------------------------
# function-definition:
#	declaration-specifiers declarator declaration-listopt compound-statement
# ---------------------------------------------------------------
def p_function_definition(t):
	'function_definition : declaration_specifiers declarator declaration_listopt compound_statement'
	if t[3] is not None: raise NotImplementedError
	t[0] = Func(t[2][1], t[2][2], t[1], t[2][0], t[4])


# ---------------------------------------------------------------
# declaration:
#	declaration-specifiers init-declarator-listopt ;
# ---------------------------------------------------------------
def p_declaration(t):
	'declaration : declaration_specifiers init_declarator_listopt SEMI'
	t[0] = (t.lineno(1), Stmt_Decl(t[1], t[2].list))


# ---------------------------------------------------------------
# declaration-listopt:
#	declaration-list		<- remove
#	empty
# ---------------------------------------------------------------
def p_declaration_listopt_1(t):
	'declaration_listopt : declaration_list'
	raise NotImplementedError


def p_declarationopt_list_2(t):
	'declaration_listopt : empty'
	pass


# ---------------------------------------------------------------
# declaration-list:			<- remove
#	declaration
#	declaration-list declaration
# ---------------------------------------------------------------
def p_declaration_list_1(t):
	'declaration_list : declaration'
	raise NotImplementedError

def p_declaration_list_2(t):
	'declaration_list : declaration_list declaration'
	raise NotImplementedError


# ---------------------------------------------------------------
# declaration-specifiersopt:
#	declaration-specifiers
#	empty
# ---------------------------------------------------------------
def p_declaration_specifiersopt_1(t):
	'declaration_specifiersopt : declaration_specifiers'
	raise NotImplementedError

def p_declaration_specifiersopt_2(t):
	'declaration_specifiersopt : empty'
	pass


# ---------------------------------------------------------------
# declaration-specifiers:
#	storage-class-specifier declaration-specifiersopt
#	type-specifier declaration-specifiersopt
#	type-qualifier declaration-specifiersopt				<- remove
#	function-specifier declaration-specifiersopt				<- remove
# ---------------------------------------------------------------
def p_declaration_specifiers_1(t):
	'declaration_specifiers : storage_class_specifier declaration_specifiersopt'
	raise NotImplementedError

def p_declaration_specifiers_2(t):
	'declaration_specifiers : type_specifier declaration_specifiersopt'
	t[0] = t[1]


# ---------------------------------------------------------------
# storage-class-specifier:	
#	typedef					<- remove
#	extern
#	static
#	auto					<- remove
#	register				<- remove
# ---------------------------------------------------------------
def p_storage_class_specifier(t):
	'''storage_class_specifier : EXTERN 
                               | STATIC
                               '''
	raise NotImplementedError


# ---------------------------------------------------------------
# type-specifier:
#	void
#	char
#	int
#	float
# ---------------------------------------------------------------
def p_type_specifier_1(t):
	'type_specifier : VOID'
	t[0] = None

def p_type_specifier_2(t):
	'type_specifier : CHAR'
	t[0] = Type.Char

def p_type_specifier_3(t):
	'type_specifier : INT'
	t[0] = Type.Int

def p_type_specifier_4(t):
	'type_specifier : FLOAT'
	t[0] = Type.Float


# ---------------------------------------------------------------
# init-declarator-listopt:
#	init-declarator-list
#	empty
# ---------------------------------------------------------------
def p_init_declarator_listopt_1(t):
	'init_declarator_listopt : init_declarator_list'
	t[0] = t[1]

def p_init_declarator_listopt_2(t):
	'init_declarator_listopt : empty'
	raise NotImplementedError


# ---------------------------------------------------------------
# init-declarator-list:
#	init-declarator
#	init-declarator-list , init-declarator
# ---------------------------------------------------------------
def p_init_declarator_list_1(t):
	'init_declarator_list : init_declarator'
	temp = myList()
	temp.add(t[1])
	t[0] = temp
	

def p_init_declarator_list_2(t):
	'init_declarator_list : init_declarator_list COMMA init_declarator'
	t[1].add(t[3])
	t[0] = t[1]


# ---------------------------------------------------------------
# init-declarator:
#	declarator
#	declarator = initializer
# ---------------------------------------------------------------
def p_init_declarator_1(t):
	'init_declarator : declarator'
	t[0] = t[1]

def p_init_declarator_2(t):
	'init_declarator : declarator EQUALS initializer'
	raise NotImplementedError


# ---------------------------------------------------------------
# specifier-qualifier-listopt:
#	specifier-qualifier-list
#	empty
# ---------------------------------------------------------------
def p_specifier_qualifier_listopt_1(t):
	'specifier_qualifier_listopt : specifier_qualifier_list'
	raise NotImplementedError

def p_specifier_qualifier_listopt_2(t):
	'specifier_qualifier_listopt : empty'
	raise NotImplementedError


# ---------------------------------------------------------------
# specifier-qualifier-list:
#	type-specifier specifier-qualifier-listopt
#	type-qualifier specifier-qualifier-listopt		<- remove
# ---------------------------------------------------------------
def p_specifier_qualifier_list(t):
	'specifier_qualifier_list : type_specifier specifier_qualifier_listopt'
	raise NotImplementedError


# ---------------------------------------------------------------
# declarator:
#	pointeropt direct-declarator
# ---------------------------------------------------------------
def p_declarator(t):
	'declarator : pointeropt direct_declarator'
	if t[2] is None: raise NotImplementedError

	if t[2].type == 1:
		t[0] = DecoratedName(t[2].value[0], t[1])
	elif t[2].type == 6:
		t[0] = (t[1], t[2].value[0], t[2].value[1])
	elif t[2].type == 3:
		t[0] = DecoratedName(t[2].value[0], t[2].value[1].val)
	else: raise NotImplementedError
				


# ---------------------------------------------------------------
# direct-declarator:				<- type-qualifier-list remove
#	identifier
#	( declarator )
#	direct-declarator [ type-qualifier-listopt assignment-expressionopt ]
#	direct-declarator [ static type-qualifier-listopt assignment-expression ]
#	direct-declarator [ type-qualifier-list static assignment-expression ]		
#	direct-declarator [ type-qualifier-listopt * ]
#	direct-declarator ( parameter-type-list )
#	direct-declarator ( identifier-listopt )
# ---------------------------------------------------------------
def p_direct_declarator_1(t):
	'direct_declarator : ID'
	temp = directDeclarator(1)
	temp.add(t[1])
	t[0] = temp

def p_direct_declarator_2(t):
	'direct_declarator : LPAREN declarator RPAREN'
	raise NotImplementedError

def p_direct_declarator_3(t):
	'direct_declarator : direct_declarator LBRACKET assignment_expressionopt RBRACKET'
	temp = directDeclarator(3)
	temp.add(t[1].value[0])
	temp.add(t[3])
	t[0] = temp

def p_direct_declarator_4(t):
	'direct_declarator : direct_declarator LBRACKET STATIC assignment_expression RBRACKET'
	raise NotImplementedError

def p_direct_declarator_5(t):
	'direct_declarator : direct_declarator LBRACKET TIMES RBRACKET'
	raise NotImplementedError

def p_direct_declarator_6(t):
	'direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'
	if(t[1] is not None and t[1].type == 1):
		temp = directDeclarator(6)
		temp.add(t[1].value[0])
		if t[3] is not None:
			temp.add(t[3].list)
		else: temp.add([])
		t[0] = temp
	else: raise NotImplementedError

def p_direct_declarator_7(t):
	'direct_declarator : direct_declarator LPAREN identifier_listopt RPAREN'
	if(t[1] is not None and t[1].type == 1):
		t[0] = Expr_Call(t[1], t[3].list)
	else: raise NotImplementedError
	pass

# ---------------------------------------------------------------
# pointeropt:
#	pointer 
#	empty
# ---------------------------------------------------------------
def p_pointeropt_1(t):
	'pointeropt : pointer'
	t[0] = True

def p_pointeropt_2(t):
	'pointeropt : empty'
	t[0] = False


# ---------------------------------------------------------------
# pointer:
#	* 
#	* pointer
# ---------------------------------------------------------------
def p_pointer_1(t):
	'pointer : TIMES'
	pass

def p_pointer_2(t):
	'pointer : TIMES pointer'
	raise NotImplementedError
	pass


# ---------------------------------------------------------------
# parameter-list:
#	parameter-declaration
#	parameter-list , parameter-declaration
# ---------------------------------------------------------------
def p_parameter_list_1(t):
	'parameter_list : parameter_declaration'
	if t[1] is not None:
		temp = myList()
		temp.add(t[1])
		t[0] = temp

def p_parameter_list_2(t):
	'parameter_list : parameter_list COMMA parameter_declaration'
	if t[3] is not None:
		t[1].add(t[3])
		t[0] = t[1]


# ---------------------------------------------------------------
# parameter-declaration:
#	declaration-specifiers declarator
#	declaration-specifiers abstract-declarator(opt <- remove)
# ---------------------------------------------------------------
def p_parameter_declaration_1(t):
	'parameter_declaration : declaration_specifiers declarator'
	t[0] = (t[1], t[2])

def p_parameter_declaration_2(t):
	'parameter_declaration : declaration_specifiers'
	if t[1] is not None:
		t[0] = (t[1], None)


# ---------------------------------------------------------------
# identifier-listopt:
#	identifier-list
#	empty
# ---------------------------------------------------------------
def p_identifier_listopt_1(t):
	'identifier_listopt : identifier_list'
	t[0] = t[1]

def p_identifier_listopt_2(t):
	'identifier_listopt : empty'
	t[0] = myList()


# ---------------------------------------------------------------
# identifier-list:
#	identifier
#	identifier-list , identifier
# ---------------------------------------------------------------
def p_identifier_list_1(t):
	'identifier_list : ID'
	temp = myList()
	temp.add(t[1])
	t[0] = temp

def p_identifier_list_2(t):
	'identifier_list : identifier_list COMMA ID'
	t[1].add(t[3])
	t[0] = t[1]


# ---------------------------------------------------------------
# initializer:
#	assignment-expression
#	{ initializer-list }
#	{ initializer-list , }
# ---------------------------------------------------------------
def p_initializer_1(t):
	'initializer : assignment_expression'
	raise NotImplementedError

def p_initializer_2(t):
	'''initializer : LBRACE initializer_list RBRACE
                       | LBRACE initializer_list COMMA RBRACE'''
	raise NotImplementedError


# ---------------------------------------------------------------
# initializer-list:
#	initializer
#	initializer_list , initializer
# ---------------------------------------------------------------
def p_initializer_list_1(t):
	'initializer_list : initializer'
	raise NotImplementedError

def p_initializer_list_2(t):
	'initializer_list : initializer_list COMMA initializer'
	raise NotImplementedError


# ---------------------------------------------------------------
# type-name:		
#	specifier-qualifier-list abstract-declarator(opt <- remove)
# ---------------------------------------------------------------
def p_type_name(t):
	'type_name : specifier_qualifier_list'
	raise NotImplementedError


# ---------------------------------------------------------------
# parameter-type-list:
#	parameter-list
#	parameter-list , ...		<- remove
# ---------------------------------------------------------------
def p_parameter_type_list(t):
	'parameter_type_list : parameter_list'
	if t[1] is not None:
		t[0]=t[1]


# ---------------------------------------------------------------
# statement:
#	selection-statement
#	iteration-statement
#	jump_statement
#	compound-statement
#	expression-statement
# ---------------------------------------------------------------
def p_statement_1(t):
	'statement : selection_statement'
	t[0] = t[1]

def p_statement_2(t):
	'statement : iteration_statement'
	t[0] = t[1]

def p_statement_3(t):
	'statement : jump_statement'
	t[0] = t[1]

def p_statement_4(t):
	'statement : compound_statement'
	t[0] = t[1]

def p_statement_5(t):
	'statement : expression_statement'
	t[0] = t[1]


# ---------------------------------------------------------------
# selection-statement:
#	if ( expression ) statement
#	if ( expression ) statement else statement
# ---------------------------------------------------------------
def p_selection_statement_1(t):
	'selection_statement : IF LPAREN expression RPAREN statement'
	t[0] = (t.lineno(1), Stmt_If(t[3], t[5]))

def p_selection_statement_2(t):
	'selection_statement : IF LPAREN expression RPAREN statement ELSE statement'
	raise NotImplementedError


# ---------------------------------------------------------------
# iteration-statement:
#	for ( expressionopt ; expressionopt ; expressionopt ) statement
#	for ( declaration expressionopt ; expressionopt ) statement
# ---------------------------------------------------------------
def p_iteration_statement_1(t):
	'iteration_statement : FOR LPAREN expressionopt SEMI expressionopt SEMI expressionopt RPAREN statement'
	t[0] = (t.lineno(1), Stmt_For(t[3].list, t[5].list, t[7].list, t[9]))

def p_iteration_statement_2(t):
	'iteration_statement : FOR LPAREN declaration expressionopt SEMI expressionopt RPAREN statement'
	raise NotImplementedError


# ---------------------------------------------------------------
# jump-statement:
#	return expressionopt ;
#	break ;
#	continue ;
# ---------------------------------------------------------------
def p_jump_statement_1(t):
	'jump_statement : RETURN expressionopt SEMI'
	t[0] = (t.lineno(1), Stmt_Return(t[2]))

def p_jump_statement_2(t):
	'jump_statement : BREAK SEMI'
	t[0] = (t.lineno(1), Stmt_Break())

def p_jump_statement_3(t):
	'jump_statement : CONTINUE SEMI'
	t[0] = (t.lineno(1), Stmt_Cont())


# ---------------------------------------------------------------
# compound-statement:
#	{ block-item-listopt }
# ---------------------------------------------------------------
def p_compound_statement(t):
	'compound_statement : LBRACE block_item_listopt RBRACE'
	t[0] = (t.lineno(1), Stmt_Comp(t[2].list))


# ---------------------------------------------------------------
# block-item-listopt:
#	block-item-list
#	empty
# ---------------------------------------------------------------
def p_block_item_listopt_1(t):
	'block_item_listopt : block_item_list'
	t[0] = t[1]

def p_block_item_listopt_2(t):
	'block_item_listopt : empty'
	t[0] = myList()


# ---------------------------------------------------------------
# block-item-list:
#	block-item
#	block-item-list block-item
# ---------------------------------------------------------------
def p_block_item_list_1(t):
	'block_item_list : block_item'
	temp = myList()
	temp.add(t[1])
	t[0] = temp

def p_block_item_list_2(t):
	'block_item_list : block_item_list block_item'
	t[1].add(t[2])
	t[0] = t[1]


# ---------------------------------------------------------------
# block-item:
#	declaration
#	statement
# ---------------------------------------------------------------
def p_block_item_1(t):
	'block_item : declaration'
	t[0] = t[1]

def p_block_item_2(t):
	'block_item : statement'
	t[0] = t[1]


# ---------------------------------------------------------------
# expression-statement:
#	expressionopt ;
# ---------------------------------------------------------------
def p_expression_statement(t):
	'expression_statement : expressionopt SEMI'
	t[0] = (t.lineno(1), Stmt_Expr(t[1].list))


# ---------------------------------------------------------------
# expressionopt:
#	expression
#	empty
# ---------------------------------------------------------------
def p_expressionopt_1(t):
	'expressionopt : expression'
	t[0] = t[1]

def p_expressionopt_2(t):
	'expressionopt : empty'
	temp = myList()
	temp.add((t.lineno(1), Stmt_Mpty()))
	t[0] = temp


# ---------------------------------------------------------------
# expression:
#	assignment-expression
#	expression , assignment-expression
# ---------------------------------------------------------------
def p_expression_1(t):
	'expression : assignment_expression'
	temp = myList()
	if t[1] is not None:
		temp.add(t[1])
	t[0] = temp

def p_expression_2(t):
	'expression : expression COMMA assignment_expression'
	NotImplementedError
	t[1].add(t[3])
	t[0] = t[1]


# ---------------------------------------------------------------
# assignment-expressionopt:
#	assignment-expression
#	empty
# ---------------------------------------------------------------
def p_assignment_expressionopt_1(t):
	'assignment_expressionopt : assignment_expression'
	t[0] = t[1]

def p_assignment_expressionopt_2(t):
	'assignment_expressionopt : empty'
	t[0] = Stmt_Mpty()


# ---------------------------------------------------------------
# assignment-expression:
#	conditional-expression
#	unary-expression assignment-operator assignment-expression
# ---------------------------------------------------------------
def p_assignment_expression_1(t):
	'assignment_expression : conditional_expression'
	t[0] = t[1]

def p_assignment_expression_2(t):
	'assignment_expression : unary_expression assignment_operator assignment_expression'
	t[0] = Expr_Bin(BinOp.Asgn, (Expr_Var(t[1]), t[3]))


# ---------------------------------------------------------------
# assignment-operator:
#	=
# ---------------------------------------------------------------
def p_assignment_operator(t):
	'assignment_operator : EQUALS'
	pass


# ---------------------------------------------------------------
# conditional-expression:
#	logical-OR-expression
#	logical-OR-expression ? expression : conditional-expression			<- remove
# ---------------------------------------------------------------
def p_conditional_expression(t):
	'conditional_expression : logical_OR_expression'
	t[0] = t[1]


# ---------------------------------------------------------------
# logical-OR-expression:
#	logical-AND-expression
#	logical-OR-expression || logical-AND-expression
# ---------------------------------------------------------------
def p_logical_OR_expression_1(t):
	'logical_OR_expression : logical_AND_expression'
	t[0] = t[1]

def p_logical_OR_expression_2(t):
	'logical_OR_expression : logical_OR_expression LOR logical_AND_expression'
	t[0] = Expr_Bin(BinOp.Or, (t[1], t[3]))


# ---------------------------------------------------------------
# logical-AND-expression:
#	inclusive-OR-expression
#	logical-AND-expression && inclusive-OR-expression
# ---------------------------------------------------------------
def p_logical_AND_expression_1(t):
	'logical_AND_expression : inclusive_OR_expression'
	t[0] = t[1]

def p_logical_AND_expression_2(t):
	'logical_AND_expression : logical_AND_expression LAND inclusive_OR_expression'
	t[0] = Expr_Bin(BinOp.And, (t[1], t[3]))


# ---------------------------------------------------------------
# inclusive-OR-expression:
#	exclusive-OR-expression
#	inclusive-OR-expression | exclusive-OR-expression
# ---------------------------------------------------------------
def p_inclusive_OR_expression_1(t):
	'inclusive_OR_expression : exclusive_OR_expression'
	t[0] = t[1]

def p_inclusive_OR_expression_2(t):
	'inclusive_OR_expression : inclusive_OR_expression OR exclusive_OR_expression'
	raise NotImplementedError


# ---------------------------------------------------------------
# exclusive-OR-expression:
#	AND-expression
#	exclusive-OR-expression ^ AND-expression
# ---------------------------------------------------------------
def p_exclusive_OR_expression_1(t):
	'exclusive_OR_expression : AND_expression'
	t[0] = t[1]

def p_exclusive_OR_expression_2(t):
	'exclusive_OR_expression : exclusive_OR_expression XOR AND_expression'
	raise NotImplementedError


# ---------------------------------------------------------------
# AND-expression:
#	equality-expression
#	AND-expression & equality-expression
# ---------------------------------------------------------------
def p_AND_expression_1(t):
	'AND_expression : equality_expression'
	t[0] = t[1]

def p_AND_expression_2(t):
	'AND_expression : AND_expression AND equality_expression'
	raise NotImplementedError


# ---------------------------------------------------------------
# equality-expression:
#	relational-expression
#	equality-expression == relational-expression
#	equality-expression != relational-expression
# ---------------------------------------------------------------
def p_equality_expression_1(t):
	'equality_expression : relational_expression'
	t[0] = t[1]

def p_equality_expression_2(t):
	'equality_expression : equality_expression EQ relational_expression'
	t[0] = Expr_Bin(BinOp.Eq, t[1], t[3])

def p_equality_expression_3(t):
	'equality_expression : equality_expression NE relational_expression'
	t[0] = Expr_Bin(BinOp.Ne, t[1], t[3])


# ---------------------------------------------------------------
# relational-expression:
#	shift-expression
#	relational-expression < shift-expression
#	relational-expression > shift-expression
#	relational-expression <= shift-expression
#	relational-expression >= shift-expression
# ---------------------------------------------------------------
def p_relational_expression_1(t):
	'relational_expression : shift_expression'
	t[0] = t[1]

def p_relational_expression_2(t):
	'relational_expression : relational_expression LT shift_expression'
	t[0] = Expr_Bin(BinOp.Lt, (t[1], t[3]))

def p_relational_expression_3(t):
	'relational_expression : relational_expression GT shift_expression'
	t[0] = Expr_Bin(BinOp.Gt, (t[1], t[3]))

def p_relational_expression_4(t):
	'relational_expression : relational_expression LE shift_expression'
	t[0] = Expr_Bin(BinOp.Le, (t[1], t[3]))

def p_relational_expression_5(t):
	'relational_expression : relational_expression GE shift_expression'
	t[0] = Expr_Bin(BinOp.Ge, (t[1], t[3]))


# ---------------------------------------------------------------
# shift-expression:
#	additive-expression
#	shift-expression << additive-expression
#	shift-expression >> additive-expression
# ---------------------------------------------------------------
def p_shift_expression_1(t):
	'shift_expression : additive_expression'
	t[0] = t[1]

def p_shift_expression_2(t):
	'shift_expression : shift_expression LSHIFT additive_expression'
	raise NotImplementedError

def p_shift_expression_3(t):
	'shift_expression : shift_expression RSHIFT additive_expression'
	raise NotImplementedError


# ---------------------------------------------------------------
# additive-expression:
#	multiplicative-expression
#	additive-expression + multiplicative-expression
#	additive-expression - multiplicative-expression
# ---------------------------------------------------------------
def p_additive_expression_1(t):
	'additive_expression : multiplicative_expression'
	t[0] = t[1]

def p_additive_expression_2(t):
	'additive_expression : additive_expression PLUS multiplicative_expression'
	t[0] = Expr_Bin(BinOp.Add, (t[1], t[3]))

def p_additive_expression_3(t):
	'additive_expression : additive_expression MINUS multiplicative_expression'
	t[0] = Expr_Bin(BinOp.Sub, (t[1], t[3]))


# ---------------------------------------------------------------
# multiplicative-expression:
#	cast-expression
#	multiplicative-expression * cast-expression
#	multiplicative-expression / cast-expression
#	multiplicative-expression % cast-expression
# ---------------------------------------------------------------
def p_multiplicative_expression_1(t):
	'multiplicative_expression : cast_expression'
	t[0] = t[1]

def p_multiplicative_expression_2(t):
	'multiplicative_expression : multiplicative_expression TIMES cast_expression'
	t[0] = Expr_Bin(BinOp.Mul, (t[1], t[3]))

def p_multiplicative_expression_3(t):
	'multiplicative_expression : multiplicative_expression DIVIDE cast_expression'
	t[0] = Expr_Bin(BinOp.Div, (t[1], t[3]))

def p_multiplicative_expression_4(t):
	'multiplicative_expression : multiplicative_expression MOD cast_expression'
	t[0] = Expr_Bin(BinOp.Mod, (t[1], t[3]))


# ---------------------------------------------------------------
# cast-expression:
#	unary-expression
#	( type-name ) cast-expression
# ---------------------------------------------------------------
def p_cast_expression_1(t):
	'cast_expression : unary_expression'
	t[0] = t[1]

def p_cast_expression_2(t):
	'cast_expression : LPAREN type_name RPAREN cast_expression'
	raise NotImplementedError


# ---------------------------------------------------------------
# unary-expression:
#	postfix-expression
#	++ unary-expression
#	-- unary-expression
#	unary-operator cast-expression
#	sizeof unary-expression				<- remove
#	sizeof ( type-name )				<- remove
# ---------------------------------------------------------------
def p_unary_expression_1(t):
	'unary_expression : postfix_expression'
	t[0] = t[1]

def p_unary_expression_2(t):
	'unary_expression : INCREMENT unary_expression'
	t[0] = Expr_Un(UnOp.Inc, t[2])

def p_unary_expression_3(t):
	'unary_expression : DECREMENT unary_expression'
	t[0] = Expr_Un(UnOp.Dec, t[2])

def p_unary_expression_4(t):
	'unary_expression : unary_operator cast_expression'
	if t[1] == 'TIMES':
		t[0] = Expr_Un(UnOp.Deref, t[2])
	else: raise NotImplementedError 


# ---------------------------------------------------------------
# unary-operator: 
#	&
#	*
#	+
#	-
#	~
#	!
# ---------------------------------------------------------------
def p_unary_operator(t):
	'''unary_operator : AND
                      | TIMES
                      | PLUS
                      | MINUS
                      | NOT
                      | LNOT
                      '''
	t[0] = t[1]


# ---------------------------------------------------------------
# postfix-expression:
#	primary-expression
#	postfix-expression [ expression ]
#	postfix-expression ( argument-expression-listopt )
#	postfix-expression . identifier							<- remove
#	postfix-expression -> identifier						<- remove
#	postfix-expression ++
#	postfix-expression --
#	( type-name ) { initializer-list }
#	( type-name ) { initializer-list , }
# ---------------------------------------------------------------
def p_postfix_expression_1(t):
	'postfix_expression : primary_expression'
	t[0] = t[1]

def p_postfix_expression_2(t):
	'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
	if len(t[3].list) != 1 : raise NotImplementedError
	t[0] = Expr_Bin(BinOp.Idx, (Expr_Var(t[1]), t[3].list[0]))

def p_postfix_expression_3(t):
	'postfix_expression : postfix_expression LPAREN argument_expression_listopt RPAREN'
	t[0] = Expr_Call(t[1], t[3].list)

def p_postfix_expression_4(t):
	'postfix_expression : postfix_expression INCREMENT'
	t[0] = Expr_Un(UnOp.Inc, t[1])

def p_postfix_expression_5(t):
	'postfix_expression : postfix_expression DECREMENT'
	t[0] = Expr_Un(UnOp.Inc, t[1])

def p_postfix_expression_6(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list RBRACKET'
	raise NotImplementedError

def p_postfix_expression_7(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list COMMA RBRACKET'
	raise NotImplementedError


# ---------------------------------------------------------------
# primary-expression:
#	identifier
#	constant
#	string-literal
#	( expression )
# ---------------------------------------------------------------
def p_primary_expression_1(t):
	'''primary_expression : ID
                          | constant
                          | string_literal
                          '''
	t[0] = t[1]
def p_primary_expression_2(t):
	'primary_expression : LPAREN expression RPAREN'	
	if len(t[2].list) != 1: raise NotImplementedError
	t[0] = t[2].list[0]

def p_string_literal(t):
	'string_literal : STRING'
	t[0] = Expr_Lit(codecs.decode(t[1][1:-1], encoding='unicode_escape'))


# ---------------------------------------------------------------
# argument-expression-listopt:
#	argument-expression-list
#	empty
# ---------------------------------------------------------------
def p_argument_expression_listopt_1(t):
	'argument_expression_listopt : argument_expression_list'
	t[0] = t[1]

def p_argument_expression_listopt_2(t):
	'argument_expression_listopt : empty'
	t[0] = myList()


# ---------------------------------------------------------------
# argument-expression-list:
#	assignment-expression
#	argument-expression-list , assignment-expression
# ---------------------------------------------------------------
def p_argument_expression_list_1(t):
	'argument_expression_list : assignment_expression'
	temp = myList()
	temp.add(t[1])
	t[0] = temp

def p_argument_expression_list_2(t):
	'argument_expression_list : argument_expression_list COMMA assignment_expression'
	t[1].add(t[3])
	t[0] = t[1]


# ---------------------------------------------------------------
# constant 
# ---------------------------------------------------------------
def p_constant_1(t):
	'constant : INUM'
	t[0] = Expr_Lit(int(t[1]))

def p_constant_2(t):
	'constant : FNUM'
	t[0] = Expr_Lit(float(t[1]))

def p_constant_3(t):
	'constant : CHARACTER'
	raise NotImplementedError


# ---------------------------------------------------------------
# empty
# ---------------------------------------------------------------
def p_empty(t):
	'empty : '
	pass


# ---------------------------------------------------------------
# error
# ---------------------------------------------------------------
def p_error(t):
	print("Error");


# ---------------------------------------------------------------
# Build the grammar
# ---------------------------------------------------------------
parser = yacc.yacc()

def parse(code):
	return parser.parse(code, lexer = Lexer.lexer)



# ---------------------------------------------------------------
if __name__ == '__main__':
	import sys
	f = open(sys.argv[1], 'r')
	code = f.read()
	p = parser.parse(code, debug = True, lexer = Lexer.lexer)
	print(p)
