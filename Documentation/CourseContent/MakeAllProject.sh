#!/bin/bash
python syncContent.py
./renderpuml.sh
# Constants
INPUT_FILE="CourseContent"
OUTPUT_FILE="CourseContent.pdf"
OUTPUT_DIR="$(dirname "$OUTPUT_FILE")"


# Ensure the output directory exists
mkdir -p "$OUTPUT_DIR"

# Compile .tex to PDF using pdflatex
pdflatex -interaction=nonstopmode -output-directory="$OUTPUT_DIR" "$OUTPUT_DIR/${INPUT_FILE}.tex"

# Rename the output PDF to the desired name if not already correct
mv "$OUTPUT_DIR/${BASE_NAME}.pdf" "$OUTPUT_FILE"

echo "PDF generated: $OUTPUT_FILE"
