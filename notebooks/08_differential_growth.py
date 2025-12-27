import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Differential Growth - Biological Simulation")


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
        # 8. Differential Growth - Biological Simulation
        [← Back to Index](index.html)

        **Differential growth** mimics how organisms grow by pushing points apart along edges.
        Points repel non-neighbors, attract neighbors, and split when edges get too long.
        """
    )
    return


@app.cell
def _(mo):
    initial_points = mo.ui.slider(20, 150, value=50, label="Initial Points", full_width=True)
    growth_steps = mo.ui.slider(50, 800, value=300, step=25, label="Growth Steps", full_width=True)
    seed = mo.ui.slider(1, 100, value=42, label="Random Seed", full_width=True)
    repulsion_strength = mo.ui.slider(0.01, 0.05, value=0.02, step=0.005, label="Repulsion Strength", full_width=True)
    line_color = mo.ui.dropdown(
        options=["lime", "cyan", "white", "yellow", "magenta", "orange"],
        value="lime",
        label="Line Color"
    )
    return initial_points, growth_steps, seed, repulsion_strength, line_color


@app.cell
def _(mo, initial_points, growth_steps, seed, repulsion_strength, line_color, np, plt):
    def differential_growth(num_points, steps, random_seed, repulsion):
        """
        Simulate differential growth.

        Args:
            num_points: Initial number of points on the curve
            steps: Number of growth iterations
            random_seed: Seed for reproducibility
            repulsion: Strength of repulsion force

        Returns:
            Final points array and edges list
        """
        np.random.seed(random_seed)

        # Initialize as circle
        angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
        points = np.column_stack([np.cos(angles), np.sin(angles)]) * 0.3

        # Connect adjacent points
        edges = [(i, (i + 1) % num_points) for i in range(num_points)]

        # Parameters
        max_edge_len = 0.05
        min_dist = 0.02
        repulsion_radius = 0.04
        attraction_force = 0.01

        for _ in range(steps):
            n_pts = len(points)
            forces = np.zeros_like(points)

            # Edge attraction (keep connected points together)
            for i, j in edges:
                diff = points[j] - points[i]
                dist = np.linalg.norm(diff)
                if dist > 0:
                    direction = diff / dist
                    forces[i] += attraction_force * direction
                    forces[j] -= attraction_force * direction

            # Point repulsion (push non-neighbors apart)
            for i in range(n_pts):
                for j in range(i + 1, n_pts):
                    diff = points[j] - points[i]
                    dist = np.linalg.norm(diff)
                    if 0 < dist < repulsion_radius:
                        strength = repulsion * (repulsion_radius - dist) / dist
                        force = strength * diff
                        forces[i] -= force
                        forces[j] += force

            # Apply forces
            points = points + forces * 0.5

            # Split long edges
            new_edges = []
            new_points = list(points)

            for i, j in edges:
                dist = np.linalg.norm(points[j] - points[i])
                if dist > max_edge_len:
                    # Insert new point at midpoint with slight noise
                    mid = (points[i] + points[j]) / 2
                    mid += np.random.randn(2) * 0.001
                    new_idx = len(new_points)
                    new_points.append(mid)
                    new_edges.append((i, new_idx))
                    new_edges.append((new_idx, j))
                else:
                    new_edges.append((i, j))

            points = np.array(new_points)
            edges = new_edges

        return points, edges

    # Run simulation
    final_points, final_edges = differential_growth(
        initial_points.value,
        growth_steps.value,
        seed.value,
        repulsion_strength.value
    )

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

    # Draw edges
    for i, j in final_edges:
        ax.plot(
            [final_points[i, 0], final_points[j, 0]],
            [final_points[i, 1], final_points[j, 1]],
            color=line_color.value,
            linewidth=1,
            alpha=0.8
        )

    # Draw points (small)
    ax.scatter(
        final_points[:, 0], final_points[:, 1],
        c=line_color.value, s=2, alpha=0.5
    )

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Differential Growth | {len(final_points)} points | {growth_steps.value} steps",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        initial_points, growth_steps, seed, repulsion_strength, line_color,
        mo.md("---"),
        mo.md("""
**Try these:**
- High repulsion (0.05): Aggressive branching
- More steps (600+): Finer detail
- Fewer initial points: Simpler base shape
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
