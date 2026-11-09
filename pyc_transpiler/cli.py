"""Command-line interface for translating and verifying programs."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from .compiler import CompileError, compile_source


def translate(input_path: Path, output_path: Path) -> None:
    try:
        generated = compile_source(input_path.read_text(encoding="utf-8"), str(input_path))
    except OSError as exc:
        raise RuntimeError(f"could not read {input_path}: {exc}") from exc
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generated, encoding="utf-8")


def verify(input_path: Path, compiler: str, keep_artifacts: bool) -> int:
    if not shutil.which(compiler):
        raise RuntimeError(f"C compiler '{compiler}' was not found on PATH. Install GCC/Clang or use --compiler.")
    temporary = tempfile.TemporaryDirectory(prefix="pyc-transpiler-")
    work = Path(temporary.name)
    c_file, executable = work / "generated.c", work / ("generated.exe" if sys.platform == "win32" else "generated")
    translate(input_path, c_file)
    compile_result = subprocess.run([compiler, "-std=c11", str(c_file), "-o", str(executable)], capture_output=True, text=True)
    if compile_result.returncode:
        sys.stderr.write(compile_result.stderr)
        return 2
    python_result = subprocess.run([sys.executable, str(input_path)], capture_output=True, text=True)
    c_result = subprocess.run([str(executable)], capture_output=True, text=True)
    if python_result.returncode or c_result.returncode:
        sys.stderr.write("program execution failed\n")
        return 3
    if python_result.stdout != c_result.stdout:
        sys.stderr.write("output mismatch\n--- Python ---\n" + python_result.stdout + "--- C ---\n" + c_result.stdout)
        return 1
    print("Verification passed: Python and C output are identical.")
    if keep_artifacts:
        destination = Path.cwd() / "build"
        destination.mkdir(exist_ok=True)
        shutil.copy2(c_file, destination / "generated.c")
        shutil.copy2(executable, destination / executable.name)
    temporary.cleanup()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pyc-transpiler", description="Translate a documented Python subset to C11.")
    commands = parser.add_subparsers(dest="command", required=True)
    translate_parser = commands.add_parser("translate", help="generate C11 source")
    translate_parser.add_argument("input", type=Path)
    translate_parser.add_argument("-o", "--output", type=Path)
    verify_parser = commands.add_parser("verify", help="compile, run, and compare output")
    verify_parser.add_argument("input", type=Path)
    verify_parser.add_argument("--compiler", default="gcc")
    verify_parser.add_argument("--keep-artifacts", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.command == "translate":
            output = args.output or args.input.with_suffix(".c")
            translate(args.input, output)
            print(f"Generated {output}")
            return 0
        return verify(args.input, args.compiler, args.keep_artifacts)
    except (CompileError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
