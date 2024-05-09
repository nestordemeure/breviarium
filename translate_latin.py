"""
Takes Latin and produces English.
"""
from pathlib import Path
from breviarum.io import read_file, write_file
from breviarum.markdown import Markdown
from breviarum.model import Human, Haiku, Opus

# model used
model = Opus()

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# Latin
latin_file = data_folder / 'latin_simplified.md'
latin = read_file(latin_file)
latin_markdown = Markdown.from_text(latin)

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
output = read_file(output_file, default_value=english_index)
english_markdown = Markdown.from_text(output)

#----------------------------------------------------------------------------------------
# TRANSLATE

def build_prompt(latin_heading:str, english_heading:str, heading_next:str, raw_prompt:str=raw_prompt) -> str:
    """takes a heading (as well as the next one) and produces an ocr cleaning prompt"""
    prompt = raw_prompt.replace('$LATIN-HEADING', latin_heading)
    prompt = prompt.replace('$ENGLISH-HEADING', english_heading)
    prompt = prompt.replace('$NEXT-HEADING', heading_next)
    return prompt

def translate_latin(latin_node:Markdown, english_node:Markdown, next_title:str):
    """Does the translation from Latin to English"""
    if (latin_node.level > 1) and (len(english_node.content) == 0):
        # builds the translation prompt from the headings
        prompt = build_prompt(latin_node.title, english_node.title, next_title)
        # queries the model
        english = english_markdown.__str__() # current version of the translation
        translation = model.chat(prompt, documents=[latin, english], answer_prefix='<response>', stop_sequences=['</response>'])
        # displays and returns
        print(f"\n{translation}\n")
        english_node.content = translation

# translates the text
latin_markdown.iter(translate_latin, other_markdowns=english_markdown, 
                    output_path=output_file, display_progress=True)