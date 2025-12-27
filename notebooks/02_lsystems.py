import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="L-Systems - Organic Growth")


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

        ---

        **Lindenmayer Systems** generate organic, self-similar structures through string rewriting.
        Invented by botanist Aristid Lindenmayer in 1968 to model plant growth.

        ## How It Works

        1. Start with an **axiom** (initial string)
        2. Apply **production rules** to replace symbols
        3. Interpret the final string as **turtle graphics** commands

        **Commands:**
        - `F` or `G`: Move forward and draw
        - `+`: Turn right by angle
        - `-`: Turn left by angle
        - `[`: Save position (push to stack)
        - `]`: Restore position (pop from stack)

        The branching (`[` and `]`) creates tree-like structures!
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
    preset
    return (preset,)


@app.cell
def _(mo):
    iterations = mo.ui.slider(1, 7, value=5, label="Iterations (depth)", full_width=True)
    iterations
    return (iterations,)


@app.cell
def _(mo):
    step_length = mo.ui.slider(1, 10, value=4, label="Step Length", full_width=True)
    step_length
    return (step_length,)


@app.cell
def _(mo):
    line_color = mo.ui.dropdown(
        options=["green", "lime", "cyan", "white", "yellow", "magenta"],
        value="lime",
        label="Line Color"
    )
    line_color
    return (line_color,)


@app.cell
def _(mo):
    line_width = mo.ui.slider(0.3, 2.0, value=0.5, step=0.1, label="Line Width", full_width=True)
    line_width
    return (line_width,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(iterations, line_color, line_width, np, plt, preset, step_length):
    def generate_lsystem_string(axiom, rules, num_iterations):
        """
        Generate L-system string by iteratively applying production rules.

        Args:
            axiom: Starting string
            rules: Dictionary mapping symbols to replacements
            num_iterations: Number of rewriting passes

        Returns:
            Final string after all iterations
        """
        current = axiom
        for _ in range(num_iterations):
            next_string = ""
            for char in current:
                # Replace if rule exists, otherwise keep character
                next_string += rules.get(char, char)
            current = next_string
        return current

    def draw_lsystem(ax, string, angle_deg, step_len, color, lw):
        """
        Interpret L-system string as turtle graphics.

        Args:
            ax: Matplotlib axis
            string: L-system command string
            angle_deg: Turning angle in degrees
            step_len: Distance per forward command
            color: Line color
            lw: Line width
        """
        x, y = 0, 0
        angle = 90  # Start pointing up
        stack = []
        lines_x, lines_y = [], []

        for cmd in string:
            if cmd in "FG":
                # Move forward and draw
                x_new = x + step_len * np.cos(np.radians(angle))
                y_new = y + step_len * np.sin(np.radians(angle))
                lines_x.extend([x, x_new, None])  # None creates line break
                lines_y.extend([y, y_new, None])
                x, y = x_new, y_new
            elif cmd == "+":
                angle -= angle_deg  # Turn right
            elif cmd == "-":
                angle += angle_deg  # Turn left
            elif cmd == "[":
                stack.append((x, y, angle))  # Save state
            elif cmd == "]":
                if stack:
                    x, y, angle = stack.pop()  # Restore state

        # Plot all lines at once (much faster)
        ax.plot(lines_x, lines_y, color=color, linewidth=lw, alpha=0.8)

    # Get preset parameters
    axiom, rules, angle = preset.value

    # Generate the L-system string
    lsys_string = generate_lsystem_string(axiom, rules, iterations.value)

    # Create visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")
    ax.set_aspect("equal")
    ax.axis("off")

    draw_lsystem(ax, lsys_string, angle, step_length.value, line_color.value, line_width.value)

    ax.set_title(
        f"L-System | Iterations: {iterations.value} | Commands: {len(lsys_string):,}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return (
        angle,
        axiom,
        draw_lsystem,
        fig,
        generate_lsystem_string,
        lsys_string,
        rules,
    )


@app.cell
def _(mo, preset):
    axiom_display, rules_display, angle_display = preset.value
    rules_str = ", ".join([f"{k} → {v}" for k, v in rules_display.items()])

    mo.md(
        f"""
        ---

        ## Current Grammar

        **Axiom:** `{axiom_display}`

        **Rules:** {rules_str}

        **Angle:** {angle_display}°

        ---

        ## Understanding L-Systems

        L-Systems are **formal grammars** that generate strings through parallel rewriting.
        Each iteration applies ALL rules simultaneously (unlike sequential rewriting).

        **Growth rate:** String length grows exponentially!
        - Iteration 1: ~10 characters
        - Iteration 5: ~1,000 characters
        - Iteration 7: ~10,000+ characters

        **Self-similarity:** Each branch contains smaller copies of the whole structure,
        creating **fractal** patterns at multiple scales.

        ---

        ## Presets Explained

        | Pattern | Description |
        |---------|-------------|
        | Plant | Realistic plant with branches |
        | Tree | Symmetric tree structure |
        | Bush | Dense branching pattern |
        | Sierpinski | Famous fractal triangle |
        | Koch Curve | Snowflake-like curve |
        | Dragon Curve | Space-filling curve |

        ---

        [← Cellular Automata](01_cellular_automata.html) | [Back to Index](index.html) | [Strange Attractors →](03_strange_attractors.html)
        """
    )
    return angle_display, axiom_display, rules_display, rules_str


if __name__ == "__main__":
    app.run()
