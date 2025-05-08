
/* (lexer | parser)? grammar IDENT ';' ; */
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

/* NOTE: The higher the line number, the lower the
 * precedence. For example, if you put IDENT on line
 * 5 and CLASS on line 6, then 'class' would be marked
 * as an IDENT!
 */

// Declarations
CLASS    : 'class';
FUN      : 'fun'  ;
VAR      : 'var'  ;
CONST    : 'const';
FN       : 'fn'   ;


// Conditions
IF     : 'if'   ;
ELSE   : 'else' ;
WHILE  : 'while';
FOR    : 'for'  ;

// Other Keywords
RETURN    : 'return'  ;
BREAK     : 'break'   ;
CONTINUE  : 'continue';


// Types
FLOAT    : DIGIT+ '.' DIGIT+;
INT      : DIGIT+           ;
STR      : '"' .*? '"'      ;
TRUE     : 'true'           ;
FALSE    : 'false'          ;
NULL     : 'null'           ;


// Other Operators
PLUS_PLUS    : '++';
MINUS_MINUS  : '--' ;

// Arithmetic Operators
PLUS     : '+' ;
MINUS    : '-' ;
STAR     : '*' ;
SLASH    : '/' ;
MODULO   : '%' ;

// Comparison Operators
EQUAL         : '=' ;
EQUAL_EQUAL   : '==';
LESS          : '<' ;
LESS_EQUAL    : '<=';
GREATER       : '>' ;
GREATER_EQUAL : '>=';
BANG          : '!' ;
BANG_EQUAL    : '!=';

// Logical Operators
AND : 'and';
OR  : 'or' ;


// Punctuation
SEMI      : ';';
LPAR      : '(';
RPAR      : ')';
LBRACE    : '{';
RBRACE    : '}';
DOT       : '.';
COMMA     : ',';

// Misc
SL_COMMENT: '//' .*? '\n';
ML_COMMENT: '/*' .*? '*/';

/* Must come after keywords */
IDENT    : [a-zA-Z_]+[\-!?]* ;

// Fragments
fragment DIGIT    : [0-9] ;

// Misc
WS       : [ \n\t\r]+ -> skip;
