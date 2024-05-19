#!/bin/bash

# Run the Python script
source activate language_model
python3 markdown_to_hugo.py

# Run the shell script
./markdown_to_epub.sh

# Define the source and target paths
SOURCE_FOLDER="./data/hugo/english/breviarum politicorum"
TARGET_FOLDER="/home/nestor/Documents/blog/nestordemeure.github.io/content/writing/translations/breviarum_politicorum"
INDEX_MD="./data/hugo/english/breviarum politicorum/_index.md"
SOURCE_EPUB="./data/epub/Mazarin_Breviarium_Politicorum.epub"
TARGET_EPUB="./data/hugo/english/breviarum politicorum/assets/Mazarin_Breviarium_Politicorum.epub"
SOURCE_ENG_MD="./data/english.md"
TARGET_ENG_MD="./data/hugo/english/breviarum politicorum/6 translators notes/2 translation/1 english.md"
SOURCE_LAT_MD="./data/latin_simplified.md"
TARGET_LAT_MD="./data/hugo/english/breviarum politicorum/6 translators notes/1 latin reference/2 latin.md"

# Delete the main _index.md file
rm -f "$INDEX_MD"

# Create the necessary directories
mkdir -p "$(dirname "$TARGET_EPUB")"
mkdir -p "$(dirname "$TARGET_ENG_MD")"
mkdir -p "$(dirname "$TARGET_LAT_MD")"

# Copy the EPUB file
cp "$SOURCE_EPUB" "$TARGET_EPUB"

# Copy the Markdown files
cp "$SOURCE_ENG_MD" "$TARGET_ENG_MD"
cp "$SOURCE_LAT_MD" "$TARGET_LAT_MD"

# Add the header to the english Markdown file
HEADER_ENG='---
title: "English Translation"
draft: false
comments: false
weight: -3
---

<!-- Old Style -->
<link rel="stylesheet" href="/css/styles/old_style.css">
'
# Insert the header at the beginning of the file
echo "$HEADER_ENG" | cat - "$TARGET_ENG_MD" > temp && mv temp "$TARGET_ENG_MD"

# Add the header to the latin Markdown file
HEADER_LAT='---
title: "Latin Reference"
css: "old.css"
draft: false
comments: false
weight: -2
---

<!-- Old Style -->
<link rel="stylesheet" href="/css/styles/old_style.css">
'
# Insert the header at the beginning of the file
echo "$HEADER_LAT" | cat - "$TARGET_LAT_MD" > temp && mv temp "$TARGET_LAT_MD"

# Prompt the user for confirmation
read -p "Press Enter to sync files from $SOURCE_FOLDER to $TARGET_FOLDER or Ctrl+C to cancel."
# Use rsync to move files and folders, replacing and merging as necessary, without deleting files in the target
rsync -av "$SOURCE_FOLDER/" "$TARGET_FOLDER/"

echo "All tasks completed successfully."
