all:
	antlr4 FloxToken.g4 -Dlanguage=Python3
	python flox_lexer.py

clean:
	rm *.interp *.tokens FloxToken*.py
