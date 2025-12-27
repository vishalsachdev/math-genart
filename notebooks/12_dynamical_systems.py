import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Dynamical Systems - Route to Chaos")


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

        **Iterated maps** show the route to chaos through bifurcations. The logistic map
        x_{n+1} = r * x_n * (1 - x_n) exhibits fixed points, period doubling, and chaos.
        """
    )
    return


@app.cell
def _(mo):
    system_type = mo.ui.dropdown(
        options=["Logistic Bifurcation", "Henon Attractor", "Tent Map Bifurcation"],
        value="Logistic Bifurcation",
        label="System Type"
    )
    resolution = mo.ui.slider(500, 2000, value=1000, step=100, label="Resolution", full_width=True)
    iterations = mo.ui.slider(100, 500, value=200, label="Iterations per r-value", full_width=True)
    colormap = mo.ui.dropdown(
        options=["cyan", "hot", "plasma", "viridis", "white"],
        value="cyan",
        label="Point Color"
    )
    return system_type, resolution, iterations, colormap


@app.cell
def _(mo, system_type, resolution, iterations, colormap, np, plt):
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
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

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

    controls = mo.vstack([
        mo.md("### Controls"),
        system_type, resolution, iterations, colormap,
        mo.md("---"),
        mo.md("""
**Logistic map behavior by r:**
- r < 3: Stable fixed point
- 3 < r < 3.57: Period doubling
- r > 3.57: Chaos with order windows

**Try:** Henon Attractor for 2D chaos
        """)
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


if __name__ == "__main__":
    app.run()
