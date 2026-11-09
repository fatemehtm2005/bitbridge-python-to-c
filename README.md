# Python to C Transpiler

An educational, source-to-source compiler project that translates a documented subset of Python 3 into portable C11 source. It also provides a verification command that runs the original Python program and the generated C program, then compares their standard output.

> **Project name is pending.** The repository is intentionally named descriptively until the final product name is selected.

## Supported Python subset

- Integer, float, Boolean, and string literals
- Variables and assignment
- Arithmetic, comparison, Boolean, and unary operators
- `print(...)`, including multiple positional values and `sep` / `end`
- `input()` / `input(prompt)`, `len(string)`, `int(value)`, `float(value)`, and `bool(value)`
- `if` / `elif` / `else`
- `while` loops, `for ... in range(...)`, `break`, and `continue`
- Functions with positional arguments and `return`

The compiler rejects unsupported syntax with source-line diagnostics. It does not claim to compile arbitrary Python programs, third-party packages, classes, dictionaries, generators, or dynamic features such as `eval`.

## Quick start

```powershell
python -m pyc_transpiler translate examples\basics.py -o build\basics.c
python -m pyc_transpiler verify examples\basics.py --compiler gcc
```

`verify` requires a C11 compiler such as GCC, Clang, or MSVC available on `PATH`.

## Architecture

```text
Python source -> Python AST -> validation -> C generator -> C11 source
                                                    |
                                               C runtime
                                                    |
                                  compile + execute + compare output
```

## Commands

```text
translate INPUT.py [-o OUTPUT.c]
verify INPUT.py [--compiler gcc] [--keep-artifacts]
```

## Development

```powershell
python -m unittest discover -s tests -v
```

## License

MIT
