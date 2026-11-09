# Contributing

## Development setup

Use Python 3.10 or newer. No third-party Python package is required.

```powershell
python -m unittest discover -s tests -v
python -m pyc_transpiler translate examples\fizzbuzz.py -o build\fizzbuzz.c
```

## Pull-request checklist

1. Add a focused test for each supported AST feature or diagnostic.
2. Keep the supported-language list in `README.md` and `docs/PROJECT_SCOPE.md` current.
3. Do not silently accept syntax that the generator cannot preserve correctly.
4. Run the unit-test command before committing.
