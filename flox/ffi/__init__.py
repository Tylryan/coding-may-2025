from __future__ import annotations

from ffi.py_os import PythonReadFile
from ffi.py_print import PythonPrint
from ffi.flox_list import *
from lox_env import Env
from tokens import fake_token



def load_ffis(env: Env):
    env.define(fake_token("print"), PythonPrint())
    env.define(fake_token("read_file"), PythonReadFile())
    env.define(fake_token("List"), List())
    env.define(fake_token("head"), Head())
    env.define(fake_token("tail"), Tail())
    env.define(fake_token("append"), Append())
    env.define(fake_token("prepend"), Prepend())
    env.define(fake_token("len"), Len())