from flask import Flask, request, render_template
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
import io
import base64
matplotlib.use('Agg')  # Use Agg backend to avoid Tkinter issues


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    steps = []
    error = None
    plot_path = None
    plot_error = None

    if request.method == 'POST':
        function_input = request.form.get('function')
        operation = request.form.get('operation')
        base_input = request.form.get('base')  # Get the base input for logarithm

        x = sp.symbols('x')

        try:
            function = sp.sympify(function_input)
            steps.append(f"Parsed function: {function}")

            if operation == 'log':
                base = float(base_input) if base_input else 10
                result, log_steps = log_steps_with_base(function, base)
                steps.extend(log_steps)
            elif operation == 'integral':
                result, integral_steps = integration_steps(function, x)
                steps.extend(integral_steps)
            elif operation == 'derivative':
                result, derivative_steps = differentiation_steps(function, x)
                steps.extend(derivative_steps)
            else:
                error = "Invalid operation selected."

            plot_path, plot_error = generate_plot(function)
           

        except Exception:
            error = "Invalid mathematical expression."

    return render_template('index.html', result=result, steps=steps, error=error, plot_path=plot_path, plot_error=plot_error)

def log_steps_with_base(function, base):
    steps = [f"Applying logarithm with base {base}"]
    result = sp.log(function, base)
    steps.append(f"Result: {result}")
    return result, steps

def integration_steps(function, x):
    steps = [f"Starting Integration of: {function}"]
    
    try:
        # Try integration using SymPy
        integral_result = sp.integrate(function, x)
    except Exception as e:
        return None, ["Integration could not be performed directly."]

    # Sum rule
    if function.is_Add:
        steps.append("Using sum rule: ∫(f + g) dx = ∫f dx + ∫g dx")

    # Product rule or substitution hint
    elif function.is_Mul and function.has(x):
        steps.append("This function is a product. Consider product rule or substitution.")

    # Logarithm-specific steps
    if function == sp.log(x):
        steps.extend([
            "Using integration by parts: ∫ u dv = u v - ∫ v du",
            "Let u = log(x), so dv = dx",
            "Differentiate u: du/dx = 1/x ⟹ du = (1/x)dx",
            "Integrate dv: ∫ dx = x, so v = x",
            "Apply formula: uv - ∫ v du",
            "Final result: x log(x) - x + C"
        ])
        integral_result = x * sp.log(x) - x  

    # Power rule
    elif function.is_Pow and function.base == x:
        n = function.exp
        if n != -1:
            steps.append(f"Using power rule: ∫ x^n dx = (x^(n+1)) / (n+1)")
            integral_result = (x**(n+1)) / (n+1)
        else:
            steps.append("Special case: ∫ x^(-1) dx = log|x|")
            integral_result = sp.log(x)

    # Partial fractions hint
    elif isinstance(function, sp.Basic) and function.is_Atom is False:
        steps.append("This is a rational function. If integration is complex, try partial fractions.")
        steps.append("Consider rewriting the function as simpler fractions before integrating.")

    steps.append(f"Final result: {integral_result}")
    return integral_result, steps





def differentiation_steps(function, x):
    steps = ["Starting Differentiation:"]
    derivative = sp.diff(function, x, evaluate=False)
    steps.append(f"Derivative before simplification: {derivative}")
    simplified = sp.simplify(derivative)
    steps.append(f"Simplified result: {simplified}")
    return simplified, steps

def generate_plot(function):
    x = sp.symbols('x')
    x_vals = np.linspace(-10, 10, 400)

    try:
        f = sp.lambdify(x, function, 'numpy')
        y_vals = f(x_vals)

        # Handle constant/scalar functions
        if np.isscalar(y_vals):
            return None, "Function could not be plotted."

        y_vals = np.array(y_vals)

        if y_vals.shape != x_vals.shape:
            return None, "Function could not be plotted."

        valid = np.isfinite(y_vals)
        if not np.any(valid):
            return None, "Function could not be plotted."

        # Create plot
        plt.figure()
        plt.plot(x_vals[valid], y_vals[valid], label=str(function))
        plt.title("Plot of the Function")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid()
        plt.legend()

        # Save plot to memory (NOT disk)
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        # Encode image to Base64
        plot_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

        return plot_base64, None

    except Exception:
        return None, "Function could not be plotted."


if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app= app
