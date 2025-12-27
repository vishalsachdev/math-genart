import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Fractals - Infinite Detail, Finite Rules")


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
        # 4. Fractals - Infinite Detail, Finite Rules

        [← Back to Index](index.html)

        **Mandelbrot** and **Julia sets**: z_{n+1} = z_n² + c.
        Every zoom reveals new structures. Infinite complexity from simple iteration.
        """
    )
    return


@app.cell
def _(mo):
    fractal_type = mo.ui.dropdown(
        options=["Mandelbrot", "Julia", "Burning Ship", "Tricorn"],
        value="Mandelbrot",
        label="Fractal Type"
    )
    max_iter = mo.ui.slider(50, 500, value=200, step=25, label="Iterations", full_width=True)
    zoom = mo.ui.slider(1, 500, value=1, label="Zoom", full_width=True)
    center_x = mo.ui.slider(-2.0, 1.0, value=-0.5, step=0.1, label="Center X", full_width=True)
    center_y = mo.ui.slider(-1.5, 1.5, value=0.0, step=0.1, label="Center Y", full_width=True)
    colormap = mo.ui.dropdown(
        options=["hot", "twilight_shifted", "plasma", "magma", "inferno", "viridis", "cubehelix"],
        value="hot",
        label="Color Map"
    )
    resolution = mo.ui.slider(400, 1000, value=600, step=100, label="Resolution", full_width=True)
    return center_x, center_y, colormap, fractal_type, max_iter, resolution, zoom


@app.cell
def _(center_x, center_y, colormap, fractal_type, max_iter, mo, np, plt, resolution, zoom):
    def compute_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iterations):
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        for i in range(max_iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + C[mask]
            M[mask] = i
        return M

    def compute_julia(width, height, xmin, xmax, ymin, ymax, max_iterations, c=-0.7+0.27015j):
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        Z = X + 1j * Y
        M = np.zeros(Z.shape)
        for i in range(max_iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = Z[mask]**2 + c
            M[mask] = i
        return M

    def compute_burning_ship(width, height, xmin, xmax, ymin, ymax, max_iterations):
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        for i in range(max_iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = (np.abs(Z[mask].real) + 1j * np.abs(Z[mask].imag))**2 + C[mask]
            M[mask] = i
        return M

    def compute_tricorn(width, height, xmin, xmax, ymin, ymax, max_iterations):
        x = np.linspace(xmin, xmax, width)
        y = np.linspace(ymin, ymax, height)
        X, Y = np.meshgrid(x, y)
        C = X + 1j * Y
        Z = np.zeros_like(C)
        M = np.zeros(C.shape)
        for i in range(max_iterations):
            mask = np.abs(Z) <= 2
            Z[mask] = np.conj(Z[mask])**2 + C[mask]
            M[mask] = i
        return M

    span = 2.5 / zoom.value
    xmin, xmax = center_x.value - span, center_x.value + span
    ymin, ymax = center_y.value - span, center_y.value + span

    compute_funcs = {
        "Mandelbrot": compute_mandelbrot, "Julia": compute_julia,
        "Burning Ship": compute_burning_ship, "Tricorn": compute_tricorn
    }
    fractal_data = compute_funcs[fractal_type.value](
        resolution.value, resolution.value, xmin, xmax, ymin, ymax, max_iter.value
    )

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")
    ax.imshow(fractal_data, cmap=colormap.value, interpolation="bilinear",
              extent=[xmin, xmax, ymin, ymax], origin="lower")
    ax.axis("off")
    ax.set_title(f"{fractal_type.value} | Zoom: {zoom.value}x | Iter: {max_iter.value}",
                 color="white", fontsize=11)
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        fractal_type, max_iter, zoom, center_x, center_y, colormap, resolution,
        mo.md("---"),
        mo.md("""**Locations:**
- Seahorse Valley: X=-0.75, Y=0.1, Zoom=50
- Mini Mandelbrot: X=-1.75, Y=0, Zoom=100""")
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


if __name__ == "__main__":
    app.run()
