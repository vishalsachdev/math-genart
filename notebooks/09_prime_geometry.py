import marimo

__generated_with = "0.13.4"
app = marimo.App(width="full", app_title="Prime Geometry - Arithmetic Aesthetics")


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

        **Ulam Spiral**: Discovered in 1963, primes plotted on an integer spiral reveal mysterious diagonal patterns.
        These correspond to quadratic polynomials like n² + n + 41 (Euler's prime-generator).
        """
    )
    return


@app.cell
def _(mo):
    max_number = mo.ui.slider(1000, 100000, value=20000, step=1000, label="Maximum Number", full_width=True)
    point_size = mo.ui.slider(0.1, 5.0, value=1.0, step=0.1, label="Point Size", full_width=True)
    point_color = mo.ui.dropdown(
        options=["cyan", "lime", "yellow", "magenta", "white", "orange"],
        value="cyan",
        label="Point Color"
    )
    return max_number, point_size, point_color


@app.cell
def _(max_number, mo, np, plt, point_color, point_size):
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
    fig, ax = plt.subplots(figsize=(8, 8), facecolor="black")

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

    controls = mo.vstack([
        mo.md("### Controls"),
        max_number, point_size, point_color,
        mo.md("---"),
        mo.md("""
**Try these:**
- 20,000 max: See the basic diagonals
- 100,000 max: Rich diagonal structure
- Small point size (0.5): More detail
- Increase point size for dense look
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
