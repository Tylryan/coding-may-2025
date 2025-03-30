# A recursive function can be converted to an iterative function
# using a loop and a stack. https://inventwithpython.com/recursion/chapter2.html

# Here's how to convert the recursive factorial function to an iterative one.


def rfact(number):
    if number == 1:
        return number

    res = rfact(number - 1)

    return res * number


def ifact(number):

    s = []

    while number > 0:
        print("BEFORE: ", number)
        s.append(number)
        number -=1

    print("BASE CASE (JUST PRETEND)")
    print("STACK: ", s)

    res = 1

    for n in s:
        print(f"AFTER: {n} * {res} = {n * res}")
        res *=n

    return res

    


print(ifact(5))

