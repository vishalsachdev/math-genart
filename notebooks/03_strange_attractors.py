import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Strange Attractors - Chaos with Memory")


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
        # 3. Strange Attractors - Chaos with Memory

        [← Back to Index](index.html)

        **Strange attractors** are geometric structures that chaotic systems evolve toward.
        Deterministic but unpredictable, bounded but fractal.
        """
    )
    return


@app.cell
def _(mo):
    attractor_type = mo.ui.dropdown(
        options=["Lorenz", "Clifford", "Aizawa", "Thomas", "Halvorsen"],
        value="Clifford",
        label="Attractor Type"
    )
    num_points = mo.ui.slider(10000, 300000, value=100000, step=10000, label="Points", full_width=True)
    seed = mo.ui.slider(1, 100, value=42, label="Seed", full_width=True)
    colormap = mo.ui.dropdown(
        options=["plasma", "viridis", "magma", "inferno", "cividis", "twilight", "turbo"],
        value="plasma",
        label="Color Map"
    )
    point_size = mo.ui.slider(0.01, 0.5, value=0.1, step=0.01, label="Point Size", full_width=True)
    return attractor_type, colormap, num_points, point_size, seed


@app.cell
def _(attractor_type, colormap, mo, np, num_points, plt, point_size, seed):
    def generate_lorenz(n_points, random_seed, sigma=10, rho=28, beta=8/3, dt=0.01):
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3)
        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                sigma * (y - x), x * (rho - z) - y, x * y - beta * z
            ]) * dt
        return points

    def generate_clifford(n_points, random_seed, a=-1.4, b=1.6, c=1.0, d=0.7):
        np.random.seed(random_seed)
        points = np.zeros((n_points, 2))
        points[0] = np.random.randn(2) * 0.1
        for i in range(1, n_points):
            x, y = points[i-1]
            points[i] = [np.sin(a * y) + c * np.cos(a * x), np.sin(b * x) + d * np.cos(b * y)]
        return points

    def generate_aizawa(n_points, random_seed, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1, dt=0.01):
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3) * 0.1
        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                (z - b) * x - d * y, d * x + (z - b) * y,
                c + a * z - (z**3 / 3) - (x**2 + y**2) * (1 + e * z) + f * z * x**3
            ]) * dt
        return points

    def generate_thomas(n_points, random_seed, b=0.208186, dt=0.05):
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3) * 0.1
        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                np.sin(y) - b * x, np.sin(z) - b * y, np.sin(x) - b * z
            ]) * dt
        return points

    def generate_halvorsen(n_points, random_seed, a=1.89, dt=0.005):
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.array([-1.48, -1.51, 2.04])
        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                -a * x - 4 * y - 4 * z - y**2,
                -a * y - 4 * z - 4 * x - z**2,
                -a * z - 4 * x - 4 * y - x**2
            ]) * dt
        return points

    generators = {
        "Lorenz": generate_lorenz, "Clifford": generate_clifford,
        "Aizawa": generate_aizawa, "Thomas": generate_thomas, "Halvorsen": generate_halvorsen
    }
    points = generators[attractor_type.value](num_points.value, seed.value)

    fig = plt.figure(figsize=(8, 8), facecolor="black")
    if points.shape[1] == 2:
        ax = fig.add_subplot(111)
        ax.scatter(points[:, 0], points[:, 1], c=np.arange(len(points)),
                   cmap=colormap.value, s=point_size.value, alpha=0.6)
        ax.set_facecolor("black")
    else:
        ax = fig.add_subplot(111, projection="3d", facecolor="black")
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=np.arange(len(points)),
                   cmap=colormap.value, s=point_size.value, alpha=0.6)
        ax.set_facecolor("black")
    ax.axis("off")
    ax.set_title(f"{attractor_type.value} | {num_points.value:,} pts | Seed: {seed.value}",
                 color="white", fontsize=11)
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        attractor_type, num_points, seed, colormap, point_size,
        mo.md("---"),
        mo.md("""**Attractors:**
- Lorenz: 3D butterfly effect
- Clifford: 2D elegant patterns
- Aizawa: 3D spiral structure
- Thomas: 3D cyclic symmetry
- Halvorsen: 3D three-lobed""")
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


if __name__ == "__main__":
    app.run()
