

# Compact
def fib1(number):
    if number <=2:
        return 1
    return fib1(number -1) + fib1(number - 2)

# My preference
def fib2(number):
    if number <= 2:
        return  1

    left  = fib2(number - 1)
    right = fib2(number - 2)

    return left + right


# Iterative
def fib3(number):
    a = 1
    b = 1

    for i in range(2, number + 1):
        temp = a
        a    = b
        b    = temp + a

    return a

def fib4(number):

    s = []

    left  = 1
    right = 1
    while number > 2:
        left  = number - 2
        right = number - 1

        s.append(left + right)

        number -=1


    print(s)

print(fib1(10))
print(fib2(10))



print(fib3(10))
print(fib4(10))
