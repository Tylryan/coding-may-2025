# Langlang
I'm currently learning how to implement languages. This language will probably
end up to be a concoction of Crafting Interpreter's Lox language with some other
ideas that I think would be neat to implement.

One of the main differences so far between my language and lox is the fact that
pretty much everything is an expression (well that's my intention anyway).


# Example
```
var a = 10;

var b = if (a > 10) { 20 }

print b; /* 20 */
```


> For more examples, see the [tests directory](./tests)