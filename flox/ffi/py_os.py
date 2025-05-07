from flox_fun import FloxCallable

class PythonReadFile(FloxCallable):

    # open(file, mode)
    def arity(self):
        return 2
    def call(self, eval_block, args: list[object]) -> object:
        # Doing runtime check on this to save headaches in
        # the future.

        # TODO(tyler): Somehow get line numbers here.
        if len(args) != 2:
            print(f"[invalid-function-arity] 'read_file' requires """
            f"{self.arity()} arguments, but {len(args)} were/was given.")
            exit(1)
        file_path: str = args[0]
        mode     : str = args[1]

        try:
            f = open(file_path, mode)
            c = f.read()
            f.close()
            return c
        except Exception:
            print(f"[runtime-error] failed to open file: '{file_path}'.")
            exit(1)