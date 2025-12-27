import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Fractals - Infinite Detail, Finite Rules")


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

        ---

        **Mandelbrot** and **Julia sets** reveal infinite complexity from a simple iteration:

        ### z_{n+1} = z_n² + c

        Every zoom level reveals new structures. The boundary has infinite length but
        encloses a finite area. Perfect for cosmic terrains and psychedelic worlds.

        ## Key Concepts

        - **Mandelbrot Set**: For each point c in the complex plane, start with z₀ = 0
          and iterate. If |z| stays bounded, c is IN the set (black).
        - **Julia Set**: Fix c, vary the starting point z₀. Each c creates a different Julia set.
        - **Escape time**: Points outside the set "escape" to infinity. Color = how fast they escape.
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    fractal_type = mo.ui.dropdown(
        options=["Mandelbrot", "Julia", "Burning Ship", "Tricorn"],
        value="Mandelbrot",
        label="Fractal Type"
    )
    fractal_type
    return (fractal_type,)


@app.cell
def _(mo):
    max_iter = mo.ui.slider(50, 500, value=200, step=25, label="Max Iterations (detail)", full_width=True)
    max_iter
    return (max_iter,)


@app.cell
def _(mo):
    zoom = mo.ui.slider(1, 500, value=1, label="Zoom Level", full_width=True)
    zoom
    return (zoom,)


@app.cell
def _(mo):
    center_x = mo.ui.slider(-2.0, 1.0, value=-0.5, step=0.1, label="Center X", full_width=True)
    center_x
    return (center_x,)


@app.cell
def _(mo):
    center_y = mo.ui.slider(-1.5, 1.5, value=0.0, step=0.1, label="Center Y", full_width=True)
    center_y
    return (center_y,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["hot", "twilight_shifted", "plasma", "magma", "inferno", "viridis", "cubehelix"],
        value="hot",
        label="Color Map"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    resolution = mo.ui.slider(400, 1000, value=600, step=100, label="Resolution", full_width=True)
    resolution
    return (resolution,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(center_x, center_y, colormap, fractal_type, max_iter, np, plt, resolution, zoom):
    def compute_mandelbrot(width, height, xmin, xmax, ymin, ymax, max_iterations):
        """
        Compute Mandelbrot set escape times.

        For each c in the complex plane, iterate z = z² + c starting from z = 0.
        Return the iteration count when |z| > 2 (escape), or max_iterations if bounded.
        """
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
        """
        Compute Julia set for fixed c.

        For each starting point z₀, iterate z = z² + c.
        Different c values create different Julia sets.
        """
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
        """
        Burning Ship fractal - take absolute values before squaring.

        z_{n+1} = (|Re(z_n)| + i|Im(z_n)|)² + c
        """
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
        """
        Tricorn (Mandelbar) fractal - use complex conjugate.

        z_{n+1} = conj(z_n)² + c
        """
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

    # Calculate view bounds
    span = 2.5 / zoom.value
    xmin, xmax = center_x.value - span, center_x.value + span
    ymin, ymax = center_y.value - span, center_y.value + span

    # Compute fractal
    compute_funcs = {
        "Mandelbrot": compute_mandelbrot,
        "Julia": compute_julia,
        "Burning Ship": compute_burning_ship,
        "Tricorn": compute_tricorn
    }

    fractal_data = compute_funcs[fractal_type.value](
        resolution.value, resolution.value,
        xmin, xmax, ymin, ymax,
        max_iter.value
    )

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")
    ax.imshow(fractal_data, cmap=colormap.value, interpolation="bilinear",
              extent=[xmin, xmax, ymin, ymax], origin="lower")
    ax.axis("off")
    ax.set_title(
        f"{fractal_type.value} | Zoom: {zoom.value}x | Iterations: {max_iter.value}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return (
        compute_burning_ship,
        compute_funcs,
        compute_julia,
        compute_mandelbrot,
        compute_tricorn,
        fig,
        fractal_data,
        span,
        xmax,
        xmin,
        ymax,
        ymin,
    )


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Interesting Locations to Explore

        | Name | Center X | Center Y | Zoom | Description |
        |------|----------|----------|------|-------------|
        | Overview | -0.5 | 0 | 1 | Full Mandelbrot set |
        | Seahorse Valley | -0.75 | 0.1 | 50 | Intricate spiral patterns |
        | Elephant Valley | 0.3 | 0.0 | 50 | Trunk-like structures |
        | Mini Mandelbrot | -1.75 | 0.0 | 100 | Small copy of the whole set |
        | Spiral | -0.761574 | -0.0847596 | 200 | Beautiful spiral |

        ---

        ## The Mathematics

        **Mandelbrot iteration**:
        ```
        z₀ = 0
        z_{n+1} = z_n² + c
        ```

        A point c is in the Mandelbrot set if |z_n| remains bounded as n → ∞.
        In practice, if |z| > 2, it will escape to infinity.

        **Fractal dimension**: The Mandelbrot set boundary has dimension 2!
        This means it's more "wiggly" than any normal curve.

        ---

        ## Fractal Variants

        - **Julia sets**: Fix c, vary starting z₀. Each c creates a unique pattern.
        - **Burning Ship**: Takes |Re| and |Im| before squaring - creates ship-like shape
        - **Tricorn**: Uses complex conjugate - creates 3-fold symmetry

        ---

        [← Strange Attractors](03_strange_attractors.html) | [Back to Index](index.html) | [Reaction-Diffusion →](05_reaction_diffusion.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
