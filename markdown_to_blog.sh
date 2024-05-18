#!/bin/bash

# Run the Python script
source activate language_model
python3 markdown_to_hugo.py

# Run the shell script
./markdown_to_epub.sh

# Define the source and target paths
SOURCE_EPUB="./data/epub/Mazarin_Breviarium_Politicorum.epub"
TARGET_EPUB="./data/hugo/english/breviarum politicorum/assets/Mazarin_Breviarium_Politicorum.epub"
SOURCE_MD="./data/english.md"
TARGET_MD="./data/hugo/english/breviarum politicorum/6 translators notes/2 translation/1 english.md"
INDEX_MD="./data/hugo/english/breviarum politicorum/_index.md"

# Delete the main _index.md file
rm -f "$INDEX_MD"

# Create the necessary directories
mkdir -p "$(dirname "$TARGET_EPUB")"
mkdir -p "$(dirname "$TARGET_MD")"

# Copy the EPUB file
cp "$SOURCE_EPUB" "$TARGET_EPUB"

# Copy the Markdown file
cp "$SOURCE_MD" "$TARGET_MD"

# Add the header to the Markdown file
HEADER='---
title: "English Translation"
draft: false
comments: false
weight: -3
---

<!-- Old Style -->
<link rel="stylesheet" href="/css/styles/old_style.css">
'

# Insert the header at the beginning of the file
echo "$HEADER" | cat - "$TARGET_MD" > temp && mv temp "$TARGET_MD"

echo "All tasks completed successfully."
