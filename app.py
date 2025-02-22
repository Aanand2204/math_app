from flask import Flask, request, render_template
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib
matplotlib.use('Agg')  # Use Agg backend to avoid Tkinter issues


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    steps = []
    error = None
    plot_path = None

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

            plot_path = generate_plot(function)

        except Exception as e:
            error = str(e)

    return render_template('index.html', result=result, steps=steps, error=error, plot_path=plot_path)

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
    x_vals = np.linspace(-10, 10, 400)
    f = sp.lambdify(sp.symbols('x'), function, 'numpy')

    try:
        y_vals = f(x_vals)
    except Exception as e:
        return None

    if np.isscalar(y_vals):
        y_vals = np.array([y_vals])
    valid_indices = np.isfinite(y_vals)
    x_vals = x_vals[valid_indices]
    y_vals = y_vals[valid_indices]

    plt.figure()
    plt.plot(x_vals, y_vals, label=str(function))
    plt.title('Plot of the Function')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.axhline(0, color='black', linewidth=0.5, ls='--')
    plt.axvline(0, color='black', linewidth=0.5, ls='--')
    plt.grid()
    plt.legend()
    
    plot_path = 'static/plot.png'
    plt.savefig(plot_path)
    plt.close()
    return plot_path

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
