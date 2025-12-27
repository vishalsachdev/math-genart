import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Cellular Automata - Rule-Based Emergence")


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

        **Conway's Game of Life**: minimal rules, maximal emergence. Each cell is alive or dead.
        Rules: Live cell with 2-3 neighbors survives. Dead cell with 3 neighbors is born.
        """
    )
    return


@app.cell
def _(mo):
    seed = mo.ui.slider(1, 1000, value=42, label="Random Seed", full_width=True)
    steps = mo.ui.slider(10, 300, value=100, label="Evolution Steps", full_width=True)
    grid_size = mo.ui.slider(50, 300, value=150, label="Grid Size", full_width=True)
    density = mo.ui.slider(0.1, 0.5, value=0.3, step=0.05, label="Initial Density", full_width=True)
    colormap = mo.ui.dropdown(
        options=["hot", "plasma", "viridis", "magma", "inferno", "cividis"],
        value="hot",
        label="Color Map"
    )
    return seed, steps, grid_size, density, colormap


@app.cell
def _(mo, seed, steps, grid_size, density, colormap, convolve, np, plt):
    def run_cellular_automata(size, random_seed, num_steps, init_density):
        np.random.seed(random_seed)
        grid = np.random.choice([0, 1], size=(size, size), p=[1 - init_density, init_density])
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        for _ in range(num_steps):
            neighbors = convolve(grid, kernel, mode="constant", cval=0)
            birth = (grid == 0) & (neighbors == 3)
            survive = (grid == 1) & ((neighbors == 2) | (neighbors == 3))
            grid = (birth | survive).astype(int)
        return grid

    final_grid = run_cellular_automata(grid_size.value, seed.value, steps.value, density.value)

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")
    ax.imshow(final_grid, cmap=colormap.value, interpolation="nearest")
    ax.axis("off")
    alive_cells = np.sum(final_grid)
    total_cells = final_grid.size
    ax.set_title(f"Seed: {seed.value} | Steps: {steps.value} | Alive: {alive_cells:,}/{total_cells:,}",
                 color="white", fontsize=11)
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        seed, steps, grid_size, density, colormap,
        mo.md("---"),
        mo.md("""
**Try these:**
- Seed 42, 100 steps: Classic
- Seed 777, 200 steps: Chaotic
- High density (0.5): Dense patterns
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
