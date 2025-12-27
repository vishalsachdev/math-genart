import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Reaction-Diffusion - Chemical Art")


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

        **Gray-Scott model**: Two chemicals diffuse and react, creating animal skin patterns,
        coral reefs, and organic textures. Different F and k values = different patterns.
        """
    )
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
    steps = mo.ui.slider(1000, 15000, value=5000, step=500, label="Steps", full_width=True)
    grid_size = mo.ui.slider(100, 300, value=200, step=25, label="Grid Size", full_width=True)
    colormap = mo.ui.dropdown(
        options=["viridis", "plasma", "magma", "inferno", "cividis", "twilight", "ocean"],
        value="viridis",
        label="Color Map"
    )
    return colormap, grid_size, preset, steps


@app.cell
def _(colormap, convolve, grid_size, mo, np, plt, preset, steps):
    def reaction_diffusion(size, Du, Dv, F, k, num_steps):
        U = np.ones((size, size))
        V = np.zeros((size, size))
        n = size // 2
        r = size // 10
        U[n-r:n+r, n-r:n+r] = 0.50
        V[n-r:n+r, n-r:n+r] = 0.25
        np.random.seed(42)
        V += np.random.rand(size, size) * 0.05

        laplacian = np.array([[0.05, 0.2, 0.05], [0.2, -1.0, 0.2], [0.05, 0.2, 0.05]])

        for _ in range(num_steps):
            Lu = convolve(U, laplacian, mode="wrap")
            Lv = convolve(V, laplacian, mode="wrap")
            uvv = U * V * V
            U += Du * Lu - uvv + F * (1 - U)
            V += Dv * Lv + uvv - (F + k) * V
        return V

    F, k = preset.value
    result = reaction_diffusion(grid_size.value, Du=0.16, Dv=0.08, F=F, k=k, num_steps=steps.value)

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")
    ax.imshow(result, cmap=colormap.value, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"F={F}, k={k} | Steps: {steps.value}", color="white", fontsize=11)
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        preset, steps, grid_size, colormap,
        mo.md("---"),
        mo.md("""**Patterns:**
- Spots: F=0.060, k=0.062
- Stripes: F=0.035, k=0.065
- Maze: F=0.029, k=0.057
- Coral: F=0.055, k=0.062""")
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


if __name__ == "__main__":
    app.run()
