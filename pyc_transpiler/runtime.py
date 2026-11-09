"""C runtime embedded into every generated program."""

RUNTIME = r'''#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>

typedef enum { PY_INT, PY_FLOAT, PY_BOOL, PY_STR, PY_NONE } PyTag;
typedef struct { PyTag tag; long long i; double f; const char *s; } PyValue;

static PyValue py_int(long long x) { return (PyValue){PY_INT, x, (double)x, NULL}; }
static PyValue py_float(double x) { return (PyValue){PY_FLOAT, (long long)x, x, NULL}; }
static PyValue py_bool(bool x) { return (PyValue){PY_BOOL, x ? 1 : 0, x ? 1.0 : 0.0, NULL}; }
static PyValue py_str(const char *x) { return (PyValue){PY_STR, 0, 0.0, x}; }
static PyValue py_none(void) { return (PyValue){PY_NONE, 0, 0.0, NULL}; }
static bool py_is_float(PyValue x) { return x.tag == PY_FLOAT; }
static double py_num(PyValue x) { return py_is_float(x) ? x.f : (double)x.i; }
static bool py_truth(PyValue x) {
  if (x.tag == PY_STR) return x.s && x.s[0];
  if (x.tag == PY_NONE) return false;
  return py_is_float(x) ? x.f != 0.0 : x.i != 0;
}
static PyValue py_add(PyValue a, PyValue b) {
  if (a.tag == PY_STR && b.tag == PY_STR) {
    size_t n = strlen(a.s) + strlen(b.s) + 1; char *out = malloc(n);
    if (!out) { fputs("out of memory\\n", stderr); exit(2); }
    strcpy(out, a.s); strcat(out, b.s); return py_str(out);
  }
  return (py_is_float(a) || py_is_float(b)) ? py_float(py_num(a) + py_num(b)) : py_int(a.i + b.i);
}
static PyValue py_sub(PyValue a, PyValue b) { return (py_is_float(a) || py_is_float(b)) ? py_float(py_num(a) - py_num(b)) : py_int(a.i - b.i); }
static PyValue py_mul(PyValue a, PyValue b) { return (py_is_float(a) || py_is_float(b)) ? py_float(py_num(a) * py_num(b)) : py_int(a.i * b.i); }
static PyValue py_div(PyValue a, PyValue b) { if (py_num(b) == 0) { fputs("division by zero\\n", stderr); exit(2); } return py_float(py_num(a) / py_num(b)); }
static PyValue py_mod(PyValue a, PyValue b) { if (b.i == 0) { fputs("modulo by zero\\n", stderr); exit(2); } return py_int(a.i % b.i); }
static PyValue py_neg(PyValue a) { return py_is_float(a) ? py_float(-a.f) : py_int(-a.i); }
static bool py_eq(PyValue a, PyValue b) {
  if (a.tag == PY_STR || b.tag == PY_STR) return a.tag == PY_STR && b.tag == PY_STR && strcmp(a.s, b.s) == 0;
  return py_num(a) == py_num(b);
}
static void py_print(PyValue x) {
  if (x.tag == PY_STR) printf("%s", x.s);
  else if (x.tag == PY_FLOAT) printf("%g", x.f);
  else if (x.tag == PY_BOOL) printf("%s", x.i ? "True" : "False");
  else if (x.tag == PY_NONE) printf("None");
  else printf("%lld", x.i);
}
'''
