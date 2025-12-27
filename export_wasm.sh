#!/bin/bash
# Export all Marimo notebooks to WASM HTML for GitHub Pages hosting

set -e

echo "=== Exporting Marimo notebooks to WASM HTML ==="

# Create output directory
mkdir -p docs

# Export each notebook
for notebook in notebooks/*.py; do
    filename=$(basename "$notebook" .py)
    echo "Exporting $filename..."
    marimo export html-wasm "$notebook" -o "docs/${filename}.html" --mode run
done

echo ""
echo "=== Export complete! ==="
echo "Files in docs/:"
ls -la docs/
echo ""
echo "To test locally: cd docs && python -m http.server 8000"
echo "Then visit: http://localhost:8000/index.html"
