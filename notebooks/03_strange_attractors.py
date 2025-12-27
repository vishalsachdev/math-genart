import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Strange Attractors - Chaos with Memory")


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

        ---

        **Strange attractors** are geometric structures that chaotic systems evolve toward.
        They produce deterministic but unpredictable, flowing signature shapes.

        ## The Paradox

        These systems are:
        - **Deterministic**: Same initial conditions → same trajectory
        - **Chaotic**: Tiny changes in initial conditions → vastly different outcomes
        - **Bounded**: Despite chaos, trajectories stay within a finite region
        - **Fractal**: The attractor has non-integer dimension

        Parameter sets define rarity layers; slight variations create entirely different structures.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    attractor_type = mo.ui.dropdown(
        options=["Lorenz", "Clifford", "Aizawa", "Thomas", "Halvorsen"],
        value="Clifford",
        label="Attractor Type"
    )
    attractor_type
    return (attractor_type,)


@app.cell
def _(mo):
    num_points = mo.ui.slider(10000, 300000, value=100000, step=10000, label="Number of Points", full_width=True)
    num_points
    return (num_points,)


@app.cell
def _(mo):
    seed = mo.ui.slider(1, 100, value=42, label="Random Seed", full_width=True)
    seed
    return (seed,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["plasma", "viridis", "magma", "inferno", "cividis", "twilight", "turbo"],
        value="plasma",
        label="Color Map"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    point_size = mo.ui.slider(0.01, 0.5, value=0.1, step=0.01, label="Point Size", full_width=True)
    point_size
    return (point_size,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(attractor_type, colormap, np, num_points, plt, point_size, seed):
    def generate_lorenz(n_points, random_seed, sigma=10, rho=28, beta=8/3, dt=0.01):
        """
        Lorenz attractor - the famous 'butterfly effect' system.

        dx/dt = σ(y - x)
        dy/dt = x(ρ - z) - y
        dz/dt = xy - βz
        """
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3)

        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                sigma * (y - x),
                x * (rho - z) - y,
                x * y - beta * z
            ]) * dt

        return points

    def generate_clifford(n_points, random_seed, a=-1.4, b=1.6, c=1.0, d=0.7):
        """
        Clifford attractor - beautiful 2D iterative map.

        x_{n+1} = sin(a·y_n) + c·cos(a·x_n)
        y_{n+1} = sin(b·x_n) + d·cos(b·y_n)
        """
        np.random.seed(random_seed)
        points = np.zeros((n_points, 2))
        points[0] = np.random.randn(2) * 0.1

        for i in range(1, n_points):
            x, y = points[i-1]
            points[i] = [
                np.sin(a * y) + c * np.cos(a * x),
                np.sin(b * x) + d * np.cos(b * y)
            ]

        return points

    def generate_aizawa(n_points, random_seed, a=0.95, b=0.7, c=0.6, d=3.5, e=0.25, f=0.1, dt=0.01):
        """
        Aizawa attractor - elegant 3D spiral structure.
        """
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3) * 0.1

        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                (z - b) * x - d * y,
                d * x + (z - b) * y,
                c + a * z - (z**3 / 3) - (x**2 + y**2) * (1 + e * z) + f * z * x**3
            ]) * dt

        return points

    def generate_thomas(n_points, random_seed, b=0.208186, dt=0.05):
        """
        Thomas attractor - cyclically symmetric system.
        """
        np.random.seed(random_seed)
        points = np.zeros((n_points, 3))
        points[0] = np.random.randn(3) * 0.1

        for i in range(1, n_points):
            x, y, z = points[i-1]
            points[i] = points[i-1] + np.array([
                np.sin(y) - b * x,
                np.sin(z) - b * y,
                np.sin(x) - b * z
            ]) * dt

        return points

    def generate_halvorsen(n_points, random_seed, a=1.89, dt=0.005):
        """
        Halvorsen attractor - cyclic 3D attractor.
        """
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

    # Generate attractor points
    generators = {
        "Lorenz": generate_lorenz,
        "Clifford": generate_clifford,
        "Aizawa": generate_aizawa,
        "Thomas": generate_thomas,
        "Halvorsen": generate_halvorsen
    }

    points = generators[attractor_type.value](num_points.value, seed.value)

    # Create visualization
    fig = plt.figure(figsize=(10, 10), facecolor="black")

    if points.shape[1] == 2:
        # 2D attractor
        ax = fig.add_subplot(111)
        ax.scatter(
            points[:, 0], points[:, 1],
            c=np.arange(len(points)),
            cmap=colormap.value,
            s=point_size.value,
            alpha=0.6
        )
        ax.set_facecolor("black")
    else:
        # 3D attractor
        ax = fig.add_subplot(111, projection="3d", facecolor="black")
        ax.scatter(
            points[:, 0], points[:, 1], points[:, 2],
            c=np.arange(len(points)),
            cmap=colormap.value,
            s=point_size.value,
            alpha=0.6
        )
        ax.set_facecolor("black")

    ax.axis("off")
    ax.set_title(
        f"{attractor_type.value} Attractor | {num_points.value:,} points | Seed: {seed.value}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return (
        fig,
        generate_aizawa,
        generate_clifford,
        generate_halvorsen,
        generate_lorenz,
        generate_thomas,
        generators,
        points,
    )


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Attractor Types

        | Attractor | Dimension | Key Feature |
        |-----------|-----------|-------------|
        | **Lorenz** | 3D | The original "butterfly effect" attractor. Discovered in 1963 by meteorologist Edward Lorenz. |
        | **Clifford** | 2D | Elegant symmetric patterns. Parameters a, b, c, d create infinite variations. |
        | **Aizawa** | 3D | Spiral structure with complex internal dynamics. |
        | **Thomas** | 3D | Cyclically symmetric - x, y, z are interchangeable. |
        | **Halvorsen** | 3D | Three-lobed cyclic attractor. |

        ---

        ## The Mathematics

        **Lorenz system** (1963):
        ```
        dx/dt = σ(y - x)
        dy/dt = x(ρ - z) - y
        dz/dt = xy - βz
        ```

        **Clifford attractor**:
        ```
        x_{n+1} = sin(a·y_n) + c·cos(a·x_n)
        y_{n+1} = sin(b·x_n) + d·cos(b·y_n)
        ```

        ---

        ## Sensitivity to Initial Conditions

        The "butterfly effect" means that two trajectories starting 0.0001 apart
        will eventually diverge completely. Yet all trajectories are bounded
        within the attractor's shape - **chaos within structure**.

        ---

        [← L-Systems](02_lsystems.html) | [Back to Index](index.html) | [Fractals →](04_fractals.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
