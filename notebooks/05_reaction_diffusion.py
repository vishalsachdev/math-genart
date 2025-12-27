import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Reaction-Diffusion - Chemical Art")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.ndimage import convolve
    plt.style.use('dark_background')
    return convolve, np, plt


@app.cell
def _(mo):
    mo.md(
        """
        # 5. Reaction-Diffusion - Chemical Art

        [← Back to Index](index.html)

        ---

        **Gray-Scott model** simulates chemical pattern formation - two chemicals diffuse
        and react, creating animal skin patterns, coral reefs, and organic textures.

        ## The Equations

        Two chemicals U and V with concentrations that evolve:

        ```
        ∂U/∂t = Du·∇²U - U·V² + F·(1-U)
        ∂V/∂t = Dv·∇²V + U·V² - (F+k)·V
        ```

        Where:
        - **Du, Dv**: Diffusion rates (U diffuses faster)
        - **F**: Feed rate (replenishes U)
        - **k**: Kill rate (removes V)
        - **∇²**: Laplacian (spatial diffusion)

        Different F and k values create radically different patterns!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    preset = mo.ui.dropdown(
        options={
            "Spots": (0.060, 0.062),
            "Stripes": (0.035, 0.065),
            "Maze": (0.029, 0.057),
            "Waves": (0.014, 0.054),
            "Coral": (0.055, 0.062),
            "Mitosis": (0.028, 0.062),
            "Holes": (0.039, 0.058),
        },
        value="Spots",
        label="Pattern Type"
    )
    preset
    return (preset,)


@app.cell
def _(mo):
    steps = mo.ui.slider(1000, 15000, value=5000, step=500, label="Simulation Steps", full_width=True)
    steps
    return (steps,)


@app.cell
def _(mo):
    grid_size = mo.ui.slider(100, 300, value=200, step=25, label="Grid Size", full_width=True)
    grid_size
    return (grid_size,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["viridis", "plasma", "magma", "inferno", "cividis", "twilight", "ocean"],
        value="viridis",
        label="Color Map"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(colormap, convolve, grid_size, np, plt, preset, steps):
    def reaction_diffusion(size, Du, Dv, F, k, num_steps):
        """
        Run Gray-Scott reaction-diffusion simulation.

        Args:
            size: Grid dimension
            Du, Dv: Diffusion coefficients for U and V
            F: Feed rate
            k: Kill rate
            num_steps: Number of simulation steps

        Returns:
            V concentration grid (shows the pattern)
        """
        # Initialize concentrations
        U = np.ones((size, size))
        V = np.zeros((size, size))

        # Add perturbation in center (seed the reaction)
        n = size // 2
        r = size // 10
        U[n-r:n+r, n-r:n+r] = 0.50
        V[n-r:n+r, n-r:n+r] = 0.25

        # Add some random noise
        np.random.seed(42)
        V += np.random.rand(size, size) * 0.05

        # Laplacian kernel (9-point stencil for better isotropy)
        laplacian = np.array([
            [0.05, 0.2, 0.05],
            [0.2, -1.0, 0.2],
            [0.05, 0.2, 0.05]
        ])

        # Simulation loop
        for _ in range(num_steps):
            # Compute Laplacians
            Lu = convolve(U, laplacian, mode="wrap")
            Lv = convolve(V, laplacian, mode="wrap")

            # Reaction term
            uvv = U * V * V

            # Update concentrations
            U += Du * Lu - uvv + F * (1 - U)
            V += Dv * Lv + uvv - (F + k) * V

        return V

    # Get parameters from preset
    F, k = preset.value

    # Run simulation
    result = reaction_diffusion(
        grid_size.value,
        Du=0.16,
        Dv=0.08,
        F=F,
        k=k,
        num_steps=steps.value
    )

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")
    ax.imshow(result, cmap=colormap.value, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(
        f"Reaction-Diffusion | F={F}, k={k} | Steps: {steps.value}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return F, fig, k, reaction_diffusion, result


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Pattern Parameter Space

        The F-k parameter space contains distinct regions:

        | Pattern | F | k | Description |
        |---------|---|---|-------------|
        | Spots | 0.060 | 0.062 | Isolated dots |
        | Stripes | 0.035 | 0.065 | Labyrinthine |
        | Maze | 0.029 | 0.057 | Interconnected corridors |
        | Waves | 0.014 | 0.054 | Propagating waves |
        | Coral | 0.055 | 0.062 | Branching structures |
        | Mitosis | 0.028 | 0.062 | Cell-like division |

        ---

        ## Real-World Patterns

        This system models actual biological patterns:
        - **Zebra stripes** and **leopard spots**
        - **Coral reef** structures
        - **Bacterial colonies**
        - **Chemical oscillations** (Belousov-Zhabotinsky)

        Alan Turing proposed reaction-diffusion in 1952 as a mechanism for
        **morphogenesis** - how organisms develop patterns during growth.

        ---

        ## The Chemistry

        Think of U as a "food" chemical and V as a "catalyst":
        - U diffuses and is consumed by V
        - V catalyzes its own production (autocatalysis)
        - V decays naturally
        - Fresh U is continuously fed in

        The competition between diffusion and reaction creates patterns!

        ---

        [← Fractals](04_fractals.html) | [Back to Index](index.html) | [Voronoi →](06_voronoi.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
