import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Differential Growth - Biological Simulation")


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

        ---

        **Differential growth** mimics how organisms grow by pushing points apart along edges.
        Growth is conflict resolved beautifully.

        ## The Algorithm

        1. Start with a closed curve (ring of points connected by edges)
        2. **Repulsion**: Points push away from nearby non-neighbor points
        3. **Attraction**: Connected points pull toward each other
        4. **Splitting**: Edges that get too long split in half

        This creates **veins, mycelium networks, coral, and alien biology**!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    initial_points = mo.ui.slider(20, 150, value=50, label="Initial Points", full_width=True)
    initial_points
    return (initial_points,)


@app.cell
def _(mo):
    growth_steps = mo.ui.slider(50, 800, value=300, step=25, label="Growth Steps", full_width=True)
    growth_steps
    return (growth_steps,)


@app.cell
def _(mo):
    seed = mo.ui.slider(1, 100, value=42, label="Random Seed", full_width=True)
    seed
    return (seed,)


@app.cell
def _(mo):
    repulsion_strength = mo.ui.slider(0.01, 0.05, value=0.02, step=0.005, label="Repulsion Strength", full_width=True)
    repulsion_strength
    return (repulsion_strength,)


@app.cell
def _(mo):
    line_color = mo.ui.dropdown(
        options=["lime", "cyan", "white", "yellow", "magenta", "orange"],
        value="lime",
        label="Line Color"
    )
    line_color
    return (line_color,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(growth_steps, initial_points, line_color, np, plt, repulsion_strength, seed):
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
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")

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
    fig
    return differential_growth, fig, final_edges, final_points


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## The Growth Process

        1. **Initial state**: Simple closed curve (circle)
        2. **Forces applied**:
           - Neighbors attract (maintains connectivity)
           - Non-neighbors repel (creates space)
        3. **Edge splitting**: Long edges spawn new points
        4. **Result**: Complex, organic branching structure

        ---

        ## Natural Analogues

        This process models:
        - **Leaf veins** - constrained growth in 2D
        - **Blood vessels** - vascular networks
        - **Mycelium** - fungal growth networks
        - **Coral** - branching marine organisms
        - **Cracked mud** - stress-driven growth
        - **Lightning** - Lichtenberg figures

        ---

        ## Parameters Explained

        | Parameter | Effect |
        |-----------|--------|
        | **Initial Points** | Complexity of starting shape |
        | **Growth Steps** | How much the curve evolves |
        | **Repulsion Strength** | How aggressively points separate |
        | **Random Seed** | Reproducible variations |

        Higher repulsion → more aggressive branching
        More steps → finer detail and more splitting

        ---

        ## Variations

        - **Multiple seeds**: Start with several curves that interact
        - **Attractors**: Points that curves grow toward
        - **Obstacles**: Regions that block growth
        - **3D extension**: Differential growth in space

        ---

        [← Fourier](07_fourier.html) | [Back to Index](index.html) | [Prime Geometry →](09_prime_geometry.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
