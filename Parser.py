# ----------------------------------------------------------------------
# Parser.py
# ----------------------------------------------------------------------

import sys
import yacc
import Lexer

# Get the token map
tokens = Lexer.tokens


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
# constant 
# ---------------------------------------------------------------
def p_constant(t):
	'''constant : INUM
                | FNUM
                | CHARACTER'''
	pass



# ---------------------------------------------------------------
# postfix-expression:
#	primary-expression
#	postfix-expression [ expression ]
#	postfix-expression ( argument-expression-list(opt) )
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
	'postfix_expression : postfix_expression LPAREN argument_expression_list RPAREN'
	pass

def p_postfix_expression_4(t):
	'postfix_expression : postfix_expression LPAREN RPAREN'
	pass

def p_postfix_expression_5(t):
	'postfix_expression : postfix_expression INCREMENT'
	pass

def p_postfix_expression_6(t):
	'postfix_expression : postfix_expression DECREMENT'
	pass

def p_postfix_expression_7(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list RBRACKET'
	pass

def p_postfix_expression_8(t):
	'postfix_expression : LPAREN type_name RPAREN LBRACKET initializer_list COMMA RBRACKET'
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
# conditional-expression:
#	logical-OR-expression
#	logical-OR-expression ? expression : conditional-expression			<- remove
# ---------------------------------------------------------------
def p_conditional_expression(t):
	'conditional_expression : logical_OR_expression'


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
# constant-expression:
	conditional-expression
# ---------------------------------------------------------------
def p_constant_expression(t):
	'constant_expression : conditional_expression'
	pass



# ---------------------------------------------------------------
# declaration:
#	declaration-specifiers init-declarator-list(opt) ;
# ---------------------------------------------------------------
def p_declaration_1(t):
	'declaration : declaration_specifiers init_declarator_list SEMI'
	pass

def p_declaration_2(t):
	'declaration : declaration_specifiers SEMI'
	pass


# ---------------------------------------------------------------
# declaration-specifiers:
#	storage-class-specifier declaration-specifiers(opt)
#	type-specifier declaration-specifiers(opt)
#	type-qualifier declaration-specifiers(opt)				<- remove
#	function-specifier declaration-specifiers(opt)			<- remove
# ---------------------------------------------------------------
def p_declaration_specifiers_1(t):
	'declaration_specifiers : storage_class_specifier declaration_specifiers'
	pass

def p_declaration_specifiers_2(t):
	'declaration_specifiers : storage_class_specifier'
	pass

def p_declaration_specifiers_3(t):
	'declaration_specifiers : type_specifier declaration_specifiers'
	pass

def p_declaration_specifiers_4(t):
	'declaration_specifiers : type_specifier'
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
# specifier-qualifier-list:
#	type-specifier specifier-qualifier-list(opt)
#	type-qualifier specifier-qualifier-list(opt)		<- remove
# ---------------------------------------------------------------
def p_specifier_qualifier_list_1(t):
	'specifier_qualifier_list : type_specifier specifier_qualifier_list'
	pass

def p_specifier_qualifier_list_2(t):
	'specifier_qualifier_list : type_specifier'
	pass


# ---------------------------------------------------------------
# declarator:
#	pointer(opt) direct-declarator
# ---------------------------------------------------------------
def p_declarator_1(t):
	'declarator : pointer direct_declarator'
	pass

def p_declarator_2(t):
	'declarator : direct_declarator'
	pass


# ---------------------------------------------------------------
# direct-declarator:				<- type-qualifier-list remove
#	identifier
#	( declarator )
#	direct-declarator [ type-qualifier-list(opt) assignment-expression(opt) ]
#	direct-declarator [ static type-qualifier-list(opt) assignment-expression ]
#	direct-declarator [ type-qualifier-list static assignment-expression ]		
#	direct-declarator [ type-qualifier-list(opt) * ]
#	direct-declarator ( parameter-type-list )
#	direct-declarator ( identifier-list(opt) )
# ---------------------------------------------------------------
def p_direct_declarator_1(t):
	'direct_declarator : ID'
	pass

def p_direct_declarator_2(t):
	'direct_declarator : LPAREN declarator RPAREN'
	pass

def p_direct_declarator_3(t):
	'direct_declarator : direct_declarator LBRACKET assignment_expression RBRACKET'
	pass

def p_direct_declarator_4(t):
	'direct_declarator : direct_declarator LBRACKET RBRACKET'
	pass

def p_direct_declarator_5(t):
	'direct_declarator : direct_declarator LBRACKET STATIC assignment_expression RBRACKET'
	pass

def p_direct_declarator_6(t):
	'direct_declarator : direct_declarator LBRACKET TIMES RBRACKET'
	pass

def p_direct_declarator_7(t):
	'direct_declarator : direct_declarator LPAREN parameter_type_list RPAREN'
	pass

def p_direct_declarator_8(t):
	'direct_declarator : direct_declarator LPAREN identifier_list RPAREN'
	pass

def p_direct_declarator_9(t):
	'direct_declarator : direct_declarator LPAREN RPAREN'
	pass


# ---------------------------------------------------------------
# pointer:
#	* 
# ---------------------------------------------------------------
def p_pointer(t):
	'pointer : TIMES'
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
# type-name:		
#	specifier-qualifier-list abstract-declarator(opt <- remove)
# ---------------------------------------------------------------
def p_type_name(t):
	'type_name : specifier_qualifier_list'
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
	'initializer : LBRACE initializer_list RBRACE'
	pass

def p_initializer_3(t):
	'initializer : LBRACE initializer_list COMMA RBRACE'
	pass


# ---------------------------------------------------------------
# initializer-list:
#	designation(opt) initializer
#	initializer_list , designation(opt) initializer
# ---------------------------------------------------------------
def p_initializer_list_1(t):
	'initializer_list : designation initializer'
	pass

def p_initializer_list_2(t):
	'initializer_list : initializer'
	pass

def p_initializer_list_3(t):
	'initializer_list : initializer_list designation initializer'
	pass

def p_initializer_list_4(t):
	'initializer_list : initializer_list initializer'
	pass


# ---------------------------------------------------------------
# designation:
#	designator-list =
# ---------------------------------------------------------------
def p_designation(t):
	'designation : designator_list EQUALS'
	pass


# ---------------------------------------------------------------
# designator-list:
#	designator
#	designator-list designator
# ---------------------------------------------------------------
def p_designator_list_1(t):
	'designator_list : designator'
	pass

def p_designator_list_2(t):
	'designator_list : designator_list designator'
	pass


# ---------------------------------------------------------------
# designator:
#	[ constant-expression ]
#	. identifier 					<- remove
# ---------------------------------------------------------------
def p_designator_1(t):
	'designator : LBRACE constant_expression RBRACE'
	pass


# ---------------------------------------------------------------
# statement:
#	selection-statement
#	iteration-statement
#	jump_statement
#	compound-statement
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


# ---------------------------------------------------------------
# compound-statement:
#	{ block-item-list(opt) }
# ---------------------------------------------------------------
def p_compound_statement_1(t):
	'compound_statement : LBRACE block_item_list RBRACE'
	pass

def p_compound_statement_2(t):
	'compound_statement : LBRACE RBRACE'
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
#	for ( expression(opt) ; expression(opt) ; expression(opt) ) statement
#	for ( declaration expression(opt) ; expression(opt) ) statement
# ---------------------------------------------------------------
def p_iteration_statement_1(t):
	'iteration_statement : FOR LPAREN expression SEMI expression SEMI expression RPAREN statement'
	pass

def p_iteration_statement_2(t):
	'iteration_statement : FOR LPAREN SEMI expression SEMI expression RPAREN statement'
	pass

def p_iteration_statement_3(t):
	'iteration_statement : FOR LPAREN expression SEMI SEMI expression RPAREN statement'
	pass

def p_iteration_statement_4(t):
	'iteration_statement : FOR LPAREN expression SEMI expression SEMI RPAREN statement'
	pass

def p_iteration_statement_5(t):
	'iteration_statement : FOR LPAREN SEMI SEMI expression RPAREN statement'
	pass

def p_iteration_statement_6(t):
	'iteration_statement : FOR LPAREN SEMI expression SEMI RPAREN statement'
	pass

def p_iteration_statement_7(t):
	'iteration_statement : FOR LPAREN expression SEMI SEMI RPAREN statement'
	pass

def p_iteration_statement_8(t):
	'iteration_statement : FOR LPAREN SEMI SEMI RPAREN statement'
	pass

def p_iteration_statement_9(t):
	'iteration_statement : FOR LPAREN declaration expression SEMI expression RPAREN statement'
	pass

def p_iteration_statement_10(t):
	'iteration_statement : FOR LPAREN declaration SEMI expression RPAREN statement'
	pass

def p_iteration_statement_11(t):
	'iteration_statement : FOR LPAREN declaration expression SEMI RPAREN statement'
	pass

def p_iteration_statement_12(t):
	'iteration_statement : FOR LPAREN declaration SEMI RPAREN statement'
	pass


# ---------------------------------------------------------------
# jump-statement:
#	return expression(opt) ;
# ---------------------------------------------------------------
def p_jump_statement_1(t):
	'jump_statement : RETURN expression SEMI'
	pass

def p_jump_statement_2(t):
	'jump_statement : RETURN SEMI'
	pass


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
#	declaration-specifiers declarator declaration-list(opt) compound-statement
# ---------------------------------------------------------------
def p_function_definition_1(t):
	'function_definition : declaration_specifiers declarator declaration_list compound_statement'
	pass

def p_function_definition_2(t):
	'function_definition : declaration_specifiers declarator compound_statement'
	pass


# ---------------------------------------------------------------
# declaration-list:
#	declaration
#	declaration-list declaration
# ---------------------------------------------------------------
def p_declaration_list_1(t):
	'declaration_list : declaration'
	pass

def p_declaration_list_2(t):
	'declaration_list : declaration_list declaration'
	pass


# ---------------------------------------------------------------
# error
# ---------------------------------------------------------------
def p_error(t):
	print("Error");

# ---------------------------------------------------------------
# Build the grammar
# ---------------------------------------------------------------
yacc.yacc()
