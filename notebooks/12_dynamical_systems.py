import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Dynamical Systems - Route to Chaos")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    plt.style.use('dark_background')
    return np, plt


@app.cell
def _(mo):
    mo.md(
        """
        # 12. Dynamical Systems - Iterated Maps

        [← Back to Index](index.html)

        ---

        **Iterated maps** show the route to chaos through bifurcations.
        Tiny parameter changes create radically different futures.

        ## The Logistic Map

        The simplest chaotic system:

        ### x_{n+1} = r · x_n · (1 - x_n)

        Where:
        - **x**: Population (0 to 1)
        - **r**: Growth rate parameter (0 to 4)
        - **n**: Time step

        This simple equation exhibits:
        - Fixed points
        - Period doubling
        - Chaos
        - Windows of order within chaos
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    system_type = mo.ui.dropdown(
        options=["Logistic Bifurcation", "Henon Attractor", "Tent Map Bifurcation"],
        value="Logistic Bifurcation",
        label="System Type"
    )
    system_type
    return (system_type,)


@app.cell
def _(mo):
    resolution = mo.ui.slider(500, 2000, value=1000, step=100, label="Resolution", full_width=True)
    resolution
    return (resolution,)


@app.cell
def _(mo):
    iterations = mo.ui.slider(100, 500, value=200, label="Iterations per r-value", full_width=True)
    iterations
    return (iterations,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["cyan", "hot", "plasma", "viridis", "white"],
        value="cyan",
        label="Point Color"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(colormap, iterations, np, plt, resolution, system_type):
    def logistic_bifurcation(res, iters):
        """
        Compute logistic map bifurcation diagram.

        For each r value, iterate the map and record the final values.
        """
        r_values = np.linspace(2.5, 4.0, res)
        last_n = iters  # Points to plot per r

        # Initial condition
        x = 0.1 * np.ones(res)

        # Warmup iterations (discard transient)
        for _ in range(500):
            x = r_values * x * (1 - x)

        # Collect points
        r_all, x_all = [], []
        for _ in range(last_n):
            x = r_values * x * (1 - x)
            r_all.extend(r_values)
            x_all.extend(x)

        return np.array(r_all), np.array(x_all)

    def henon_attractor(n_points=50000, a=1.4, b=0.3):
        """
        Generate Henon attractor points.

        x_{n+1} = 1 - a·x_n² + y_n
        y_{n+1} = b·x_n
        """
        points = np.zeros((n_points, 2))
        points[0] = [0.1, 0.1]

        for i in range(1, n_points):
            x, y = points[i - 1]
            points[i] = [1 - a * x**2 + y, b * x]

        return points

    def tent_map_bifurcation(res, iters):
        """
        Compute tent map bifurcation diagram.

        T(x) = μ·min(x, 1-x)
        """
        mu_values = np.linspace(0, 2, res)
        last_n = iters

        x = 0.1 * np.ones(res)

        # Warmup
        for _ in range(500):
            x = mu_values * np.minimum(x, 1 - x)
            x = np.clip(x, 0.001, 0.999)  # Prevent collapse to 0

        # Collect points
        mu_all, x_all = [], []
        for _ in range(last_n):
            x = mu_values * np.minimum(x, 1 - x)
            x = np.clip(x, 0.001, 0.999)
            mu_all.extend(mu_values)
            x_all.extend(x)

        return np.array(mu_all), np.array(x_all)

    # Generate data based on system type
    fig, ax = plt.subplots(figsize=(12, 8), facecolor="black")

    if system_type.value == "Logistic Bifurcation":
        r_vals, x_vals = logistic_bifurcation(resolution.value, iterations.value)
        ax.scatter(r_vals, x_vals, c=colormap.value, s=0.01, alpha=0.1)
        ax.set_xlabel("r (growth rate)", color="white", fontsize=10)
        ax.set_ylabel("x (population)", color="white", fontsize=10)
        ax.set_xlim([2.5, 4.0])
        ax.set_ylim([0, 1])
        ax.tick_params(colors="white")

    elif system_type.value == "Henon Attractor":
        henon_pts = henon_attractor()
        # Skip transient
        ax.scatter(
            henon_pts[1000:, 0], henon_pts[1000:, 1],
            c=colormap.value, s=0.1, alpha=0.3
        )
        ax.set_aspect("equal")
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-0.5, 0.5])
        ax.axis("off")

    elif system_type.value == "Tent Map Bifurcation":
        mu_vals, x_vals = tent_map_bifurcation(resolution.value, iterations.value)
        ax.scatter(mu_vals, x_vals, c=colormap.value, s=0.01, alpha=0.1)
        ax.set_xlabel("μ (slope)", color="white", fontsize=10)
        ax.set_ylabel("x", color="white", fontsize=10)
        ax.set_xlim([0, 2])
        ax.set_ylim([0, 1])
        ax.tick_params(colors="white")

    ax.set_facecolor("black")
    ax.set_title(system_type.value, color="white", fontsize=14, pad=10)
    plt.tight_layout()
    fig
    return (
        fig,
        henon_attractor,
        henon_pts,
        logistic_bifurcation,
        mu_vals,
        r_vals,
        tent_map_bifurcation,
        x_vals,
    )


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Reading the Bifurcation Diagram

        **Logistic map behavior by r:**

        | r range | Behavior |
        |---------|----------|
        | 0 - 1 | Extinction (x → 0) |
        | 1 - 3 | Single stable fixed point |
        | 3 - 3.45 | Period-2 oscillation |
        | 3.45 - 3.54 | Period-4 oscillation |
        | 3.54 - 3.57 | Period-8, 16, 32... (period doubling) |
        | 3.57+ | Chaos (with windows of order) |

        ---

        ## The Feigenbaum Constants

        The period-doubling cascade has universal properties:

        - **δ ≈ 4.669...**: Ratio of widths between bifurcations
        - **α ≈ 2.502...**: Ratio of widths of tines

        These constants appear in **all** period-doubling routes to chaos,
        not just the logistic map! This is deep mathematical universality.

        ---

        ## Other Systems

        **Henon Attractor:**
        - 2D chaotic map
        - Fractal structure (Cantor-like)
        - Positive Lyapunov exponent

        **Tent Map:**
        - Simpler than logistic (piecewise linear)
        - Exactly solvable in some cases
        - Same bifurcation structure

        ---

        ## Chaos vs Randomness

        Chaotic systems are:
        - **Deterministic**: Same initial conditions → same outcome
        - **Sensitive**: Tiny changes → completely different outcomes
        - **Bounded**: Stay within a finite region
        - **Aperiodic**: Never exactly repeat

        This is **deterministic chaos** - unpredictable but not random!

        ---

        [← Phase Portraits](11_phase_portraits.html) | [Back to Index](index.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
