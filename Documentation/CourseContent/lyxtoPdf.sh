#!/bin/bash

# Constants
INPUT_FILE="CourseContent.lyx"
OUTPUT_FILE="CourseContent.pdf"
OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"

# Export .lyx to .tex
lyx -e pdflatex "$INPUT_FILE"

# Get the filename without extension
BASE_NAME=$(basename "$INPUT_FILE" .lyx)

# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Compile .tex to PDF using pdflatex
pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$OUTPUT_DIR/${BASE_NAME}.tex"

# Rename the output PDF to the desired name if not already correct
mv "$OUTPUT_DIR/${BASE_NAME}.pdf" "$OUTPUT_FILE"

echo "PDF generated: $OUTPUT_FILE"
