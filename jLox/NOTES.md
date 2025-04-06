
# Chapter 6: Parser
> There are evidently several methods of parsing. The book
> uses Recursive Descent. Below are a few other parsing
> techniques:
> 1. LL(k)
> 2. LR(1)
> 3. LALR
> 4. Parser Combinators
> 5. Earley Parser
> 6. Shunting Yard Algorithm
> 7. Packrat Parser

The parser produces a Tree structure that represents the order code 
should be evaluated in, in reverse.

So the precedence level chart below is actually the reverse of
what you might expect.
## Precedence Levels
Each level should call the one higher to keep the parsing machine
from halting at any given level.
- expression()
- equality()
- comparison()
- term()
- factor()
- unary()
- primary()
## Grammar
```
expression ::= equality;
equality   ::= comparison ( ( "!=" | "==") comparison)*;
comparison ::= term ( ( ">" | ">=" | "<" | "<=" ) term)*;
term       ::= factor ( ("-" | "+" ) factor )*;
factor     ::= unary ( ("/" | "*" ) unary )*;
unary      ::= ("/" | "*" ) unary
             | primary;
primary    ::= NUMBER | STRING | "true" | "false" | "nil"
             | "(" expression ")";
```
## Gotchas
First, each rule needs to match expression at that precedence level or HIGHER.
So in the case of unary expressions, which are right associative, 
we would need to make sure it can continue up the precedence levels
by converting `unary ::= ("!" | "-") unary` into:
```bnf
unary ::= ("!" | "-") unary
       | primary;
```

Second, left associativity produces left-recursive grammars if not careful.
Take factor expressions as an example. The grammar for factor
expressions could simply be:
```bnf
factor ::= factor ("/" | "*") unary
         | unary;
```
This rule is left associative because "factor" is the name of the
rule and the very first a factor can be is itself. This can cause
an infinite loop.

One way to fix this is to update the grammar to:
```bnf
factor ::= unary ( ( "/" | "*") unary )*;
```

This works, but it makes the grammar a little less clear to the
reader. Another way is precedence climbing which I believe is explained
in part III.


