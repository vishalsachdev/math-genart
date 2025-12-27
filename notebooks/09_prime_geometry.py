import marimo

__generated_with = "0.13.4"
app = marimo.App(width="medium", app_title="Prime Geometry - Arithmetic Aesthetics")


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
        # 9. Prime Number Geometry - Arithmetic Aesthetics

        [← Back to Index](index.html)

        ---

        Pure arithmetic yields unexpected symmetry. **Ulam spirals** reveal hidden
        patterns in prime numbers that mathematicians still don't fully understand.

        ## The Ulam Spiral

        Discovered by Stanislaw Ulam in 1963 while doodling during a boring meeting:

        1. Write integers in a spiral pattern starting from 1
        2. Circle all the prime numbers
        3. Notice the diagonal patterns!

        ```
        17-16-15-14-13
        |            |
        18  5- 4- 3 12
        |   |     |  |
        19  6  1- 2 11
        |   |        |
        20  7- 8- 9-10
        |
        21-22-23-24-25-...
        ```

        Primes tend to cluster on certain diagonals!
        """
    )
    return


@app.cell
def _(mo):
    mo.md("## Parameters")
    return


@app.cell
def _(mo):
    max_number = mo.ui.slider(1000, 100000, value=20000, step=1000, label="Maximum Number", full_width=True)
    max_number
    return (max_number,)


@app.cell
def _(mo):
    point_size = mo.ui.slider(0.1, 5.0, value=1.0, step=0.1, label="Point Size", full_width=True)
    point_size
    return (point_size,)


@app.cell
def _(mo):
    point_color = mo.ui.dropdown(
        options=["cyan", "lime", "yellow", "magenta", "white", "orange"],
        value="cyan",
        label="Point Color"
    )
    point_color
    return (point_color,)


@app.cell
def _(mo):
    mo.md("---\n## Visualization")
    return


@app.cell
def _(max_number, np, plt, point_color, point_size):
    def sieve_of_eratosthenes(n):
        """
        Efficient prime number generation using Sieve of Eratosthenes.

        Returns a set of all primes up to n.
        """
        is_prime = [True] * (n + 1)
        is_prime[0] = is_prime[1] = False

        for i in range(2, int(n**0.5) + 1):
            if is_prime[i]:
                for j in range(i * i, n + 1, i):
                    is_prime[j] = False

        return set(i for i, p in enumerate(is_prime) if p)

    def ulam_spiral_coordinates(n):
        """
        Generate spiral coordinates for numbers 1 to n.

        Returns a dictionary mapping number -> (x, y) coordinate.
        """
        coords = {1: (0, 0)}
        x, y = 0, 0
        dx, dy = 1, 0  # Start moving right
        steps_in_direction = 1
        steps_taken = 0
        direction_changes = 0

        for num in range(2, n + 1):
            x += dx
            y += dy
            coords[num] = (x, y)
            steps_taken += 1

            if steps_taken == steps_in_direction:
                steps_taken = 0
                # Turn left: (dx, dy) -> (-dy, dx)
                dx, dy = -dy, dx
                direction_changes += 1
                # Increase steps every 2 turns
                if direction_changes % 2 == 0:
                    steps_in_direction += 1

        return coords

    # Generate primes and coordinates
    primes = sieve_of_eratosthenes(max_number.value)
    coords = ulam_spiral_coordinates(max_number.value)

    # Get prime coordinates
    prime_coords = [coords[p] for p in primes if p in coords]

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 10), facecolor="black")

    if prime_coords:
        px, py = zip(*prime_coords)
        ax.scatter(px, py, c=point_color.value, s=point_size.value, alpha=0.6)

    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        f"Ulam Spiral | {len(primes):,} primes up to {max_number.value:,}",
        color="white", fontsize=12, pad=10
    )
    plt.tight_layout()
    fig
    return (
        coords,
        fig,
        prime_coords,
        primes,
        px,
        py,
        sieve_of_eratosthenes,
        ulam_spiral_coordinates,
    )


@app.cell
def _(mo):
    mo.md(
        """
        ---

        ## Why Diagonals?

        The diagonal lines correspond to **quadratic polynomials**. For example:

        - **Main diagonal**: n² + n + 41 (Euler's prime-generating polynomial)
        - Generates primes for n = 0 to 39!

        Many quadratic polynomials happen to generate unusually many primes,
        and these show up as diagonal clusters in the Ulam spiral.

        ---

        ## Mathematical Mystery

        The diagonal patterns are:
        - **Real**: Statistically significant clustering
        - **Unexplained**: No complete theory explains why
        - **Connected**: To deep questions about prime distribution

        The Riemann Hypothesis (one of the greatest unsolved problems) relates
        to how primes are distributed among integers.

        ---

        ## Other Prime Visualizations

        - **Sacks Spiral**: Primes on Archimedean spiral (squares at integers)
        - **Klauber Triangle**: Triangular arrangement
        - **Prime Factorization Diagrams**: Color by factors
        - **Modular Patterns**: Primes mod n create patterns

        ---

        ## Prime Facts

        - There are infinitely many primes (Euclid, 300 BCE)
        - Prime gaps can be arbitrarily large
        - Twin primes (p, p+2) may be infinite (unproven!)
        - The largest known prime has 24+ million digits

        ---

        [← Differential Growth](08_differential_growth.html) | [Back to Index](index.html) | [Graph Networks →](10_graph_networks.html)
        """
    )
    return


if __name__ == "__main__":
    app.run()
