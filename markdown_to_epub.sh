#!/bin/bash

# Define input and output file paths
INPUT_FILE="./data/english.md"
OUTPUT_FILE="./data/epub/Mazarin - Breviarium Politicorum.epub"
CSS_FILE="./data/epub/style.css"
FONT_DIR="./data/epub/fonts"
TITLE_PAGE="./data/epub/title_page.png"

# Define metadata
TITLE="Breviarium Politicorum"
SUBTITLE="Leaves from Mazarin's Notebooks."
AUTHOR="Mazarin"
TRANSLATOR="Nestor Demeure"

# Run pandoc command to convert markdown to epub
pandoc "$INPUT_FILE" -o "$OUTPUT_FILE" \
  --metadata title="$TITLE" \
  --metadata subtitle="$SUBTITLE" \
  --metadata author="$AUTHOR" \
  --metadata translator="$TRANSLATOR" \
  --css="$CSS_FILE" \
  --epub-embed-font="$FONT_DIR/IMFellDWPica-Italic.ttf" \
  --epub-embed-font="$FONT_DIR/IMFellDWPica-Regular.ttf" \
  --epub-embed-font="$FONT_DIR/IMFellDWPicaSC-Regular.ttf" \
  --epub-cover-image="$TITLE_PAGE"

# Check if pandoc succeeded
if [ $? -eq 0 ]; then
  echo "Conversion successful: $OUTPUT_FILE"
else
  echo "Conversion failed"
fi
