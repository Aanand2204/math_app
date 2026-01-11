import sympy as sp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

def generate_plot(function):
    x = sp.Symbol('x')
    x_vals = np.linspace(-5, 5, 300)

    try:
        f = sp.lambdify(x, function, 'numpy')
        y_vals = f(x_vals)

        if np.isscalar(y_vals):
            return None, "Function could not be plotted."

        y_vals = np.array(y_vals)
        valid = np.isfinite(y_vals)

        if not valid.any():
            return None, "Function could not be plotted."

        plt.figure()
        plt.plot(x_vals[valid], y_vals[valid], label=str(function))
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.title("Function Plot")
        plt.grid()
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format="png")
        plt.close()
        buffer.seek(0)

        plot_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return plot_base64, None

    except Exception:
        return None, "Function could not be plotted."
