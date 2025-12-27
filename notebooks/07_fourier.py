import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Fourier & Lissajous - Wave Visualization")


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

        **Waves as visual language.** Lissajous curves arise from two perpendicular oscillations:
        `x(t) = sin(a·t + δ)`, `y(t) = sin(b·t)`. The ratio a:b determines the pattern.
        """
    )
    return


@app.cell
def _(mo):
    freq_a = mo.ui.slider(1, 10, value=3, label="Frequency A", full_width=True)
    freq_b = mo.ui.slider(1, 10, value=4, label="Frequency B", full_width=True)
    num_curves = mo.ui.slider(1, 30, value=12, label="Number of Curves", full_width=True)
    phase_spread = mo.ui.slider(0.0, 2.0, value=1.0, step=0.1, label="Phase Spread (× π)", full_width=True)
    colormap = mo.ui.dropdown(
        options=["twilight", "rainbow", "plasma", "viridis", "hsv", "coolwarm"],
        value="twilight",
        label="Color Map"
    )
    line_width = mo.ui.slider(0.5, 3.0, value=1.5, step=0.25, label="Line Width", full_width=True)
    return freq_a, freq_b, num_curves, phase_spread, colormap, line_width


@app.cell
def _(mo, freq_a, freq_b, num_curves, phase_spread, colormap, line_width, np, plt):
    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

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

    controls = mo.vstack([
        mo.md("### Controls"),
        freq_a, freq_b, num_curves, phase_spread, colormap, line_width,
        mo.md("---"),
        mo.md("""
**Frequency Ratios:**
- 1:1 → Ellipse/line
- 1:2 → Figure-8
- 2:3 → Pretzel shape
- 3:4 → Complex knot

**Tips:** Integer ratios create closed curves. Try high phase spread for ribbon effects.
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
