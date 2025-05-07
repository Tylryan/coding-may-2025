from __future__ import annotations

from ffi.py_os import PythonReadFile
from ffi.py_print import PythonPrint
from lox_env import Env
from tokens import fake_token



def load_ffis(env: Env):
    env.define(fake_token("print"), PythonPrint())
    env.define(fake_token("read_file"), PythonReadFile())