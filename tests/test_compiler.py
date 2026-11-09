import unittest

from pyc_transpiler import CompileError, compile_source


class CompilerTests(unittest.TestCase):
    def test_generates_program_and_runtime(self):
        c_source = compile_source('name = "Ada"\nprint("Hello, " + name)\n')
        self.assertIn("int main(void)", c_source)
        self.assertIn('py_str("Ada")', c_source)
        self.assertIn("py_add", c_source)

    def test_generates_control_flow_and_functions(self):
        source = """\
def double(value):
    return value * 2

for index in range(3):
    if index == 1:
        print(double(index))
"""
        c_source = compile_source(source)
        self.assertIn("PyValue py_double", c_source)
        self.assertIn("for (", c_source)
        self.assertIn("if (py_eq", c_source)

    def test_rejects_unknown_name(self):
        with self.assertRaisesRegex(CompileError, "undefined variable"):
            compile_source("print(missing)\n")

    def test_rejects_unsupported_container(self):
        with self.assertRaisesRegex(CompileError, "unsupported expression"):
            compile_source("items = [1, 2]\n")

    def test_handles_string_escaping(self):
        c_source = compile_source('print("quote: \\" and newline\\n")\n')
        self.assertIn('quote:', c_source)
        self.assertIn('\\\\n', c_source)


if __name__ == "__main__":
    unittest.main()
