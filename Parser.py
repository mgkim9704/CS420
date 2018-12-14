# ----------------------------------------------------------------------
# Parser.py
# ----------------------------------------------------------------------

import sys
import yacc
import Lexer

# Get the token map
tokens = Lexer.tokens


# ---------------------------------------------------------------
# translation-unit:
#	external-declaration
#	translation-unit external-declaration
# ---------------------------------------------------------------
def p_translation_unit_1(t):
	'translation_unit : external_declaration'
	pass

def p_translation_unit_2(t):
	'translation_unit : translation_unit external_declaration'
	pass


# ---------------------------------------------------------------
# external-declaration:
#	function-definition
#	declaration
# ---------------------------------------------------------------
def p_external_declaration_1(t):
	'external_declaration : function_definition'
	pass

def p_external_declaration_2(t):
	'external_declaration : declaration'
	pass


# ---------------------------------------------------------------
# function-definition:
#	declaration-specifiers declarator declaration-listopt compound-statement
# ---------------------------------------------------------------
def p_function_definition(t):
	'function_definition : declaration_specifiers declarator declaration_listopt compound_statement'
	pass


# ---------------------------------------------------------------
# declaration:
#	declaration-specifiers init-declarator-listopt ;
# ---------------------------------------------------------------
def p_declaration(t):
	'declaration : declaration_specifiers init_declarator_listopt SEMI'
	pass


# ---------------------------------------------------------------
# declaration-listopt:
#	declaration-list
#	empty
# ---------------------------------------------------------------
def p_declaration_listopt_1(t):
	'declaration_listopt : declaration_list'
	pass


def p_declarationopt_list_2(t):
	'declaration_listopt : empty'
	pass


# ---------------------------------------------------------------
# declaration-list:
#	declaration
#	declaration-list declaration
#	empty
# ---------------------------------------------------------------
def p_declaration_list_1(t):
	'declaration_list : declaration'
	pass

def p_declaration_list_2(t):
	'declaration_list : declaration_list declaration'
	pass


# ---------------------------------------------------------------
# declaration-specifiersopt:
#	declaration-specifiers
#	empty
# ---------------------------------------------------------------
def p_declaration_specifiersopt_1(t):
	'declaration_specifiersopt : declaration_specifiers'
	pass

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
	pass

def p_declaration_specifiers_2(t):
	'declaration_specifiers : type_specifier declaration_specifiersopt'
	pass


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
	pass


# ---------------------------------------------------------------
# type-specifier:
#	void
#	char
#	int
#	float
# ---------------------------------------------------------------
def p_type_specifier(t):
	'''type_specifier : VOID
                      | CHAR
                      | INT
                      | FLOAT
                      '''


# ---------------------------------------------------------------
# init-declarator-listopt:
#	init-declarator-list
#	empty
# ---------------------------------------------------------------
def p_init_declarator_listopt_1(t):
	'init_declarator_listopt : init_declarator_list'
	pass

def p_init_declarator_listopt_2(t):
	'init_declarator_listopt : empty'
	pass


# ---------------------------------------------------------------
# init-declarator-list:
#	init-declarator
#	init-declarator-list , init-declarator
# ---------------------------------------------------------------
def p_init_declarator_list_1(t):
	'init_declarator_list : init_declarator'
	pass

def p_init_declarator_list_2(t):
	'init_declarator_list : init_declarator_list COMMA init_declarator'
	pass


# ---------------------------------------------------------------
# init-declarator:
#	declarator
#	declarator = initializer
# ---------------------------------------------------------------
def p_init_declarator_1(t):
	'init_declarator : declarator'
	pass

def p_init_declarator_2(t):
	'init_declarator : declarator EQUALS initializer'
	pass


# ---------------------------------------------------------------
# specifier-qualifier-listopt:
#	specifier-qualifier-list
#	empty
# ---------------------------------------------------------------
def p_specifier_qualifier_listopt_1(t):
	'specifier_qualifier_listopt : specifier_qualifier_list'
	pass

def p_specifier_qualifier_listopt_2(t):
	'specifier_qualifier_listopt : empty'
	pass


# ---------------------------------------------------------------
# specifier-qualifier-list:
#	type-specifier specifier-qualifier-listopt
#	type-qualifier specifier-qualifier-listopt		<- remove
# ---------------------------------------------------------------
def p_specifier_qualifier_list(t):
	'specifier_qualifier_list : type_specifier specifier_qualifier_listopt'
	pass


# ---------------------------------------------------------------
# declarator:
#	pointeropt direct-declarator
# ---------------------------------------------------------------
def p_declarator(t):
	'declarator : pointeropt direct_declarator'
	pass


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
	pass

def p_direct_declarator_2(t):
	'direct_declarator : LPAREN declarator RPAREN'
	pass

def p_direct_declarator_3(t):
	'direct_declarator : direct_declarator LBRACKET assignment_expressionopt RBRACKET'
	pass

def p_direct_declarator_4(t):
	'direct_declarator : direct_declarator LBRACKET STATIC assignment_expression RBRACKET'
	pass

def p_direct_declarator_5(t):
	'direct_declarator : direct_declarator LBRACKET TIMES RBRACKET'
	pass

def p_direct_declarator_6(t):
	'direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'
	pass

def p_direct_declarator_7(t):
	'direct_declarator : direct_declarator LPAREN identifier_listopt RPAREN'
	pass


# ---------------------------------------------------------------
# pointeropt:
#	pointer 
#	empty
# ---------------------------------------------------------------
def p_pointeropt_1(t):
	'pointeropt : pointer'
	pass

def p_pointeropt_2(t):
	'pointeropt : empty'
	pass


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
	pass


# ---------------------------------------------------------------
# parameter-list:
#	parameter-declaration
#	parameter-list , parameter-declaration
# ---------------------------------------------------------------
def p_parameter_list_1(t):
	'parameter_list : parameter_declaration'
	pass

def p_parameter_list_2(t):
	'parameter_list : parameter_list COMMA parameter_declaration'
	pass


# ---------------------------------------------------------------
# parameter-declaration:
#	declaration-specifiers declarator
#	declaration-specifiers abstract-declarator(opt <- remove)
# ---------------------------------------------------------------
def p_parameter_declaration_1(t):
	'parameter_declaration : declaration_specifiers declarator'
	pass

def p_parameter_declaration_2(t):
	'parameter_declaration : declaration_specifiers'
	pass


# ---------------------------------------------------------------
# identifier-listopt:
#	identifier-list
#	empty
# ---------------------------------------------------------------
def p_identifier_listopt_1(t):
	'identifier_listopt : identifier_list'
	pass

def p_identifier_listopt_2(t):
	'identifier_listopt : empty'
	pass


# ---------------------------------------------------------------
# identifier-list:
#	identifier
#	identifier-list , identifier
# ---------------------------------------------------------------
def p_identifier_list_1(t):
	'identifier_list : ID'
	pass

def p_identifier_list_2(t):
	'identifier_list : identifier_list COMMA ID'
	pass 



# ---------------------------------------------------------------
# initializer:
#	assignment-expression
#	{ initializer-list }
#	{ initializer-list , }
# ---------------------------------------------------------------
def p_initializer_1(t):
	'initializer : assignment_expression'
	pass

def p_initializer_2(t):
	'''initializer : LBRACE initializer_list RBRACE
                       | LBRACE initializer_list COMMA RBRACE'''
	pass


# ---------------------------------------------------------------
# initializer-list:
#	initializer
#	initializer_list , initializer
# ---------------------------------------------------------------
def p_initializer_list_1(t):
	'initializer_list : initializer'
	pass

def p_initializer_list_2(t):
	'initializer_list : initializer_list COMMA initializer'
	pass


# ---------------------------------------------------------------
# type-name:		
#	specifier-qualifier-list abstract-declarator(opt <- remove)
# ---------------------------------------------------------------
def p_type_name(t):
	'type_name : specifier_qualifier_list'
	pass


# ---------------------------------------------------------------
# parameter-type-list:
#	parameter-list
#	parameter-list , ...		<- remove
# ---------------------------------------------------------------
def p_parameter_type_list(t):
	'parameter_type_list : parameter_list'
	pass


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
	pass

def p_statement_2(t):
	'statement : iteration_statement'
	pass

def p_statement_3(t):
	'statement : jump_statement'
	pass

def p_statement_4(t):
	'statement : compound_statement'
	pass

def p_statement_5(t):
	'statement : expression_statement'
	pass


# ---------------------------------------------------------------
# selection-statement:
#	if ( expression ) statement
#	if ( expression ) statement else statement
# ---------------------------------------------------------------
def p_selection_statement_1(t):
	'selection_statement : IF LPAREN expression RPAREN statement'
	pass

def p_selection_statement_2(t):
	'selection_statement : IF LPAREN expression RPAREN statement ELSE statement'
	pass


# ---------------------------------------------------------------
# iteration-statement:
#	for ( expressionopt ; expressionopt ; expressionopt ) statement
#	for ( declaration expressionopt ; expressionopt ) statement
# ---------------------------------------------------------------
def p_iteration_statement_1(t):
	'iteration_statement : FOR LPAREN expressionopt SEMI expressionopt SEMI expressionopt RPAREN statement'
	pass

def p_iteration_statement_2(t):
	'iteration_statement : FOR LPAREN declaration expressionopt SEMI expressionopt RPAREN statement'
	pass


# ---------------------------------------------------------------
# jump-statement:
#	return expressionopt ;
# ---------------------------------------------------------------
def p_jump_statement(t):
	'jump_statement : RETURN expressionopt SEMI'
	pass


# ---------------------------------------------------------------
# compound-statement:
#	{ block-item-listopt }
# ---------------------------------------------------------------
def p_compound_statement(t):
	'compound_statement : LBRACE block_item_listopt RBRACE'
	pass


# ---------------------------------------------------------------
# block-item-listopt:
#	block-item-list
#	empty
# ---------------------------------------------------------------
def p_block_item_listopt_1(t):
	'block_item_listopt : block_item_list'
	pass

def p_block_item_listopt_2(t):
	'block_item_listopt : empty'
	pass


# ---------------------------------------------------------------
# block-item-list:
#	block-item
#	block-item-list block-item
# ---------------------------------------------------------------
def p_block_item_list_1(t):
	'block_item_list : block_item'
	pass

def p_block_item_list_2(t):
	'block_item_list : block_item_list block_item'
	pass


# ---------------------------------------------------------------
# block-item:
#	declaration
#	statement
# ---------------------------------------------------------------
def p_block_item_1(t):
	'block_item : declaration'
	pass

def p_block_item_2(t):
	'block_item : statement'
	pass


# ---------------------------------------------------------------
# expression-statement:
#	expressionopt ;
# ---------------------------------------------------------------
def p_expression_statement(t):
	'expression_statement : expressionopt SEMI'
	pass


# ---------------------------------------------------------------
# expressionopt:
#	expression
#	empty
# ---------------------------------------------------------------
def p_expressionopt_1(t):
	'expressionopt : expression'
	pass

def p_expressionopt_2(t):
	'expressionopt : empty'
	pass


# ---------------------------------------------------------------
# expression:
#	assignment-expression
#	expression , assignment-expression
# ---------------------------------------------------------------
def p_expression_1(t):
	'expression : assignment_expression'
	pass

def p_expression_2(t):
	'expression : expression COMMA assignment_expression'
	pass


# ---------------------------------------------------------------
# assignment-expressionopt:
#	assignment-expression
#	empty
# ---------------------------------------------------------------
def p_assignment_expressionopt_1(t):
	'assignment_expressionopt : assignment_expression'
	pass

def p_assignment_expressionopt_2(t):
	'assignment_expressionopt : empty'
	pass


# ---------------------------------------------------------------
# assignment-expression:
#	conditional-expression
#	unary-expression assignment-operator assignment-expression
# ---------------------------------------------------------------
def p_assignment_expression_1(t):
	'assignment_expression : conditional_expression'
	pass

def p_assignment_expression_2(t):
	'assignment_expression : unary_expression assignment_operator assignment_expression'
	pass


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


# ---------------------------------------------------------------
# logical-OR-expression:
#	logical-AND-expression
#	logical-OR-expression || logical-AND-expression
# ---------------------------------------------------------------
def p_logical_OR_expression_1(t):
	'logical_OR_expression : logical_AND_expression'
	pass

def p_logical_OR_expression_2(t):
	'logical_OR_expression : logical_OR_expression LOR logical_AND_expression'
	pass


# ---------------------------------------------------------------
# logical-AND-expression:
#	inclusive-OR-expression
#	logical-AND-expression && inclusive-OR-expression
# ---------------------------------------------------------------
def p_logical_AND_expression_1(t):
	'logical_AND_expression : inclusive_OR_expression'
	pass

def p_logical_AND_expression_2(t):
	'logical_AND_expression : logical_AND_expression LAND inclusive_OR_expression'
	pass


# ---------------------------------------------------------------
# inclusive-OR-expression:
#	exclusive-OR-expression
#	inclusive-OR-expression | exclusive-OR-expression
# ---------------------------------------------------------------
def p_inclusive_OR_expression_1(t):
	'inclusive_OR_expression : exclusive_OR_expression'
	pass

def p_inclusive_OR_expression_2(t):
	'inclusive_OR_expression : inclusive_OR_expression OR exclusive_OR_expression'
	pass


# ---------------------------------------------------------------
# exclusive-OR-expression:
#	AND-expression
#	exclusive-OR-expression ^ AND-expression
# ---------------------------------------------------------------
def p_exclusive_OR_expression_1(t):
	'exclusive_OR_expression : AND_expression'
	pass

def p_exclusive_OR_expression_2(t):
	'exclusive_OR_expression : exclusive_OR_expression XOR AND_expression'
	pass


# ---------------------------------------------------------------
# AND-expression:
#	equality-expression
#	AND-expression & equality-expression
# ---------------------------------------------------------------
def p_AND_expression_1(t):
	'AND_expression : equality_expression'
	pass

def p_AND_expression_2(t):
	'AND_expression : AND_expression AND equality_expression'
	pass


# ---------------------------------------------------------------
# equality-expression:
#	relational-expression
#	equality-expression == relational-expression
#	equality-expression != relational-expression
# ---------------------------------------------------------------
def p_equality_expression_1(t):
	'equality_expression : relational_expression'
	pass

def p_equality_expression_2(t):
	'equality_expression : equality_expression EQ relational_expression'
	pass

def p_equality_expression_3(t):
	'equality_expression : equality_expression NE relational_expression'
	pass


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
	pass

def p_relational_expression_2(t):
	'relational_expression : relational_expression LT shift_expression'
	pass

def p_relational_expression_3(t):
	'relational_expression : relational_expression GT shift_expression'
	pass

def p_relational_expression_4(t):
	'relational_expression : relational_expression LE shift_expression'
	pass

def p_relational_expression_5(t):
	'relational_expression : relational_expression GE shift_expression'
	pass


# ---------------------------------------------------------------
# shift-expression:
#	additive-expression
#	shift-expression << additive-expression
#	shift-expression >> additive-expression
# ---------------------------------------------------------------
def p_shift_expression_1(t):
	'shift_expression : additive_expression'
	pass

def p_shift_expression_2(t):
	'shift_expression : shift_expression LSHIFT additive_expression'
	pass

def p_shift_expression_3(t):
	'shift_expression : shift_expression RSHIFT additive_expression'
	pass


# ---------------------------------------------------------------
# additive-expression:
#	multiplicative-expression
#	additive-expression + multiplicative-expression
#	additive-expression - multiplicative-expression
# ---------------------------------------------------------------
def p_additive_expression_1(t):
	'additive_expression : multiplicative_expression'
	pass

def p_additive_expression_2(t):
	'additive_expression : additive_expression PLUS multiplicative_expression'
	pass

def p_additive_expression_3(t):
	'additive_expression : additive_expression MINUS multiplicative_expression'
	pass


# ---------------------------------------------------------------
# multiplicative-expression:
#	cast-expression
#	multiplicative-expression * cast-expression
#	multiplicative-expression / cast-expression
#	multiplicative-expression % cast-expression
# ---------------------------------------------------------------
def p_multiplicative_expression_1(t):
	'multiplicative_expression : cast_expression'
	pass

def p_multiplicative_expression_2(t):
	'multiplicative_expression : multiplicative_expression TIMES cast_expression'
	pass

def p_multiplicative_expression_3(t):
	'multiplicative_expression : multiplicative_expression DIVIDE cast_expression'
	pass

def p_multiplicative_expression_4(t):
	'multiplicative_expression : multiplicative_expression MOD cast_expression'
	pass


# ---------------------------------------------------------------
# cast-expression:
#	unary-expression
#	( type-name ) cast-expression
# ---------------------------------------------------------------
def p_cast_expression_1(t):
	'cast_expression : unary_expression'
	pass

def p_cast_expression_2(t):
	'cast_expression : LPAREN type_name RPAREN cast_expression'
	pass


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
	pass

def p_unary_expression_2(t):
	'unary_expression : INCREMENT unary_expression'
	pass

def p_unary_expression_3(t):
	'unary_expression : DECREMENT unary_expression'
	pass

def p_unary_expression_4(t):
	'unary_expression : unary_operator cast_expression'
	pass


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
	pass


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
	pass

def p_postfix_expression_2(t):
	'postfix_expression : postfix_expression LBRACKET expression RBRACKET'
	pass

def p_postfix_expression_3(t):
	'postfix_expression : postfix_expression LPAREN argument_expression_listopt RPAREN'
	pass

def p_postfix_expression_4(t):
	'postfix_expression : postfix_expression INCREMENT'
	pass

def p_postfix_expression_5(t):
	'postfix_expression : postfix_expression DECREMENT'
	pass

def p_postfix_expression_6(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list RBRACKET'
	pass

def p_postfix_expression_7(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list COMMA RBRACKET'
	pass


# ---------------------------------------------------------------
# primary-expression:
#	identifier
#	constant
#	string-literal
#	( expression )
# ---------------------------------------------------------------
def p_primary_expression(t):
	'''primary_expression : ID
                          | constant
                          | STRING
                          | LPAREN expression RPAREN
                          '''
	pass


# ---------------------------------------------------------------
# argument-expression-listopt:
#	argument-expression-list
#	empty
# ---------------------------------------------------------------
def p_argument_expression_listopt_1(t):
	'argument_expression_listopt : argument_expression_list'
	pass

def p_argument_expression_listopt_2(t):
	'argument_expression_listopt : empty'
	pass


# ---------------------------------------------------------------
# argument-expression-list:
#	assignment-expression
#	argument-expression-list , assignment-expression
# ---------------------------------------------------------------
def p_argument_expression_list_1(t):
	'argument_expression_list : assignment_expression'
	pass

def p_argument_expression_list_2(t):
	'argument_expression_list : argument_expression_list COMMA assignment_expression'
	pass


# ---------------------------------------------------------------
# constant 
# ---------------------------------------------------------------
def p_constant(t):
	'''constant : INUM
                | FNUM
                | CHARACTER'''
	pass


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



# ---------------------------------------------------------------
if __name__ == '__main__':
	import sys
	f = open(sys.argv[1], 'r')
	code = f.read()
	parser.parse(code, debug = True, lexer = Lexer.lexer)
