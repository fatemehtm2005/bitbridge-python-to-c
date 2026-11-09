"""A compact Python-subset to C11 source translator."""

from .compiler import CompileError, compile_source

__all__ = ["CompileError", "compile_source"]
