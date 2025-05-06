# Flox
This language will basically be Lox (Crafting Interpreters), but with most everything
being an Expression.


```
var a = 0;
var b = 1;
var c = if (a)      { "NOPE" }
        else if (b) { "YEP"  }
        else        { "NOPE" };
```

## Preprocessor Work and Macros
I'm thinking of a preprocessor with it's own mini language that will 
be evaluated before compile. The preprocessor's main job will be:
 1. Declaring Macros, which will be expanded before compile time.
 2. Running code before compile time.time replacing macros with their return values.
Macros are allowed to be used anywhere in the program after they have
been defined and where they are imported. These macros are simply 
replaced with the their body if they are used in other parts
of a program like an assembly process/procedure.

```rs
// macro-definition := "macro" "$"IDENT ("=" EXPR ";")
//                                      | "( PARAMS? ) BlockExpr;
// macro-call := "$"IDENT ("(" PARAMS? ")" )? ;


$define(__linux__);
preprocesser {
    // This is where macros will be defined. Macros
    // can be used anywhere in the program after they
    // are defined and included.
    macros {
        macro $PI 3.14;
        macro $is_type(expr, type) { 
            if (expr.kind == type) {
                // Not a return from a function!
                // This is what will replace '$is_type'.
                return true;
            }
            return false;
        }
    }

    // The preprocessor code below would be evaluated before
    // the compiler pass. However, as nothing is being defined 
    // (in this case below), it does not remain in memory once 
    // the compiler pass begins.
    if ($defined(__linux__)) {
        // If username is not "David Hasselhoff", crash or
        // or something.

        // Macros can be used here.
        var a = $PI * 2;
    }

    $undefine(__linux__);
}

// Macros can be anywhere in the code after they are defined.
fun main() {
    // '$PI' would be replaced with 3.14
    // before the compiler was run.
    const pi_squared = $PI * $PI;


    // '$is_type' would be replaced with
    // 'true' before the compiler ran.
    if ($is_type(pi_squared, bool)) {
        print("This should be true.");
    } else {
        print("This should be false.");
    }
}

```