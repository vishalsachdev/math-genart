import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Fourier & Lissajous - Wave Visualization")


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
        # 7. Fourier Series & Lissajous Curves

        [← Back to Index](index.html)

        ---

        Transform **waves into visual language**. Oscillating ribbons and spectral sculptures.

        ## Lissajous Curves

        Parametric curves from two perpendicular oscillations:

        ```
        x(t) = A·sin(a·t + δ)
        y(t) = B·sin(b·t)
        ```

        Where:
        - **a, b**: Frequency ratio (determines the pattern)
        - **δ**: Phase difference
        - **A, B**: Amplitudes

        The ratio a:b determines the number of lobes and symmetry!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    freq_a = mo.ui.slider(1, 10, value=3, label="Frequency A", full_width=True)
    freq_a
    return (freq_a,)


@app.cell
def _(mo):
    freq_b = mo.ui.slider(1, 10, value=4, label="Frequency B", full_width=True)
    freq_b
    return (freq_b,)


@app.cell
def _(mo):
    num_curves = mo.ui.slider(1, 30, value=12, label="Number of Curves", full_width=True)
    num_curves
    return (num_curves,)


@app.cell
def _(mo):
    phase_spread = mo.ui.slider(0.0, 2.0, value=1.0, step=0.1, label="Phase Spread (× π)", full_width=True)
    phase_spread
    return (phase_spread,)


@app.cell
def _(mo):
    colormap = mo.ui.dropdown(
        options=["twilight", "rainbow", "plasma", "viridis", "hsv", "coolwarm"],
        value="twilight",
        label="Color Map"
    )
    colormap
    return (colormap,)


@app.cell
def _(mo):
    line_width = mo.ui.slider(0.5, 3.0, value=1.5, step=0.25, label="Line Width", full_width=True)
    line_width
    return (line_width,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(colormap, freq_a, freq_b, line_width, np, num_curves, phase_spread, plt):
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")

    # Time parameter
    t = np.linspace(0, 2 * np.pi, 2000)

    # Get colormap
    cmap = plt.get_cmap(colormap.value)
    n = num_curves.value

    # Draw multiple curves with phase offset
    for i in range(n):
        # Phase offset for this curve
        phase = i * phase_spread.value * np.pi / n

        # Lissajous curve with slight frequency variation
        a = freq_a.value + i * 0.05
        b = freq_b.value + i * 0.05

        x = np.sin(a * t + phase)
        y = np.sin(b * t)

        # Color based on position in sequence
        color = cmap(i / n)

        ax.plot(x, y, color=color, linewidth=line_width.value, alpha=0.7)

    ax.set_aspect("equal")
    ax.set_xlim([-1.3, 1.3])
    ax.set_ylim([-1.3, 1.3])
    ax.axis("off")
    ax.set_title(
        f"Lissajous Curves | {freq_a.value}:{freq_b.value} | {n} curves",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return a, b, cmap, color, fig, i, n, phase, t, x, y


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Frequency Ratios

        The ratio a:b determines the pattern:

        | Ratio | Pattern |
        |-------|---------|
        | 1:1 | Ellipse or line (depending on phase) |
        | 1:2 | Figure-8 (infinity symbol) |
        | 2:3 | Pretzel shape |
        | 3:4 | Complex knot |
        | 1:1 with phase | Circle |

        **Integer ratios** create closed curves.
        **Irrational ratios** create curves that never close (fill the rectangle).

        ---

        ## Historical Context

        Lissajous figures were first studied by:
        - **Nathaniel Bowditch** (1815) - mechanical demonstration
        - **Jules Antoine Lissajous** (1857) - optical method using mirrors

        Before oscilloscopes, physicists used Lissajous figures to compare
        frequencies of tuning forks!

        ---

        ## Fourier Connection

        Any periodic signal can be decomposed into a sum of sine waves (Fourier series):

        ```
        f(t) = a₀ + Σ [aₙ·cos(n·ω·t) + bₙ·sin(n·ω·t)]
        ```

        Lissajous curves visualize the **superposition** of two such waves
        at right angles. The epicycle animation (rotating circles) shows
        how complex curves emerge from simple circular motion.

        ---

        ## Sound Visualization

        Lissajous figures appear on oscilloscopes when:
        - X-input: One audio signal
        - Y-input: Another audio signal

        The pattern reveals the **frequency relationship** between sounds -
        perfect for tuning instruments or analyzing harmonics!

        ---

        [← Voronoi](06_voronoi.html) | [Back to Index](index.html) | [Differential Growth →](08_differential_growth.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
