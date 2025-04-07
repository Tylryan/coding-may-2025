
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
- assignment()
- equality()
- comparison()
- term()
- factor()
- unary()
- primary()
## Grammar
```
expression ::= equality;
assignment ::= IDENT "=" assignment
             | equality ;
equality   ::= comparison ( ( "!=" | "==") comparison)* ;
comparison ::= term ( ( ">" | ">=" | "<" | "<=" ) term)* ;
term       ::= factor ( ("-" | "+" ) factor )* ;
factor     ::= unary ( ("/" | "*" ) unary )* ;
unary      ::= ("/" | "*" ) unary
             | primary ;
primary    ::= NUMBER | STRING | "true" | "false" | "nil"
             | "(" expression ")" ;
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


# Chapter 8
## Assignment
### Grammar
```
<assign> ::= IDENT "=" <expr>
           | <next_precedence_level>
```
### Examples
Below are two valid assignment expressions:
```
a.b.c = d;
a = b = c = d;
```

Here is an invalid assignment where the left side is not
an l-value.
```
"hello, world!" = 5;
```
### Implementation
1. Evaluate the left side of the expression.
2. While at an equal sign, parse the right side using the **right**
   **associative** rule. 
   - See below for the difference between right and left associativity in code.
3. If the left side is an l-value (such as a Variable), assign the the right expression to the variable.
    - If it is not, throw error.


### Right Associativity
Assignment is right associative. This means an expression like
`a = b = c;` would be evaluated like `(a = (b = c));` instead of
`((a = b) = c)`.

In order to achieve right associativity, you would pretty much
do the same thing as what you'd do for left associativity except
for one thing: when parsing the right side, don't go up a precedence
level.

```python
def assignment():
    left = next_precedence_level()
    
    while match(EQUAL):
        operator = previous()
        right = assignment()
        # If we were to instead go to the next precedence level
        # here, then this would be left associative.
        # right = next_precedence_level()
        left = BinOp(left, operator, right)
    return left
```