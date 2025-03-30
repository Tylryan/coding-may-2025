# Try wrapping your mind around this one
# This is practically the same concept as count_up_and_down(),
# where I was emphasising the timing. However, this function
# calls itself not once, but twice.
def countup(start: int, end: int) -> None:
    print("CREATING STACK FRAME")

    if start >= end:
        print("BASE CASE")
        return

    print("CALLING COUNTUP FOR FIRST TIME: START = ", start)
    stop: None = countup(start + 1, end)
    print("START AFTER THE FIRST COUNTUP:\t", start)

    print("CALLING COUNTUP FOR THE SECOND TIME: START =", start)
    stop: None = countup(start + 1, end)
    print("START AFTER THE SECOND COUNTUP:\t", start)

    print("RETURNING FROM STACK FRAME\n")


print("START")
countup(0, 2)
print("END")


