
lexer grammar FloxToken;

/* Token types are just numbers, but they are ordered by 
 * appearance in this file. For example, since 'FUN' is
 * the first token, it would map to the number 1. 'VAR'
 * would map to the number 2 and so on. If I were
 * to want to update the positioning of these tokens
 * in this g4 file in the future, it would break my
 * Python code.
 * In order to prevent this, I'm explicitly defining
 * their 'type'.
 */

// Declarations
CLASS    : 'class' -> type(1);
FUN      : 'fun'   -> type(2);
VAR      : 'var'   -> type(3);
CONST    : 'const' -> type(4);
FN       : 'fn'    -> type(5);


// Conditions
IF     : 'if'   -> type(10);
WHILE  : 'while'-> type(11);
FOR    : 'for'  -> type(12);

// Other Keywords
RETURN    : 'return'   -> type(13);
BREAK     : 'break'    -> type(14);
CONTINUE  : 'continue' -> type(15);

// Types
FLOAT    : DIGIT+ '.' DIGIT+ -> type(20);
INT      : DIGIT+            -> type(21);
STR      : '"' .*? '"'       -> type(22);
TRUE     : 'true'            -> type(23);
FALSE    : 'false'           -> type(24);
NULL     : 'null'            -> type(25);
IDENT    : [a-zA-Z_]+[\-!?]* -> type(26);


// Arithmetic Operators
PLUS     : '+' -> type(40);
MINUS    : '-' -> type(41);
STAR     : '*' -> type(42);
SLASH    : '/' -> type(43);
MODULO   : '%' -> type(44);

// Comparison Operators
EQUAL         : '='  -> type(50);
EQUAL_EQUAL   : '==' -> type(51);
LESS          : '<'  -> type(52);
LESS_EQUAL    : '<=' -> type(53);
GREATER       : '>'  -> type(54);
GREATER_EQUAL : '>=' -> type(54);
BANG          : '!'  -> type(55);
BANG_EQUAL    : '!=' -> type(56);

// Logical Operators
AND : 'and' -> type(60);
OR  : 'or'  -> type(61);

// Punctuation
SEMI      : ';' -> type(70);
LPAR      : '(' -> type(71);
RPAR      : ')' -> type(72);
LBRACE    : '{' -> type(73);
RBRACE    : '}' -> type(74);
DOT       : '.' -> type(75);

// Misc
SL_COMMENT: '//' .*? '\n' -> type(100);
ML_COMMENT: '/*' .*? '*/' -> type(101);

// Fragments
fragment DIGIT    : [0-9] ;

// Misc
WS       : [ \n\t\r]+ -> skip;
