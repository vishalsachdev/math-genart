import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Mathematical Generative Art Systems")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md(
        """
        # Mathematical Generative Art Systems

        **12 proven mathematical systems for high-impact generative art.**

        Each system demonstrates how simple rules create complex, beautiful patterns.
        Click on any system below to explore it interactively.

        Based on the comprehensive guide by [Wilfred Kamau](https://www.linkedin.com/posts/wilfred-kamau-001134267_mathematical-system-for-generative-ai-activity-7409583130673696768-hqoB).

        ---

        ### [1. Cellular Automata](01_cellular_automata.html)
        **Rule-Based Emergence** - Conway's Game of Life

        ### [2. L-Systems](02_lsystems.html)
        **Organic Growth** - String rewriting creates botanical structures

        ### [3. Strange Attractors](03_strange_attractors.html)
        **Chaos with Memory** - Lorenz, Clifford, Aizawa attractors

        ### [4. Fractals](04_fractals.html)
        **Infinite Detail** - Mandelbrot, Julia sets

        ### [5. Reaction-Diffusion](05_reaction_diffusion.html)
        **Chemical Art** - Gray-Scott model patterns

        ### [6. Voronoi Diagrams](06_voronoi.html)
        **Space Partitioning** - Natural geometry

        ### [7. Fourier & Lissajous](07_fourier.html)
        **Wave Visualization** - Transform waves into art

        ### [8. Differential Growth](08_differential_growth.html)
        **Biological Simulation** - Organism growth

        ### [9. Prime Geometry](09_prime_geometry.html)
        **Arithmetic Aesthetics** - Ulam spirals

        ### [10. Graph Networks](10_graph_networks.html)
        **Topology Art** - Neural maps

        ### [11. Phase Portraits](11_phase_portraits.html)
        **Complex Domain Coloring** - Function visualization

        ### [12. Dynamical Systems](12_dynamical_systems.html)
        **Route to Chaos** - Bifurcation diagrams

        ---

        ## About These Visualizations

        Each notebook provides:
        - **Interactive parameters** - adjust seeds, iterations, and system-specific values
        - **Real-time rendering** - see changes instantly as you modify parameters
        - **Deterministic generation** - same seed = same output

        Built with [Marimo](https://marimo.io) and exported to WebAssembly for browser-only execution.
        """
    )
    return


if __name__ == "__main__":
    app.run()
