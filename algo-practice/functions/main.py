from time import sleep

# I stumbled upon an interesting idea while writing 
# a setup script for FreeBSD: turning a while loop
# into a function.
def while_loop(code_block_fn) -> object:
    counter = 0
    while True:
        returned, val = code_block_fn(counter)
        if returned: return val

        counter+=1
    
# With the 'while_loop' function declared above, you 
# can create an 'attempt' function which is a while 
# loop that only loops a maximum of 'n' times with
# an increasing delay time.
def attempt(code_block_fn, limit: int) -> object:
    # Logic to extend while_loop.
    def fn(counter: int) -> bool:
        to_break, ret_val  = code_block_fn(counter)
        if counter >= limit or to_break: 
            return (True, ret_val)

        print(f"Delaying {counter} second(s).")
        sleep(counter)

        return (False, ret_val)

    return while_loop(fn)


def main():
    # Define some sort of lambda or function which
    # returns (TO_BREAK, RETURN_OBJECT).
    def is_right(counter) -> tuple[bool, object]:
        answer = input(f"attempt {counter + 1}: ")

        valid_answers=["y", "n"]

        if answer in valid_answers:
            return (True, "Correct Answer!")

        return (False, "Incorrect Answer!")

    print("Will loop forever until is_right")
    ret: object = while_loop(is_right)
    print(ret)

    limit=5
    print(f"Will only loop {limit} times. With an increasing delay.")
    # Now the while loop returns a value.
    ret: object = attempt(is_right, limit=limit)
    print(ret)

if __name__ == "__main__":
    main()
