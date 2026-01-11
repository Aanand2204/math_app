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
    variables = []

    if request.method == "POST":
        try:
            function_input = request.form.get("function")
            operation = request.form.get("operation")
            base_input = request.form.get("base")

            function = parse_function(function_input)
            steps.append(f"Parsed function: $$ {sp.latex(function)} $$")

            variables = sorted(function.free_symbols, key=lambda s: s.name)
            steps.append(f"Detected variables: {', '.join(map(str, variables))}")

            selected_var = request.form.get("variable")
            if operation in ["derivative", "integral"]:
                if len(variables) == 0:
                    raise ValueError("No variable to differentiate or integrate.")

                if len(variables) == 1:
                    var = variables[0]
                else:
                    if not selected_var:
                        raise ValueError("Please select a variable.")
                    var = sp.Symbol(selected_var)


            if operation == "log":
                base = float(base_input) if base_input else 10
                result, op_steps = log_steps(function, base)

            elif operation == "derivative":
                result, op_steps = differentiation_steps(function, var)


            elif operation == "integral":
                result, op_steps = integration_steps(function, var)

            else:
                raise ValueError("Invalid operation")

            latex_result = sp.latex(result)

            # Plot only if single-variable
            if len(variables) == 1:
                plot_path, plot_error = generate_plot(function)
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
        variables=[str(v) for v in variables]
    )

# Required for Vercel
app=app
