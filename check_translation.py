"""
Takes the English translation and checks it paragraph per paragraph.
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

# Latin
latin_file = data_folder / 'latin_simplified.md'
latin = read_file(latin_file)
latin_markdown = Markdown.from_text(latin)

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
prompt_file = prompt_folder / 'check_translation.md'
raw_prompt = read_file(prompt_file)

# Output
output_file = data_folder / 'translation_check.md'
output = read_file(output_file, default_value=english_index)
output_markdown = Markdown.from_text(output)

#----------------------------------------------------------------------------------------
# CHECK

def build_prompt(latin_content:str, english_content:str, raw_prompt:str=raw_prompt) -> str:
    prompt = raw_prompt.replace('$LATIN', latin_content)
    prompt = prompt.replace('$ENGLISH', english_content)
    return prompt

def check_translation(output_node:Markdown, english_node:Markdown, latin_node:Markdown, next_title:str):
    """Check the translation section per section"""
    # if the section has not been processed yet and has english content
    if (len(output_node.content) == 0) and (len(english_node.content) != 0):
        # builds the checking prompt from the headings
        prompt = build_prompt(latin_node.content, english_node.content)
        # queries the model
        check = model.chat(prompt, answer_prefix='<response>', stop_sequences=['</response>'])
        # simplifies Matching answers
        if 'Matching' in check: check = 'Matching'
        # displays and returns
        print(f"\n{check}\n")
        output_node.content = check

# checks the text
output_markdown.iter(check_translation, other_markdowns=[latin_markdown,english_markdown], 
                    output_path=output_file, display_progress=True)