"""This module extends the form language with free function operators,
which are either already available as member functions on UFL objects
or defined as compound operators involving basic operations on the UFL
objects."""

__authors__ = "Martin Sandve Alnes and Anders Logg"
__date__ = "2008-04-09 -- 2009-01-09"

import math
from ufl.log import ufl_assert, error
from ufl.zero import Zero
from ufl.scalar import ScalarValue, as_ufl
from ufl.differentiation import VariableDerivative, Grad, Div, Curl, Rot
from ufl.tensoralgebra import Transposed, Inner, Outer, Dot, Cross, Determinant, Inverse, Cofactor, Trace, Deviatoric, Skew
from ufl.variable import Variable
from ufl.conditional import EQ, NE, LE, GE, LT, GT, Conditional
from ufl.mathfunctions import Sqrt, Exp, Ln, Cos, Sin

#--- Tensor operators ---

def transpose(A):
    "The transposed of A."
    return Transposed(A)

def outer(a, b):
    "The outer product of a and b."
    return Outer(a, b)

def inner(a, b):
    "The inner product of a and b."
    return Inner(a, b)

def dot(a, b):
    "The dot product of a and b."
    return Dot(a, b)

def cross(a, b):
    "The cross product of a and b."
    return Cross(a, b)

def det(A):
    "The determinant of A."
    return Determinant(A)

def inv(A):
    "The inverse of A."
    return Inverse(A)

def cofac(A):
    "The cofactor of A."
    return Cofactor(A)

def tr(A):
    "The trace of A."
    return Trace(A)

def dev(A):
    "The deviatoric part of A."
    return Deviatoric(A)

def skew(A):
    "The skew symmetric part of A."
    return Skew(A)

#--- Differential operators

def Dx(f, *i):
    "The partial derivative of f with respect to spatial variable number i."
    return f.dx(*i)

def Dt(f):
    #return TimeDerivative(f) # TODO: Add class
    raise NotImplementedError

def diff(f, v):
    "The derivative of f with respect to the variable v."
    return VariableDerivative(f, v)

def grad(f):
    "The gradient of f."
    return Grad(f)

def div(f):
    "The divergence of f."
    return Div(f)

def curl(f):
    "The curl of f."
    return Curl(f)

def rot(f):
    "The rot of f."
    return Rot(f)

#--- DG operators ---

def jump(v):
    "The jump of v across a facet."
    r = v.rank()
    cell = v.cell()
    ufl_assert(cell is not None, "FIXME: Not all expressions have a cell. How should this be done? What does FFC do?")
    n = cell.n
    if r == 0:
        return v('+')*n('+') + v('-')*n('-')
    elif r == 1:
        return dot(v('+'), n('+')) + dot(v('-'), n('-'))
    else:
        error("jump(v) is only defined for scalar or vector-valued expressions (not rank %d expressions)." % r)

def avg(v):
    "The average of v across a facet."
    return 0.5*(v('+') + v('-'))

#--- Other operators ---

def variable(e):
    "A variable representing the given expression."
    return Variable(e)

#--- Conditional expressions ---

def conditional(condition, true_value, false_value):
    "A conditional expression, like the C construct (condition ? true_value : false_value)."
    return Conditional(condition, true_value, false_value)

def eq(left, right):
    "A boolean expresion (left == right) for use with conditional."
    return EQ(left, right)

def ne(left, right):
    "A boolean expresion (left != right) for use with conditional."
    return NE(left, right)

def le(left, right):
    "A boolean expresion (left <= right) for use with conditional."
    return LE(left, right)

def ge(left, right):
    "A boolean expresion (left >= right) for use with conditional."
    return GE(left, right)

def lt(left, right):
    "A boolean expresion (left < right) for use with conditional."
    return LT(left, right)

def gt(left, right):
    "A boolean expresion (left > right) for use with conditional."
    return GT(left, right)

def sign(x):
    "The sign (+1 or -1) of x."
    return conditional(eq(x, 0), 0, conditional(lt(x, 0), -1, +1))

#--- Math functions ---

def _mathfunction(f, cls, fun):
    f = as_ufl(f)
    if isinstance(f, ScalarValue): return as_ufl(fun(f._value))
    if isinstance(f, Zero): return as_ufl(fun(0))
    return cls(f)

def sqrt(f):
    "The square root of f."
    return _mathfunction(f, Sqrt, math.sqrt)

def exp(f):
    "The exponential of f."
    return _mathfunction(f, Exp, math.exp)

def ln(f):
    "The natural logarithm of f."
    return _mathfunction(f, Ln, math.log)

def cos(f):
    "The cosinus of f."
    return _mathfunction(f, Cos, math.cos)

def sin(f):
    "The sinus of f."
    return _mathfunction(f, Sin, math.sin)

