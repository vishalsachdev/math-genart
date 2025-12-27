# CLAUDE.md

Project-specific instructions and context for Claude Code.

---

## Project Overview

**Mathematical Generative Art Systems** - A collection of 12 interactive mathematical visualizations that create beautiful generative art.

- **Live Site**: https://vishalsachdev.github.io/math-genart/
- **Technology**: Marimo notebooks exported to WebAssembly for browser-only execution
- **Inspiration**: Based on Wilfred Kamau's LinkedIn post on mathematical generative art systems

### Systems

| # | System | Key Concepts |
|---|--------|--------------|
| 1 | Cellular Automata | Conway's Game of Life, rule-based emergence |
| 2 | L-Systems | Lindenmayer systems, organic growth via string rewriting |
| 3 | Strange Attractors | Lorenz, Clifford, Aizawa - deterministic chaos |
| 4 | Fractals | Mandelbrot, Julia sets - infinite complexity from z^2 + c |
| 5 | Reaction-Diffusion | Gray-Scott model, chemical pattern formation |
| 6 | Voronoi Diagrams | Space partitioning, natural geometry |
| 7 | Fourier & Lissajous | Wave visualization, oscillating curves |
| 8 | Differential Growth | Biological simulation, organic structures |
| 9 | Prime Geometry | Ulam spirals, arithmetic aesthetics |
| 10 | Graph Networks | Topology art, neural and social networks |
| 11 | Phase Portraits | Complex domain coloring, function visualization |
| 12 | Dynamical Systems | Bifurcation diagrams, route to chaos |

---

## Quick Commands

```bash
# Run a notebook locally
marimo run notebooks/01_cellular_automata.py

# Edit a notebook interactively
marimo edit notebooks/01_cellular_automata.py

# Export all notebooks to WASM HTML
./export_wasm.sh

# Test locally
cd docs && python -m http.server 8000
```

---

## Project Structure

```
math-genart/
├── notebooks/           # Marimo Python notebooks (source)
│   ├── index.py        # Landing page with system cards
│   ├── 01_cellular_automata.py
│   ├── ...
│   └── 12_dynamical_systems.py
├── docs/               # WASM-exported HTML (GitHub Pages)
│   ├── index.html
│   ├── *.html          # One per notebook
│   └── assets/         # Marimo WASM runtime
├── export_wasm.sh      # Export script
└── requirements.txt    # Python dependencies
```

---

## Current Focus

- [x] Project complete - all 12 systems implemented and deployed

---

## Roadmap

### Phase 1: Core Implementation (Complete)
- [x] Create 12 mathematical visualization notebooks
- [x] Export all notebooks to WebAssembly HTML
- [x] Deploy to GitHub Pages
- [x] Add column layout (controls left, visualization right)
- [x] Add credit attribution to original source

### Phase 2: Potential Enhancements (Future)
- [ ] Add color scheme selector (dark mode, custom palettes)
- [ ] Enable PNG/SVG export from visualizations
- [ ] Add animation controls (play/pause for dynamic systems)
- [ ] Create gallery view with thumbnails
- [ ] Add preset parameter configurations per system
- [ ] Mobile-responsive layout improvements
- [ ] Add mathematical explanations/tooltips

---

## Session Log

### 2025-12-27
- **Completed**: Column layout added to all 12 notebooks, WASM re-export, credit attribution to Wilfred Kamau, pushed to GitHub
- **Method**: Used 7 parallel subagents to speed up notebook updates
- **Status**: Project is feature-complete and deployed
- **Next**: Consider Phase 2 enhancements if desired

---

## Code Patterns

### Notebook Structure
Each notebook follows this pattern:
1. Imports cell
2. UI controls (sliders, dropdowns) in left column
3. Visualization function in right column
4. Educational markdown explaining the mathematics

### WASM Export
Notebooks are exported with:
```bash
marimo export html-wasm notebook.py -o docs/notebook.html --mode run
```

---

## Dependencies

- **marimo**: Reactive notebook framework
- **numpy**: Numerical computing
- **matplotlib**: Visualization
- **scipy**: Scientific algorithms (for some systems)
