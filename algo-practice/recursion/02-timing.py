# This function shows the two XYZ of a recursive
# function. Note: If you have 2 recursive calls,
# then there will be a BEFORE, DURING, AFTER phase
# inside the function.
def count_down_and_up(number: int) -> None:

    if number == 0:
        print("REACHED BASE CASE")
        return 1
    print("COUNT DOWN (BEFORE): ", number)

    # Res will print after DOWN and BASE CASE, but
    # before UP.
    res = count_down_and_up(number - 1)
    print("RES (MIDDLE): ", res)

    print("COUNT UP (AFTER): ", number)
    return number

count_down_and_up(2)
