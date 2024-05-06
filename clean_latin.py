from pathlib import Path
from .breviarum.io import read_file, write_file
from .breviarum.markdown import Markdown
from .breviarum.model import Human, Haiku, Opus

# model used
model = Haiku()

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# OCRs
ocr_folder = data_folder / 'ocr'
ocr1_file = ocr_folder / '1701 (v1).txt'
ocr2_file = ocr_folder / '1701 (v2).txt'
ocr1 = read_file(ocr1_file)
ocr2 = read_file(ocr2_file)

# index
index_folder = data_folder / 'index'
index_file = index_folder / '1701.md'
index = read_file(index_file)

# prompt
prompt_folder = data_folder / 'prompt'
prompt_file = prompt_folder / 'ocr_cleanup.md'
raw_prompt = read_file(prompt_file)

# output
output_file = data_folder / 'latin.md'

#----------------------------------------------------------------------------------------
# PROCESS HEADINGS

def build_prompt(heading:str, heading_next:str, raw_prompt:str=raw_prompt, index:str=index) -> str:
    """takes a heading (as well as the next one) and produces an ocr cleaning prompt"""
    prompt = raw_prompt.replace('$INDEX', index)
    prompt = prompt.replace('$HEADING', heading)
    prompt = prompt.replace('$NEXT-HEADING', heading_next)
    return prompt

def clean_up_ocr(output_file:Path) -> str:
    """Loads the file and cleans up as much of the OCR as possible"""
    output = read_file(output_file, default_value=index)
    root = Markdown.from_text(output)
    nb_headings = len(root)
    current_heading = 0
    # load the latin recurcively
    def clean_up_ocr_rec(section:Markdown, next_title=None):
        # displays progress
        nonlocal current_heading
        current_heading += 1
        print(f"[{current_heading}/{nb_headings}] Processing '{section.title}'.")
        # load the next title
        if len(section.children) > 0:
            next_title = section.children[0].title
        # load the latin
        if (section.level > 1) and (len(section.content) == 0) and (next_title is not None):
            # builds the latin extraction prompt for the heading
            prompt = build_prompt(section.title, next_title)
            # queries the model
            latin = model.chat(prompt, documents=[ocr1, ocr2], answer_prefix='<response>', stop_sequences=['</response>'])
            # display and returns
            print(f"\n{latin}\n")
            section.content = latin
        # save the results so far
        write_file(output_file, root.__str__())
        # process the children
        if len(section.children) > 0:
            titles = [child.title for child in section.children]
            next_titles = titles[1:] + [next_title]
            for child, next_child_title in zip(section.children, next_titles):
                clean_up_ocr_rec(child, next_child_title)
    clean_up_ocr_rec(root)
    # return
    return root.__str__()

# Runs on the document
clean_up_ocr(output_file)
