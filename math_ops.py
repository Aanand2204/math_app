import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)

# Common symbol
x = sp.Symbol('x')

# Parser configuration
TRANSFORMATIONS = standard_transformations + (
    implicit_multiplication_application,
    convert_xor
)

def to_latex(expr):
    return sp.latex(expr)

def parse_function(expr_str):
    """
    Parse user input like '7x+3y' safely.
    """
    allowed_symbols = {
        'x': sp.Symbol('x'),
        'y': sp.Symbol('y')
    }

    return parse_expr(
        expr_str,
        local_dict=allowed_symbols,
        transformations=TRANSFORMATIONS
    )

def log_steps(function, base):
    steps = [f"Applying logarithm with base {base}"]
    result = sp.log(function, base)
    steps.append(f"Result: {result}")
    return result, steps

def differentiation_steps(function, var):
    steps = [f"Differentiating with respect to {var}"]
    derivative = sp.diff(function, var, evaluate=False)
    steps.append(f"Derivative: {sp.latex(derivative)}")
    simplified = sp.simplify(derivative)
    steps.append(f"Simplified result: {sp.latex(simplified)}")
    return simplified, steps


def integration_steps(function, var):
    steps = [f"Integrating with respect to {var}"]
    result = sp.integrate(function, var)
    steps.append(f"Result: {sp.latex(result)} + C")
    return result, steps

