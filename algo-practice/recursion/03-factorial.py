# This uses the concept from 02-timing.py of 



def method1_factorial(number):
    
    if number == 1:
        return number

    return number * method1_factorial(number -1)

def method2_factorial(number):
    
    if number == 1:
        print("BASE CASE REACHED")
        return number

    # This is just emphasising that you can store
    # the results in a variable before the 
    # recursive function is over.
    print("BEFORE: ", number)
    stop_here = method2_factorial(number - 1)
    # At this point, `stop_here` is already calculated. There
    # is no more work to be done and the result can
    # be used at no without further computation.

    # Below, I've used the result of `stop_here` two more
    # times without having to find the result of `stop_here`
    # again. Compare that to `method1_factorial`.
    res = number * stop_here
    print(f"AFTER: {number} * {stop_here} = {res}")
    return res


print(method2_factorial(5))
