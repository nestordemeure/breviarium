"""
Insures that the text reads well
"""
from pathlib import Path
from breviarum.io import read_file
from breviarum.markdown import Markdown
from breviarum.model import Human, Haiku, Opus

# model used
model = Opus()

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# English
english_file = data_folder / 'english.md'
english = read_file(english_file)
english_markdown = Markdown.from_text(english)

# index
index_folder = data_folder / 'index'
english_index_file = index_folder / 'translated_index.md'
english_index = read_file(english_index_file)

# prompt
prompt_folder = data_folder / 'prompt'
prompt_file = prompt_folder / 'check_readability.md'
raw_prompt = read_file(prompt_file)

# Output
output_file = data_folder / 'readable.md'
output = read_file(output_file, default_value=english_index)
output_markdown = Markdown.from_text(output)

#----------------------------------------------------------------------------------------
# CHECK

def build_prompt(english_content:str, raw_prompt:str=raw_prompt) -> str:
    prompt = raw_prompt.replace('$ENGLISH', english_content)
    return prompt

def check_readability(output_node:Markdown, english_node:Markdown, next_title:str):
    """Check the readability of the text section per section"""
    # if the section has not been processed yet and has english content
    if (len(output_node.content) == 0) and (len(english_node.content) != 0):
        # builds the checking prompt
        prompt = build_prompt(english_node.content)
        # queries the model
        check = model.chat(prompt)
        # simplifies Matching answers
        if 'Readable' in check: check = 'Readable.'
        # displays and returns
        print(f"\n{check}\n")
        output_node.content = check

# checks the text
output_markdown.iter(check_readability, other_markdowns=english_markdown, 
                    output_path=output_file, display_progress=True)