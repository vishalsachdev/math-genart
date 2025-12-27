# Mathematical Generative Art Systems

Interactive visualizations of 12 mathematical systems that create beautiful generative art.

**[View Live Demo](https://YOUR_USERNAME.github.io/math-genart/)**

Based on the comprehensive guide "Mathematical Generative Art Systems" by Willy (2025).

## Systems Included

| # | System | Description |
|---|--------|-------------|
| 1 | **Cellular Automata** | Conway's Game of Life - rule-based emergence |
| 2 | **L-Systems** | Lindenmayer systems - organic growth via string rewriting |
| 3 | **Strange Attractors** | Lorenz, Clifford, Aizawa - deterministic chaos |
| 4 | **Fractals** | Mandelbrot, Julia sets - infinite complexity from z² + c |
| 5 | **Reaction-Diffusion** | Gray-Scott model - chemical pattern formation |
| 6 | **Voronoi Diagrams** | Space partitioning - natural geometry |
| 7 | **Fourier & Lissajous** | Wave visualization - oscillating curves |
| 8 | **Differential Growth** | Biological simulation - organic structures |
| 9 | **Prime Geometry** | Ulam spirals - arithmetic aesthetics |
| 10 | **Graph Networks** | Topology art - neural and social networks |
| 11 | **Phase Portraits** | Complex domain coloring - function visualization |
| 12 | **Dynamical Systems** | Bifurcation diagrams - route to chaos |

## Features

- **Interactive parameters**: Adjust seeds, iterations, and system-specific values in real-time
- **Browser-only execution**: Runs entirely in WebAssembly, no server needed
- **Deterministic generation**: Same parameters = same output (perfect for NFTs)
- **Educational content**: Each notebook explains the mathematics behind the visualizations

## Local Development

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run notebooks locally

```bash
# Run a specific notebook
marimo run notebooks/01_cellular_automata.py

# Or edit interactively
marimo edit notebooks/01_cellular_automata.py
```

### Export to WASM HTML

```bash
chmod +x export_wasm.sh
./export_wasm.sh
```

### Test locally

```bash
cd docs
python -m http.server 8000
# Visit http://localhost:8000/index.html
```

## Deploy to GitHub Pages

1. Push to GitHub
2. Go to Settings → Pages
3. Set Source to "Deploy from a branch"
4. Select `main` branch and `/docs` folder
5. Save

Your site will be live at `https://YOUR_USERNAME.github.io/math-genart/`

## Technology

Built with:
- [Marimo](https://marimo.io) - Reactive Python notebooks
- [NumPy](https://numpy.org) - Numerical computing
- [Matplotlib](https://matplotlib.org) - Visualization
- [SciPy](https://scipy.org) - Scientific algorithms

Exported to WebAssembly using Marimo's WASM export for browser-only execution.

## License

MIT License - feel free to use, modify, and share!

## Credits

- Original guide: "Mathematical Generative Art Systems" by Willy (2025)
- Interactive implementation: Built with Claude Code
