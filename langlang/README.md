# Langlang
I'm currently learning how to implement languages. This language will probably
end up to be a concoction of Crafting Interpreter's Lox language with some other
ideas that I think would be neat to implement.

One of the main differences so far between my language and lox is the fact that
pretty much everything is an expression (well that's my intention anyway).



# Examples
The following example demonstrates that "ifs" are if-expressions instead
of regular statements. Additionally, a variable can be set to the result
of an assignment.

```
var a = 10;
/* `b` is equal to 20 */
var b = if (a > 2) { a = 20 };

print a; /* 20 */
print b; /* 20 */

b = 10;
print a; /* 20 */
print b; /* 10 */

```

> For more examples, see the [tests directory](./tests)