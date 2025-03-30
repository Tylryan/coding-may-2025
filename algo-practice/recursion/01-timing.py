# This function shows the two XYZ of a recursive
# function. Note: If you have 2 recursive calls,
# then there will be a BEFORE, DURING, AFTER phase
# inside the function.
# Source: https://inventwithpython.com/recursion/chapter1.html
def count_down_and_up(number: int) -> None:

    if number == 0:
        print("REACHED BASE CASE (AND RETURNING)")
        return
    print("COUNT DOWN (BEFORE): ", number)

    count_down_and_up(number - 1)

    print("COUNT UP (AFTER/RETURNING): ", number)
    return


count_down_and_up(3)
