# A recursive function can be converted to an iterative function
# using a loop and a stack. https://inventwithpython.com/recursion/chapter2.html

# Here's how to convert the recursive factorial function to an iterative one.


def rfact(number):
    if number == 1:
        return number

    print("BEFORE: ", number)
    res = rfact(number - 1)
    print(f"AFTER: {number} * {res} = {number * res}")

    return res * number


# His example shows that it can be done, my example shows the exact
# translation (At least I think).
def ifact(number):

    stack = []

    while number > 0:
        print("BEFORE: ", number)
        stack.append(number)
        number -=1

    print("BASE CASE (JUST PRETEND)")
    print("STACK: ", stack)

    res = 1

    # Just going backwards through the stack
    i = len(stack)
    while i > 0:
        n = stack.pop()
        print(f"AFTER: {n} * {res} = {n * res}")
        res *= n

        i-=1

    return res

    


print("RFACT"); print(rfact(5))
print("IFACT"); print(ifact(5))

