import os
import re
import time
from typing import List
from pathlib import Path
from anthropic import Anthropic
from anthropic.types import Usage

# model used
model = 'opus'

#----------------------------------------------------------------------------------------
# API

# see: https://docs.anthropic.com/claude/docs/models-overview#claude-3-a-new-generation-of-ai
# https://docs.anthropic.com/claude/reference/rate-limits
client = Anthropic(api_key=os.environ.get('ANTHROPIC_API_KEY'), max_retries=4)
if model == 'haiku':
    MODEL = 'claude-3-haiku-20240307'
    MAX_TOKENS = 4096
    TOKENS_PER_MINUTE = 50000
elif model == 'opus':
    MODEL = 'claude-3-opus-20240229'
    MAX_TOKENS = 4096
    TOKENS_PER_MINUTE = 20000
else:
    raise RuntimeError(f"Model '{model}' is neither 'haiku' nor 'opus'.")

class Throttler:
    """Keeps tokens per minute to the given bounds"""
    def __init__(self, tokenPerMinute:int):
        self.tokenPerMinute: int = tokenPerMinute
        self.last_start_time: float = time.time()
        self.last_token_usage: int = 0
    
    def start(self):
        # wait until we are back to 0 TPM
        time_to_wait = 60 * (self.last_token_usage / self.tokenPerMinute)
        time_waited = time.time() - self.last_start_time
        actual_time_to_wait = max(1, time_to_wait - time_waited)
        if actual_time_to_wait > 60: 
            minutes_to_waits, seconds_to_wait = divmod(int(actual_time_to_wait), 60)
            print(F"Waiting {minutes_to_waits}min{seconds_to_wait}.")
        elif actual_time_to_wait > 1: 
            print(F"Waiting {int(actual_time_to_wait)} seconds.")
        time.sleep(actual_time_to_wait)
        # records this starting time
        self.last_token_usage = 0
        self.last_start_time = time.time()

    def stop(self, usage:Usage):
        # records the usage
        self.last_token_usage = usage.input_tokens + usage.output_tokens

# used to make sure we do not go above our per minute usage
throttler = Throttler(TOKENS_PER_MINUTE)

#----------------------------------------------------------------------------------------
# IO

def read_file(file_path: Path, default_value: str=None) -> str:
    """Reads a given file as a string or returns default value if file does not exist."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        return default_value

def write_file(file_path: Path, content: str):
    """
    Writes a given string to a file, overwriting it if it already exists.
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

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
# PARSING INDEX

def extract_headings(text:str) -> List[str]:
    """takes a string and extract the markdown headings as a list"""
    # Pattern to match Markdown headings: one or more `#` followed by a space and any characters until the end of the line
    pattern = r'^#+\s+(.*)$'
    # Find all matches in the text, using MULTILINE to make `^` and `$` match the start and end of each line
    headings = re.findall(pattern, text, flags=re.MULTILINE)
    # Strip any spaces from the headings
    headings = [heading.strip() for heading in headings]
    return headings

# extract headings
headings = extract_headings(index)

#----------------------------------------------------------------------------------------
# CLEAN UP LATIN

def build_prompt(heading:str, heading_next:str, raw_prompt:str=raw_prompt, index:str=index) -> str:
    """takes a heading (as well as the next one) and produces an ocr cleaning prompt"""
    prompt = raw_prompt.replace('$INDEX', index)
    prompt = prompt.replace('$HEADING', heading)
    prompt = prompt.replace('$NEXT-HEADING', heading_next)
    return prompt

def get_latin_heading(heading:str, next_heading:str) -> str:
    """takes a heading (as well as the next one) and produces a clean modern latin transcription for it"""
    # builds the latin extraction prompt for the heading
    prompt = build_prompt(heading, next_heading)
    # iterates until we are done with this heading
    latin = ""
    stop_reason = 'max_tokens'
    while stop_reason == 'max_tokens':
        # queries the model
        throttler.start()
        answer = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            messages=[
                {"role": "user", "content": # passes the two documents as well as the prompt
                    [{"type": "text", "text": ocr1}, 
                    {"type": "text", "text": ocr2}, 
                    {"type": "text", "text": prompt}
                ]},
                {"role": "assistant", "content": '<response>' + latin} # primes the model to start transcribing
            ],
            stop_sequences=['</response>'] # stop once the latin is written
        )
        throttler.stop(answer.usage)
        # updates our stopping criteria
        stop_reason = answer.stop_reason
        if stop_reason == 'max_tokens': print(f"WARNING: `{heading}` stopped due to max tokens, will take further iterations.")
        # updates our extracted latin
        if len(answer.content) > 1: print(f"WARNING: `answer.content` is of length {len(answer.content)}: {answer.content}")
        latin += answer.content[0].text
    # strips any unneeded spaces and returns
    latin = latin.strip()
    print(f"\n{latin}\n")
    return latin

#----------------------------------------------------------------------------------------
# PROCESS HEADINGS

class Section:
    def __init__(self, title: str = "", content: str = "", level: int = 0, children: list = None):
        self.level = level
        self.title = title.strip()
        self.content = content.strip()
        self.children = [] if (children is None) else children

    def _strip(self):
        """applie strip to all inner nodes"""
        self.title = self.title.strip()
        self.content = self.content.strip()
        for child in self.children:
            child._strip()

    def __str__(self, level=0):
        """converts to a well formatted markdown"""
        md = ''
        # adds the title
        if self.title:
            md += ('#' * self.level) + ' ' + self.title + '\n'
        # adds the body
        if self.content:
            md += '\n' + self.content + '\n'
        # adds the children
        if len(self.children) > 0:
            md += '\n' + '\n\n'.join(child.__str__() for child in self.children)
        return md.strip()

    def __len__(self) -> int:
        return 1 + sum(len(child) for child in self.children)

    @classmethod
    def from_markdown(cls, document: str):
        lines = document.split('\n')

        root = cls(level=0)  # root is a level 0 dummy section
        stack = [root]  # Stack to keep track of section hierarchy

        heading_pattern = re.compile(r'^(#{1,6})\s+(.*)')

        for line in lines:
            heading_match = heading_pattern.match(line)
            if heading_match:
                level = len(heading_match.group(1))
                title = heading_match.group(2).strip()
                new_section = cls(title, level=level)

                # Find correct parent for the new section
                while level <= stack[-1].level:
                    stack.pop()
                stack[-1].children.append(new_section)
                stack.append(new_section)
            else:
                # Add non-heading lines to the content of the current section
                stack[-1].content += '\n' + line

        root._strip()
        return root

def load_latin(output_file:Path) -> str:
    output = read_file(output_file, default_value=index)
    root = Section.from_markdown(output)
    nb_headings = len(root)
    current_heading = 0
    # load the latin recurcively
    def load_latin_rec(section:Section, next_title=None):
        # displays progress
        nonlocal current_heading
        current_heading += 1
        print(f"[{current_heading}/{nb_headings}] Processing '{section.title}'.")
        # load the next title
        if len(section.children) > 0:
            next_title = section.children[0].title
        # load the latin
        if (section.level > 1) and (len(section.content) == 0) and (next_title is not None):
            section.content = get_latin_heading(section.title, next_title)
        # save the results so far
        write_file(output_file, root.__str__())
        # process the children
        if len(section.children) > 0:
            titles = [child.title for child in section.children]
            next_titles = titles[1:] + [next_title]
            for child, next_child_title in zip(section.children, next_titles):
                load_latin_rec(child, next_child_title)
    load_latin_rec(root)
    # return
    return root.__str__()

# Runs on the document
load_latin(output_file)
