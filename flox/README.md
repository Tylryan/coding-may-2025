# Flox
This language will basically be Lox (Crafting Interpreters), but with most everything
being an Expression.


```rs

fun map(fn, xs) { 
	fun map__(ys, res) {
		if (len(ys) == 0) {
			return res;
		}
		var got_got = fn(head(ys));
		return map__(tail(ys), append(got_got, res));
	}

	return map__(xs, List());
}

fun filter(fn, xs) {
	fun filter__(ys, res) {
		if (len(ys) == 0) {
			return res;
		}

		var predicate = fn(head(ys));

		if (predicate) 
			return filter__(tail(ys), append(head(ys), res));
		else filter__ 
			return filter__(tail(ys), res);
	}

	return filter__(xs, List());
}



/* TODO(tyler): a function with no parameters 
 * crashes when called. */
fun main(a) {

	var a = List(1,2,3);
	print(a);

	fun square(n) {return n * n; }

	var b = map(square, a);
	print(b);

	fun large_number(n) {
		/* TODO(tyler): shouldn't have to 
		 * explicitly return here. */
		if (n > 2)  { return true ; }
		else        { return false ;}
	}

	var c = filter(large_number, b);
	print(c);
}

main(1);
```

## Some Interesting Ideas
### Preprocessor Work and Macros
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
        macro $PI = 3.14;
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

}
$undefine(__linux__);

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


### Private Code

```js
// Create private blocks that contain code
// only visible in the current file.
private {
        fun secret_helper(x) { 
                return x + x; 
        }
        fun other_secret_helper(y) {
                return secret_helper(y) * secret_helper(y);
        }
}

fun public_function(y) {
        return other_secret_helper(y);
}


// private code within the same file is visible.
fun main() {
        // These two print statements would display
        // the same thing.
        print(other_secret_helper(10));
        print(public_function(10));
}
```

### Structs.
```js
// @allargs is already provided
// by default.
struct Person { name, age };


// However, if you wanted to define your own 
// initializer, you could use a static method.
// Note the implicit return.

// Methods can be added to structs at any
// point in the program. This idea came from
// traits in Rust.
extend Person {
        fun Self::new(name, age) { 
                return Person(name, age);
        }
        fun Self::from(tuple) {
                name = tuple.get(0);
                age = tuple.get(1);

                Person(name, age);
        }

        fun greet(self, other) {
                print($format("Hello '{other.name}', my name is '{self.name}'." ));
        }

        fun Person::compare(lhs, rhs) {
                if (lhs.age == rhs.age)     { 0  }
                else if (lhs.age > rhs.age) { 1  }
                else                        { -1 }
        }
}

fun main() {
        // Instantiating a new 'person' using
        // the default initializer.
        me  = Person("Me", 1000);
        // The same thing but using a custom
        // initializer.
        you = Person::new("You", 10001);

        // "Hello 'You', my name is 'Me'.
        me.greet(you);            
        Person::compare(me, you); // -1
}
```

### Types
```js
type Expr = Literal
           | Binary ;

struct Literal { number: f64 };
struct Binary  { 
        left : Expr , 
        op   : str  ,
        right: Expr 
};

extend Literal {
        fun as_map(self) -> HashMap[str, object] { 
                var hm = HashMap::new();
                hm.put("literal", self.token.value);
                return hm
        }
}

extend Binary {
        fun as_map(self) -> HashMap[str, object] { 
                var binary_expr =  HashMap::new();
                var inner: HashMap::new();

                inner.put("left", self.left.as_map());
                inner.put("op", self.op);
                inner.put("right", self.right.as_map());

                hm.put("binary-expr", inner);
                return hm
        }
}

// Not practical, but the example is clear.
fun print_expr(expr: Expr) -> null {
        match (expr) {
                Literal => print(expr.as_map()),
                Binary => print(binary.as_map()),
        }
}

fun main() {
        var bin_op: Binary = Binary(Literal(1), "+", Literal(2));

        print_expr(bin_op);
        // OUTPUT
        //{
        //        "binary-expr": {
        //                "left" : literal : { 1 },
        //                "op"   : "+",
        //                "right": literal : { 2 }
        //        }
        //}
}

```

### Reference Counting
At some point, I'd like to learn about Garbage Collection and I think the simplest
place to start is Reference Counting.

The MVP would be a language that had no GC by default and manual reference counting.
#### Manual Reference Counting
```rs
fun create_person(name: str) -> Rc[Person] {
        return Rc::track(Person(name));
}

fun main() {

        person: Rc[Person] = create_person("Me");
        other_person: Rc[Person] = create_person("You");

        // Creates a reference cycle
        person.friends.push(other_person);
        Rc::add_ref(other_person)


        // ... Other stuff ...

        // Eventually will be freed when ref_count == 0
        Rc::remove_ref(other_person);
        Rc::remove_ref(person);

        // Or free quickly if you no
        // longer need it.
        Rc::free(person);
}
```

#### Automatic Reference Counting

```rs
Arc::remove();
Arc::ref_count();
Arc::strong();  // Same thing as Arc::track()
Arc::ref();
Arc::free();
// Eventually we'll need to detect cycles like the one 
// above.
Arc::weak();
```