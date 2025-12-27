import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Phase Portraits - Complex Domain Coloring")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import hsv_to_rgb
    plt.style.use('dark_background')
    return hsv_to_rgb, np, plt


@app.cell
def _(mo):
    mo.md(
        """
        # 11. Complex Numbers & Phase Portraits
        [← Back to Index](index.html)

        **Domain coloring** visualizes complex functions by mapping phase to hue and magnitude to brightness.
        This reveals zeros, poles, and singularities as flowing color patterns.
        """
    )
    return


@app.cell
def _(mo):
    func_choice = mo.ui.dropdown(
        options={
            "z² - 1 (two zeros)": "z**2 - 1",
            "z³ - 1 (three zeros)": "z**3 - 1",
            "z⁴ - 1 (four zeros)": "z**4 - 1",
            "sin(z)": "np.sin(z)",
            "cos(z)": "np.cos(z)",
            "1/z (simple pole)": "1/z",
            "(z² - 1)/(z² + 1)": "(z**2 - 1)/(z**2 + 1)",
            "exp(z)": "np.exp(z)",
            "z·exp(1/z)": "z * np.exp(1/z)",
            "tan(z)": "np.tan(z)",
        },
        value="z² - 1 (two zeros)",
        label="Function f(z)"
    )
    resolution = mo.ui.slider(200, 800, value=500, step=50, label="Resolution", full_width=True)
    view_range = mo.ui.slider(1.0, 5.0, value=2.5, step=0.5, label="View Range", full_width=True)
    brightness_mode = mo.ui.dropdown(
        options=["Magnitude", "Constant", "Log magnitude"],
        value="Magnitude",
        label="Brightness Mode"
    )
    return func_choice, resolution, view_range, brightness_mode


@app.cell
def _(mo, func_choice, resolution, view_range, brightness_mode, hsv_to_rgb, np, plt):
    def domain_coloring(func_str, res, vrange, brightness):
        """
        Create domain coloring visualization of a complex function.

        Args:
            func_str: String representation of function (in terms of z)
            res: Resolution (pixels)
            vrange: View range (-vrange to vrange on both axes)
            brightness: How to map magnitude to brightness

        Returns:
            RGB image array
        """
        # Create complex grid
        x = np.linspace(-vrange, vrange, res)
        y = np.linspace(-vrange, vrange, res)
        X, Y = np.meshgrid(x, y)
        z = X + 1j * Y

        # Evaluate function (handle division by zero)
        with np.errstate(divide='ignore', invalid='ignore'):
            w = eval(func_str)

        # Get phase and magnitude
        phase = np.angle(w)  # -π to π
        magnitude = np.abs(w)

        # Map phase to hue (0 to 1)
        hue = (phase + np.pi) / (2 * np.pi)

        # Saturation
        saturation = np.ones_like(hue) * 0.9

        # Value/brightness based on mode
        if brightness == "Magnitude":
            # Compress magnitude with arctan
            value = 2 * np.arctan(magnitude) / np.pi
        elif brightness == "Log magnitude":
            # Log scale with oscillation to show contours
            value = 0.5 + 0.5 * np.sin(np.log(magnitude + 0.001) * 2)
        else:
            # Constant brightness
            value = np.ones_like(hue) * 0.8

        # Handle infinities and NaNs
        value = np.nan_to_num(value, nan=0, posinf=1, neginf=0)
        value = np.clip(value, 0, 1)

        # Create HSV image and convert to RGB
        hsv = np.stack([hue, saturation, value], axis=-1)
        rgb = hsv_to_rgb(hsv)

        return rgb

    # Generate domain coloring
    func_str = func_choice.value
    rgb_img = domain_coloring(
        func_str,
        resolution.value,
        view_range.value,
        brightness_mode.value
    )

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")
    extent = [-view_range.value, view_range.value, -view_range.value, view_range.value]
    ax.imshow(rgb_img, extent=extent, origin="lower")
    ax.axhline(0, color="white", linewidth=0.5, alpha=0.3)
    ax.axvline(0, color="white", linewidth=0.5, alpha=0.3)
    ax.axis("off")

    # Get display name
    display_name = func_choice.options[func_choice.value] if hasattr(func_choice, 'options') else func_str
    ax.set_title(
        f"Phase Portrait | f(z) = {display_name}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        func_choice, resolution, view_range, brightness_mode,
        mo.md("---"),
        mo.md("""
**Color wheel:**
- Red: Positive real (phase = 0)
- Cyan: Negative real (phase = π)
- Yellow-green: Positive imaginary

**Features:**
- Zeros: All colors meet at a point
- Poles: Brightness changes rapidly
- Try Log magnitude for contours
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
