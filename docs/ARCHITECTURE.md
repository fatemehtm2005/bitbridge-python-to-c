# Architecture

## Pipeline

1. Python's standard `ast` module parses source code.
2. The generator validates every statement and expression against the supported grammar.
3. A C11 generator maps AST nodes to runtime operations and structured C control flow.
4. A compact runtime represents integers, floating-point values, Booleans, strings, and `None`.
5. The verifier runs the original Python program and the compiled C executable, then compares standard output byte-for-byte.

## Design choices

- **C11 output:** the generated output remains inspectable and portable.
- **Tagged values:** a small `PyValue` type keeps source generation simple while supporting several primitive Python types.
- **Fail-fast diagnostics:** unsupported dynamic behavior is rejected during generation instead of silently producing wrong C.
- **Behavioral verification:** output comparison provides a direct and understandable correctness signal for supported examples.
