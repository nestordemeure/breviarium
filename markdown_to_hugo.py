"""
Takes a markdown file and produces a Hugo folder hierarchy.
"""
import re
import shutil
from pathlib import Path
from breviarum.io import read_file, write_file
from breviarum.markdown import Markdown

#----------------------------------------------------------------------------------------
# LOADING DATA

# where all the data is stored
data_folder = Path('./data')

# input
input_file = data_folder / 'english.md'
input = read_file(input_file)
markdown = Markdown.from_text(input)

# output folder
output_folder = data_folder / 'hugo'

#----------------------------------------------------------------------------------------
# FILENAME OF TITLE

def remove_stop_words(text_list):
    # List of common English+Latin stop words
    english_stop_words = [
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours",
        "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
        "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
        "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are",
        "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
        "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as",
        "until", "while", "of", "at", "by", "for", "with", "about", "against", "between",
        "into", "through", "during", "before", "after", "above", "below", "to", "from",
        "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don",
        "should", "now"]
    latin_stop_words = [
        "a", "ab", "ac", "ad", "at", "atque", "aut", "autem", "cum", "de", "dum", "e", "ex",
        "et", "etiam", "enim", "ergo", "est", "et", "hic", "haec", "hoc", "id", "ille",
        "illa", "illud", "in", "inter", "ipsum", "ipsa", "ipso", "ita", "me", "mihi",
        "nec", "necque", "neque", "nisi", "non", "nos", "noster", "nostri", "nostra", 
        "nostrum", "quam", "quae", "qui", "quibus", "quid", "quidem", "quo", "quod",
        "quos", "sed", "si", "sic", "sunt", "sum", "tamen", "tibi", "tu", "tuum", "tua",
        "tuo", "te", "ut", "ubi", "vel", "vero"]
    stop_words = set(english_stop_words + latin_stop_words)

    # Filter the list to exclude any words that are in the stop words set
    filtered_list = [word for word in text_list if word not in stop_words]
    return filtered_list

def id_of_str(title:str):
    # simplifies the string
    title = re.sub(r'[^a-zA-Z0-9 ]', '', title)
    title = title.lower()

    # Split the string into words
    words = title.split()

    # remove stop words
    words = [word for word in words if word not in {'i', 'ii', 'iii', 'iv', 'v'}]
    words_filtered = remove_stop_words(words)
    if (len(words_filtered) > 0) and (len(words) > 2):
        words = words_filtered

    if len(words) < 1:
        # no word found, return the string intact
        return title
    elif len(words) < 2:
        # only one word anyway
        return words[0]
    else:
        # gets the longest consecutive pair of words
        id = None
        id_length = 0
        for i in range(len(words) - 1):
            new_id_length = len(words[i]) + len(words[i+1])
            if new_id_length > id_length:
                id = f"{words[i]} {words[i+1]}"
                id_length = new_id_length
        return id

#----------------------------------------------------------------------------------------
# PROCESSING THE FILE

def create_hugo_rec(node: Markdown, folder: Path, priority:int=0):
    # splits node's children
    file_children = [child for child in node.children if (child.level > 3)] # printed in the same file
    rec_children = [child for child in node.children if (child.level <= 3)] # printed in a new file
    # content to be printed to file
    content = '---\n'
    content += f'title: "{node.title}"\n'
    content += 'draft: false\n'
    content += 'comments: false\n'
    content += f'weight: {-priority}\n'
    content += 'images:\n'
    content += '---\n'
    if (node.content != ""):
        content += '\n' + node.content
    for child in file_children:
        content += '\n\n' + child.__str__()
    # unique id that will be used for naming file or folder
    name = id_of_str(node.title)
    if priority > 0: name = str(priority) + ' ' + name
    # create the corresponding file or folder
    if (len(rec_children) == 0):
        # no children, write to file
        write_file(folder / f"{name}.md", content)
    else:
        # children, create a folder with an index file and subfiles
        sub_folder = folder / name
        sub_folder.mkdir(parents=True)
        # create index file
        write_file(sub_folder / "_index.md", content)
        # create children
        for child_priority, child in enumerate(rec_children, start=1):
            create_hugo_rec(child, sub_folder, child_priority)

#----------------------------------------------------------------------------------------
# MAIN

# creates a dedicated output folder
# purging any previous folder by the same name
output_folder = output_folder / input_file.stem
if output_folder.exists():
    shutil.rmtree(output_folder)
output_folder.mkdir(parents=True)

# gets to the title heading
markdown = markdown.children[0]

# creates the hugo files
create_hugo_rec(markdown, output_folder)
