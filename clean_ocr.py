"""
Takes OCRs and produces a clean text.
"""
from pathlib import Path
from breviarum.io import read_file
from breviarum.markdown import Markdown
from breviarum.model import Human, Haiku, Opus

# model used
model = Human()

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
output = read_file(output_file, default_value=index)
output_markdown = Markdown.from_text(output)

#----------------------------------------------------------------------------------------
# PROCESS HEADINGS

def build_prompt(heading:str, heading_next:str, raw_prompt:str=raw_prompt, index:str=index) -> str:
    """takes a heading (as well as the next one) and produces an ocr cleaning prompt"""
    prompt = raw_prompt.replace('$INDEX', index)
    prompt = prompt.replace('$HEADING', heading)
    prompt = prompt.replace('$NEXT-HEADING', heading_next)
    return prompt

def clean_up_ocr(section:Markdown, next_title:str):
    """generate the section content based on the OCRs"""
    if (section.level > 1) and (len(section.content) == 0):
        # builds the latin extraction prompt for the heading
        prompt = build_prompt(section.title, next_title)
        # queries the model
        latin = model.chat(prompt, documents=[ocr1, ocr2], answer_prefix='<response>', stop_sequences=['</response>'])
        # displays and returns
        print(f"\n{latin}\n")
        section.content = latin

# runs the OCR clean-up
output_markdown.iter(clean_up_ocr, output_path=output_file, display_progress=True)