# USAGE
# 	If you're just wanting to run the whole compiler on the
# 	default test file (specified below by the variable 'FILE?'),
# 	then you can just run:
# 	$ make
#
# 	If you wanted to run just the lexer or parser by themselves,
# 	then you can run:
# 	$ make lexer
# 	$ make parser
#
# 	# If you wanted to specify which langlang test script to run,
# 	then run:
# 	$ make FILE=/path/to/file.langlang
#
ARITH=tests/01-arithmetic.txt
VARIABLES=tests/02-global-variables.txt
SCOPE=tests/03-scope.txt
SCOPE_FULL=tests/03-scope-full.txt
IF=tests/04-if.txt
IF_ELSE=tests/04-if-else.txt
WHILE=tests/05-while.txt
WHILE_BREAK=tests/05-while-break.txt
FUN=tests/06-functions.txt
FILE?=$(FUN)


i:
	make interpreter

# Since this rule is at the top of all the other rules, it is the rule
# executed when running `make` without any arguments.
interpreter:
	make parser

interpreter:
	python interpreter.py $(FILE)

# This is just an alias for running the lexer.
l:
	make lexer
# make lexer will 
lexer:
	python lexer.py $(FILE)

p:
	make parser
parser:
	python parser.py $(FILE)
