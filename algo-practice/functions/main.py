from time import sleep

# I stumbled upon an interesting idea while writing 
# a setup script for FreeBSD: turning a while loop
# into a function.
#
# The code below demonstrates the advantage of such
# a design by making it painfully obvious how easy
# such a design is to extend. You can basically create
# your own language constructs within a host language
# using functions.
def while_loop(code_block_fn) -> object:
    counter = 0
    while True:
        returned, val = code_block_fn(counter)
        if returned: return val

        counter+=1

# A while loop with no while loop...
def _while_loop(code_block_fn) -> object:
    def __inner(counter):
        returned, val = code_block_fn(counter)
        if returned:
            return val
        __inner(counter + 1)

    return __inner(0)

# The while_loop can be extended by passing in a
# new function that adds more logic to the while_loop.
def until_loop(code_block_fn, limit: int) -> object:
    # Logic to extend while_loop
    def fn(counter: int) -> bool:
        to_break, ret_val  = code_block_fn(counter)
        if counter >= limit or to_break: 
            return (True, ret_val)

        return (False, ret_val)

    return while_loop(fn)

# Now the until_loop can be extended by passing
# in a new function to until_loop that adds more
# logic.
def attempt(code_block_fn, limit: int) -> object:
    # Logic to extend until_loop.
    def fn(counter: int) -> bool:
        to_break, ret_val  = code_block_fn(counter)
        if counter >= limit:
            return (True, ret_val)

        print(f"Delaying {counter} second(s).")
        sleep(counter)

        return (False, ret_val)

    return until_loop(fn, limit)


def main():
    # Define some sort of lambda or function which
    # returns (TO_BREAK, RETURN_OBJECT).
    def is_right(counter) -> tuple[bool, object]:
        answer = input(f"attempt {counter + 1}: ")

        valid_answers=["y", "n"]

        if answer in valid_answers:
            return (True, "Correct Answer!")

        return (False, "Incorrect Answer!")

    #ret: object = _while_loop(is_right)
    #print("Will loop forever until is_right")
    #ret: object = while_loop(is_right)
    #print(ret)

    limit=5
    print(f"Will only loop {limit} times. With an increasing delay.")
    # Now the while loop returns a value.
    ret: object = attempt(is_right, limit=limit)
    print(ret)

if __name__ == "__main__":
    main()
