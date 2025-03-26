import sys
def perror(error_msg, _exit = True):
    print(error_msg, file=sys.stderr)

    if _exit:
        exit(1)
