import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="L-Systems - Organic Growth")


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
        # 2. L-Systems - Formal Grammars → Organic Growth

        [← Back to Index](index.html)

        **Lindenmayer Systems** generate organic, self-similar structures through string rewriting.
        Commands: `F`/`G` = forward, `+`/`-` = turn, `[`/`]` = branch.
        """
    )
    return


@app.cell
def _(mo):
    preset = mo.ui.dropdown(
        options={
            "Plant": ("X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, 25),
            "Tree": ("F", {"F": "FF+[+F-F-F]-[-F+F+F]"}, 22.5),
            "Bush": ("F", {"F": "F[+F]F[-F]F"}, 25.7),
            "Sierpinski": ("F-G-G", {"F": "F-G+F+G-F", "G": "GG"}, 120),
            "Koch Curve": ("F", {"F": "F+F-F-F+F"}, 90),
            "Dragon Curve": ("FX", {"X": "X+YF+", "Y": "-FX-Y"}, 90),
            "Fern": ("X", {"X": "F+[[X]-X]-F[-FX]+X", "F": "FF"}, 22.5),
            "Seaweed": ("F", {"F": "FF-[-F+F+F]+[+F-F-F]"}, 22),
        },
        value="Plant",
        label="Preset Pattern"
    )
    iterations = mo.ui.slider(1, 7, value=5, label="Iterations", full_width=True)
    step_length = mo.ui.slider(1, 10, value=4, label="Step Length", full_width=True)
    line_color = mo.ui.dropdown(
        options=["green", "lime", "cyan", "white", "yellow", "magenta"],
        value="lime",
        label="Line Color"
    )
    line_width = mo.ui.slider(0.3, 2.0, value=0.5, step=0.1, label="Line Width", full_width=True)
    return iterations, line_color, line_width, preset, step_length


@app.cell
def _(iterations, line_color, line_width, mo, np, plt, preset, step_length):
    def generate_lsystem_string(axiom, rules, num_iterations):
        current = axiom
        for _ in range(num_iterations):
            next_string = ""
            for char in current:
                next_string += rules.get(char, char)
            current = next_string
        return current

    def draw_lsystem(ax, string, angle_deg, step_len, color, lw):
        x, y = 0, 0
        angle = 90
        stack = []
        lines_x, lines_y = [], []

        for cmd in string:
            if cmd in "FG":
                x_new = x + step_len * np.cos(np.radians(angle))
                y_new = y + step_len * np.sin(np.radians(angle))
                lines_x.extend([x, x_new, None])
                lines_y.extend([y, y_new, None])
                x, y = x_new, y_new
            elif cmd == "+":
                angle -= angle_deg
            elif cmd == "-":
                angle += angle_deg
            elif cmd == "[":
                stack.append((x, y, angle))
            elif cmd == "]":
                if stack:
                    x, y, angle = stack.pop()

        ax.plot(lines_x, lines_y, color=color, linewidth=lw, alpha=0.8)

    axiom, rules, angle = preset.value
    lsys_string = generate_lsystem_string(axiom, rules, iterations.value)

    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")
    ax.set_aspect("equal")
    ax.axis("off")
    draw_lsystem(ax, lsys_string, angle, step_length.value, line_color.value, line_width.value)
    ax.set_title(f"Iterations: {iterations.value} | Commands: {len(lsys_string):,}",
                 color="white", fontsize=11)
    plt.tight_layout()

    axiom_display, rules_display, angle_display = preset.value
    rules_str = ", ".join([f"{k}→{v}" for k, v in rules_display.items()])

    controls = mo.vstack([
        mo.md("### Controls"),
        preset, iterations, step_length, line_color, line_width,
        mo.md("---"),
        mo.md(f"**Axiom:** `{axiom_display}`"),
        mo.md(f"**Angle:** {angle_display}°"),
        mo.md(f"**Rules:** {rules_str}"),
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


if __name__ == "__main__":
    app.run()
