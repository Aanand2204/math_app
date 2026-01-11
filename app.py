from flask import Flask, render_template, request
from math_ops import (
    parse_function,
    log_steps,
    differentiation_steps,
    integration_steps
)
from plot_utils import generate_plot
import sympy as sp

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    latex_result = None
    steps = []
    error = None
    plot_path = None
    plot_error = None

    if request.method == "POST":
        try:
            steps = []
            function_input = request.form.get("function")
            operation = request.form.get("operation")
            base_input = request.form.get("base")

            expr = parse_function(function_input)

            variables = sorted(expr.free_symbols, key=lambda s: s.name)
            if not variables:
                raise ValueError("No variable found in the expression.")

            var = variables[0]

            if operation == "log":
                base = float(base_input) if base_input else 10
                result, steps = log_steps(expr, base)

            elif operation == "derivative":
                result, steps = differentiation_steps(expr, var)

            elif operation == "integral":
                result, steps = integration_steps(expr, var)

            else:
                raise ValueError("Invalid operation")

            latex_result = sp.latex(result)

            # Plot only if single-variable
            if len(variables) == 1:
                plot_path, plot_error = generate_plot(expr)
            else:
                plot_error = "Plotting is available only for single-variable functions."

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template(
        "index.html",
        result=latex_result,
        steps=steps,
        error=error,
        plot_path=plot_path,
        plot_error=plot_error,
    )

# Required for Vercel
app=app
