import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Graph Networks - Topology Art")


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
        # 10. Graph Theory & Network Flow
        [← Back to Index](index.html)

        **Connections matter more than positions.** Neural maps, knowledge graphs,
        and social network abstractions emerge from relationship patterns.
        """
    )
    return


@app.cell
def _(mo):
    num_nodes = mo.ui.slider(10, 150, value=60, label="Number of Nodes", full_width=True)
    edge_prob = mo.ui.slider(0.02, 0.25, value=0.08, step=0.01, label="Edge Probability", full_width=True)
    seed = mo.ui.slider(1, 100, value=42, label="Random Seed", full_width=True)
    colormap = mo.ui.dropdown(
        options=["plasma", "viridis", "magma", "inferno", "coolwarm", "YlOrRd"],
        value="plasma",
        label="Node Colormap"
    )
    layout = mo.ui.dropdown(
        options=["Random", "Circular", "Force-directed"],
        value="Force-directed",
        label="Layout"
    )
    return num_nodes, edge_prob, seed, colormap, layout


@app.cell
def _(mo, num_nodes, edge_prob, seed, colormap, layout, np, plt):
    def generate_random_graph(n, p, random_seed):
        """
        Generate Erdős–Rényi random graph G(n, p).

        Args:
            n: Number of nodes
            p: Probability of each edge
            random_seed: Seed for reproducibility

        Returns:
            edges: List of (i, j) tuples
            degree: Degree of each node
        """
        np.random.seed(random_seed)

        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if np.random.rand() < p:
                    edges.append((i, j))

        # Calculate degrees
        degree = np.zeros(n)
        for i, j in edges:
            degree[i] += 1
            degree[j] += 1

        return edges, degree

    def random_layout(n, random_seed):
        """Random positions in unit square."""
        np.random.seed(random_seed)
        return np.random.rand(n, 2)

    def circular_layout(n):
        """Nodes arranged in a circle."""
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
        return np.column_stack([np.cos(angles), np.sin(angles)]) * 0.45 + 0.5

    def force_directed_layout(n, edges, random_seed, iterations=50):
        """
        Simple force-directed layout (Fruchterman-Reingold style).

        Connected nodes attract, all nodes repel.
        """
        np.random.seed(random_seed)
        pos = np.random.rand(n, 2)

        k = 1.0 / np.sqrt(n)  # Optimal distance

        for _ in range(iterations):
            # Repulsion between all pairs
            disp = np.zeros((n, 2))
            for i in range(n):
                for j in range(i + 1, n):
                    delta = pos[i] - pos[j]
                    dist = max(np.linalg.norm(delta), 0.01)
                    force = k * k / dist
                    direction = delta / dist
                    disp[i] += force * direction
                    disp[j] -= force * direction

            # Attraction along edges
            for i, j in edges:
                delta = pos[i] - pos[j]
                dist = max(np.linalg.norm(delta), 0.01)
                force = dist * dist / k
                direction = delta / dist
                disp[i] -= force * direction
                disp[j] += force * direction

            # Apply displacement with cooling
            temp = 0.1 * (1 - _ / iterations)
            for i in range(n):
                disp_len = np.linalg.norm(disp[i])
                if disp_len > 0:
                    pos[i] += disp[i] / disp_len * min(disp_len, temp)

            # Keep in bounds
            pos = np.clip(pos, 0.05, 0.95)

        return pos

    # Generate graph
    n = num_nodes.value
    edges, degree = generate_random_graph(n, edge_prob.value, seed.value)

    # Generate layout
    if layout.value == "Random":
        pos = random_layout(n, seed.value)
    elif layout.value == "Circular":
        pos = circular_layout(n)
    else:
        pos = force_directed_layout(n, edges, seed.value)

    # Visualization
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

    # Draw edges
    for i, j in edges:
        ax.plot(
            [pos[i, 0], pos[j, 0]],
            [pos[i, 1], pos[j, 1]],
            "w-", linewidth=0.3, alpha=0.3
        )

    # Draw nodes (size by degree)
    sizes = (degree + 1) * 15
    scatter = ax.scatter(
        pos[:, 0], pos[:, 1],
        c=degree, cmap=colormap.value,
        s=sizes, alpha=0.8,
        edgecolors="white", linewidths=0.5
    )

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_aspect("equal")
    ax.axis("off")

    avg_degree = 2 * len(edges) / n if n > 0 else 0
    ax.set_title(
        f"Network Graph | {n} nodes, {len(edges)} edges | Avg degree: {avg_degree:.1f}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        num_nodes, edge_prob, seed, colormap, layout,
        mo.md("---"),
        mo.md("""
**Try these:**
- Force-directed + 60 nodes: Organic clusters
- Circular + high edge prob: Dense webs
- Random layout: Baseline comparison
- Low edge prob (0.02): Sparse, disconnected
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
