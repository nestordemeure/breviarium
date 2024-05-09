"""
Takes Latin and produces English.
"""
from pathlib import Path
from breviarum.io import read_file, write_file
from breviarum.markdown import Markdown
from breviarum.model import Human, Haiku, Opus

# model used
model = Human()

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# Latin
latin_file = data_folder / 'latin_simplified.md'
latin = read_file(latin_file)

# indices
index_folder = data_folder / 'index'
latin_index_file = index_folder / 'latin_simplified_index.md'
english_index_file = index_folder / 'translated_index.md'
latin_index = read_file(latin_index_file)
english_index = read_file(english_index_file)

# prompt
prompt_folder = data_folder / 'prompt'
prompt_file = prompt_folder / 'translate_latin.md'
raw_prompt = read_file(prompt_file)

# English output
output_file = data_folder / 'english.md'

#----------------------------------------------------------------------------------------
# TRANSLATE

def build_prompt(latin_heading:str, english_heading:str, heading_next:str, raw_prompt:str=raw_prompt) -> str:
    """takes a heading (as well as the next one) and produces an ocr cleaning prompt"""
    prompt = raw_prompt.replace('$LATIN-HEADING', latin_heading)
    prompt = prompt.replace('$ENGLISH-HEADING', english_heading)
    prompt = prompt.replace('$NEXT-HEADING', heading_next)
    return prompt

def translate(latin:str, english_index:str, output_file:Path):
    """Does the translation recurcively"""
    # load the markdown trees
    output = read_file(output_file, default_value=english_index)
    english_root = Markdown.from_text(output)
    latin_root = Markdown.from_text(latin)
    # process recurcively
    nb_headings = len(latin_root)
    current_heading = 0
    def translate_rec(latin_node:Markdown, english_node:Markdown, next_title='the end'):
        nonlocal output
        nonlocal current_heading
        # displays progress
        current_heading += 1
        print(f"[{current_heading}/{nb_headings}] Processing '{latin_node.title}' / '{english_node.title}'.")
        # load the next title
        next_titles = [child.title for child in latin_node.children] + [next_title]
        # does the translation
        if (latin_node.level > 1) and (len(english_node.content) == 0):
            # builds the latin extraction prompt for the heading
            prompt = build_prompt(latin_node.title, english_node.title, next_titles[0])
            # queries the model
            translation = model.chat(prompt, documents=[latin, output], answer_prefix='<response>', stop_sequences=['</response>'])
            # display and returns
            print(f"\n{translation}\n")
            english_node.content = translation
        # save the results so far
        output = english_root.__str__()
        write_file(output_file, output)
        # process the children
        for i in range(len(latin_node.children)):
            latin_child = latin_node.children[i]
            english_child = english_node.children[i]
            next_child_title = next_titles[i+1]
            translate_rec(latin_child, english_child, next_child_title)
        return None
    # run the function
    translate_rec(latin_root, english_root)

#----------------------------------------------------------------------------------------
# MAIN

# process the text
translate(latin, english_index, output_file)