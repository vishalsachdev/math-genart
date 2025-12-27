import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Voronoi Diagrams - Space Partitioning")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.spatial import Voronoi, Delaunay
    plt.style.use('dark_background')
    return Delaunay, Voronoi, np, plt


@app.cell
def _(mo):
    mo.md(
        """
        # 6. Voronoi Diagrams & Delaunay Triangulation
        [← Back to Index](index.html)

        **Voronoi diagrams** partition space so each region contains all points closest to one seed.
        Natural geometry found in crystals, cells, and city districts. Delaunay triangulation is the dual graph.
        """
    )
    return


@app.cell
def _(mo):
    num_points = mo.ui.slider(10, 200, value=50, label="Number of Points", full_width=True)
    seed = mo.ui.slider(1, 100, value=42, label="Random Seed", full_width=True)
    display_mode = mo.ui.dropdown(
        options=["Voronoi", "Delaunay", "Both"],
        value="Voronoi",
        label="Display Mode"
    )
    colormap = mo.ui.dropdown(
        options=["rainbow", "viridis", "plasma", "Set3", "tab20", "twilight"],
        value="rainbow",
        label="Color Map"
    )
    show_points = mo.ui.checkbox(value=True, label="Show seed points")
    return num_points, seed, display_mode, colormap, show_points


@app.cell
def _(Delaunay, Voronoi, colormap, display_mode, mo, np, num_points, plt, seed, show_points):
    # Generate random points
    np.random.seed(seed.value)
    points = np.random.rand(num_points.value, 2)

    # Create figure
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

    # Get colormap
    cmap = plt.get_cmap(colormap.value)
    colors = [cmap(i / num_points.value) for i in range(num_points.value)]

    # Draw Voronoi diagram
    if display_mode.value in ["Voronoi", "Both"]:
        vor = Voronoi(points)

        for i, point_idx in enumerate(vor.point_region):
            region = vor.regions[point_idx]
            if -1 not in region and len(region) > 0:
                polygon = [vor.vertices[j] for j in region]
                # Clip to [0,1] bounds
                polygon = np.array(polygon)
                ax.fill(
                    polygon[:, 0], polygon[:, 1],
                    alpha=0.6,
                    color=colors[i % len(colors)],
                    edgecolor="white",
                    linewidth=0.5
                )

    # Draw Delaunay triangulation
    if display_mode.value in ["Delaunay", "Both"]:
        tri = Delaunay(points)
        edge_color = "cyan" if display_mode.value == "Both" else "white"
        ax.triplot(
            points[:, 0], points[:, 1], tri.simplices,
            color=edge_color,
            linewidth=0.8,
            alpha=0.8
        )

    # Draw seed points
    if show_points.value:
        ax.scatter(
            points[:, 0], points[:, 1],
            c="white", s=30, zorder=5,
            edgecolors="black", linewidths=0.5
        )

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"{display_mode.value} | {num_points.value} points | Seed: {seed.value}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()

    controls = mo.vstack([
        mo.md("### Controls"),
        num_points, seed, display_mode, colormap, show_points,
        mo.md("---"),
        mo.md("""
**Try these:**
- Voronoi mode: See cell territories
- Delaunay mode: See triangulation
- Both mode: View the duality
- More points = finer partitions
        """)
    ], gap=1)

    visualization = mo.vstack([
        mo.md("### Visualization"),
        fig
    ])

    mo.hstack([controls, visualization], widths=[1, 2], gap=2)
    return


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Voronoi vs Delaunay Duality

        These two structures are **duals** of each other:

        | Voronoi | Delaunay |
        |---------|----------|
        | Face (region) | Vertex (point) |
        | Edge | Edge |
        | Vertex | Face (triangle) |

        If you connect the Voronoi vertices that share an edge, you get the Delaunay triangulation.
        If you connect the circumcenters of Delaunay triangles, you get the Voronoi diagram.

        ---

        ## Properties

        **Voronoi diagram:**
        - Each cell is convex
        - Edges are perpendicular bisectors of point pairs
        - Used for nearest-neighbor queries in O(log n) time

        **Delaunay triangulation:**
        - Maximizes minimum angle (avoids skinny triangles)
        - No point lies inside any triangle's circumcircle
        - Unique for points in general position

        ---

        ## Natural Occurrences

        Voronoi patterns appear everywhere in nature:
        - **Giraffe spots** - pigment cells establish territories
        - **Dragonfly wings** - cell membranes
        - **Mud cracks** - stress relief patterns
        - **Foam bubbles** - minimal surface area
        - **Galaxy distribution** - cosmic web structure

        ---

        [← Reaction-Diffusion](05_reaction_diffusion.html) | [Back to Index](index.html) | [Fourier →](07_fourier.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
