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

def power_rule(coef, power, var):
    if power == 1:
        return (
            f"Using the power rule: $$ \\frac{{d}}{{d{var}}}(x) = 1 $$",
            coef
        )
    else:
        return (
            f"Using the power rule: "
            f"$$ \\frac{{d}}{{d{var}}}({coef}{var}^{power})"
            f" = {coef * power}{var}^{power - 1} $$",
            coef * power * var ** (power - 1)
        )

def log_steps(expr, base):
    steps = []

    steps.append(
        "Step 1: Identify the logarithmic expression."
    )

    steps.append(
        f"Step 2: Apply the definition of logarithm:"
        f"$$ \\log_{{{base}}}({sp.latex(expr)}) $$"
    )

    result = sp.log(expr, base)

    steps.append(
        f"Final Answer:"
        f"$$ {sp.latex(result)} $$"
    )

    return result, steps



def differentiation_steps(expr, var):
    steps = []
    result_terms = []

    steps.append(
        f"Step 1: Identify the variable of differentiation:"
        f"$$ \\frac{{d}}{{d{var}}} $$"
    )

    steps.append(
        f"Step 2: Write the given function:"
        f"$$ f({var}) = {sp.latex(expr)} $$"
    )

    terms = sp.Add.make_args(expr)

    steps.append(
        "Step 3: Split the function into individual terms."
    )

    for term in terms:
        coef, power = term.as_coeff_exponent(var)

        if power == 0:
            steps.append(
                f"Constant term: $$ {sp.latex(term)} $$ → Derivative is 0"
            )
            continue

        explanation, derived = power_rule(coef, power, var)
        steps.append(explanation)
        result_terms.append(derived)

    final_result = sum(result_terms)

    steps.append(
        "Step 4: Combine all differentiated terms."
    )

    steps.append(
        f"Final Answer:"
        f"$$ \\frac{{d}}{{d{var}}}({sp.latex(expr)})"
        f" = {sp.latex(final_result)} $$"
    )

    return final_result, steps



def integration_steps(expr, var):
    steps = []
    result_terms = []

    steps.append(
        f"Step 1: Identify the variable of integration:"
        f"$$ \\int \\, d{var} $$"
    )

    steps.append(
        f"Step 2: Write the given function:"
        f"$$ f({var}) = {sp.latex(expr)} $$"
    )

    terms = sp.Add.make_args(expr)

    steps.append(
        "Step 3: Integrate each term separately using power rule."
    )

    for term in terms:
        coef, power = term.as_coeff_exponent(var)

        if power == -1:
            steps.append(
                f"$$ \\int \\frac{{1}}{{{var}}} \\, d{var}"
                f" = \\ln|{var}| $$"
            )
            result_terms.append(sp.log(var))
        else:
            new_power = power + 1
            integrated = coef * var ** new_power / new_power

            steps.append(
                f"$$ \\int {sp.latex(term)} \\, d{var}"
                f" = \\frac{{{coef}}}{{{new_power}}}{var}^{new_power} $$"
            )

            result_terms.append(integrated)

    final_result = sum(result_terms)

    steps.append(
        "Step 4: Combine all integrated terms and add constant of integration."
    )

    steps.append(
        f"Final Answer:"
        f"$$ \\int {sp.latex(expr)} \\, d{var}"
        f" = {sp.latex(final_result)} + C $$"
    )

    return final_result, steps



