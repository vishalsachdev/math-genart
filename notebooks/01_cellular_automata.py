import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Cellular Automata - Rule-Based Emergence")


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
        # 1. Cellular Automata - Rule-Based Emergence

        [← Back to Index](index.html)

        ---

        **Conway's Game of Life** demonstrates how minimal rules generate maximal emergence:
        self-replication, oscillators, gliders, and complex organic patterns from simple initial conditions.

        ## The Rules

        Each cell is either **alive** (1) or **dead** (0). At each step:
        - **Survival**: A live cell with 2-3 neighbors survives
        - **Birth**: A dead cell with exactly 3 neighbors becomes alive
        - **Death**: All other cells die or stay dead

        These simple rules create astonishing complexity - the system is **Turing complete**!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    seed = mo.ui.slider(1, 1000, value=42, label="Random Seed", full_width=True)
    seed
    return (seed,)


@app.cell
def _(mo):
    steps = mo.ui.slider(10, 300, value=100, label="Evolution Steps", full_width=True)
    steps
    return (steps,)


@app.cell
def _(mo):
    grid_size = mo.ui.slider(50, 300, value=150, label="Grid Size", full_width=True)
    grid_size
    return (grid_size,)


@app.cell
def _(mo):
    density = mo.ui.slider(0.1, 0.5, value=0.3, step=0.05, label="Initial Density", full_width=True)
    density
    return (density,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["hot", "plasma", "viridis", "magma", "inferno", "cividis"],
        value="hot",
        label="Color Map"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(colormap, convolve, density, grid_size, np, plt, seed, steps):
    def run_cellular_automata(size, random_seed, num_steps, init_density):
        """
        Run Conway's Game of Life simulation.

        Args:
            size: Grid dimension (size x size)
            random_seed: Seed for reproducible randomness
            num_steps: Number of evolution steps
            init_density: Probability of cell being alive initially

        Returns:
            Final grid state after evolution
        """
        np.random.seed(random_seed)

        # Initialize grid with random state
        grid = np.random.choice(
            [0, 1],
            size=(size, size),
            p=[1 - init_density, init_density]
        )

        # Moore neighborhood kernel (8 neighbors)
        kernel = np.array([[1, 1, 1],
                          [1, 0, 1],
                          [1, 1, 1]])

        # Evolution loop
        for _ in range(num_steps):
            # Count neighbors using convolution
            neighbors = convolve(grid, kernel, mode="constant", cval=0)

            # Apply Game of Life rules
            birth = (grid == 0) & (neighbors == 3)
            survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
            grid = (birth | survive).astype(int)

        return grid

    # Run simulation
    final_grid = run_cellular_automata(
        grid_size.value,
        seed.value,
        steps.value,
        density.value
    )

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")
    ax.imshow(final_grid, cmap=colormap.value, interpolation="nearest")
    ax.axis("off")

    # Statistics
    alive_cells = np.sum(final_grid)
    total_cells = final_grid.size
    alive_pct = 100 * alive_cells / total_cells

    ax.set_title(
        f"Cellular Automata | Seed: {seed.value} | Steps: {steps.value}\n"
        f"Alive: {alive_cells:,} / {total_cells:,} ({alive_pct:.1f}%)",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return alive_cells, alive_pct, fig, final_grid, run_cellular_automata, total_cells


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## How It Works

        The **Game of Life** uses a simple cellular automaton where each cell's next state
        depends only on its current state and the count of its 8 neighbors.

        **Key patterns to discover:**
        - **Still lifes**: Stable patterns (blocks, beehives)
        - **Oscillators**: Patterns that cycle (blinkers, toads)
        - **Spaceships**: Patterns that move (gliders)
        - **Methuselahs**: Small patterns that evolve for many generations

        **Try these seeds** for interesting patterns:
        - Seed 42, 100 steps: Classic evolution
        - Seed 777, 200 steps: More chaotic
        - Seed 123, 50 steps: Early-stage patterns

        ---

        ## Mathematical Foundation

        The cellular automaton is defined by:
        - **State space**: S = {0, 1}
        - **Neighborhood**: Moore (8 adjacent cells)
        - **Transition function**: f(state, neighbors) based on birth/survival rules

        This simple system exhibits **emergent complexity** - behavior that cannot be
        predicted without running the simulation.

        ---

        [← Back to Index](index.html) | [Next: L-Systems →](02_lsystems.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
