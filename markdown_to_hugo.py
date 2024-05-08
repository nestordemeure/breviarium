"""
Takes a markdown file and produces a Hugo folder hierarchy.
"""
from pathlib import Path
from breviarum.io import read_file, write_file
from breviarum.markdown import Markdown

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# input
input_file = data_folder / 'english_gpt.md'
input = read_file(input_file)
markdown = Markdown.from_text(input)

# output folder
output_folder = data_folder / 'hugo'

#----------------------------------------------------------------------------------------
# PROCESSING THE FILE

def create_header(title, priority):
    """Create an header for a Hugo file"""
    return f'---\
title: "{title}"\
draft: false\
comments: false\
weight: -{priority}\
images:\
---'.strip()

def create_hugo_rec(node: Markdown, folder: Path, priority:int=0):
    # content to be printed to file
    header = create_header(node.title, priority)
    body = node.__str__() # TODO remove title heading
    content = header + '\n\n' + body
    # create the corresponding file or folder
    if len(node.children) == 0:
        # no children, create a file
        # writes to file
        filename = f"{priority} {node.title}.md" # TODO simplify name (minuscule, only first words)
        file_path = folder / filename
        write_file(file_path, content)
    else:
        # children, create a folder with an index
        # TODO create folder
        sub_folder = folder / f"{priority} {node.title}"
        # TODO create index file
        filename = "_index.md"
        file_path = sub_folder / filename
        write_file(file_path, content)
        # create children
        for child_priority, child in enumerate(node.children):
            create_hugo_rec(child, sub_folder, child_priority)


create_hugo_rec(markdown, output_folder)