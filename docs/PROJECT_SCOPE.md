# Project scope and acceptance criteria

## Purpose

The project demonstrates a transparent compilation pipeline from a practical subset of Python 3 to portable C11. It is an educational compiler prototype, not a replacement for CPython, Cython, or a full production compiler.

## Deliverables

1. Command-line translator producing a `.c` file from a `.py` file.
2. Embedded C runtime for numeric values, Booleans, strings, expressions, and output.
3. Source diagnostics for unsupported syntax.
4. Verification command that compiles generated C, executes both programs, and checks output equality.
5. Examples, tests, architecture documentation, and a reproducible GitHub repository.

## Acceptance criteria

- A supported input file is translated without manual source rewriting.
- Generated C compiles as C11 with a compatible compiler.
- The verification command reports matching output for included examples.
- Unsupported constructs result in a readable error with a source location.

## Explicit boundaries

The first version accepts a documented subset only. Classes, imports, third-party packages, dictionaries, list literals, exceptions, comprehensions, async code, reflection, and Python's dynamic object model are outside this project's acceptance scope.
