from __future__ import annotations # for Markdown type in definition of method of the Markdown class
import re
from pathlib import Path
from typing import Union, List
from .io import write_file

class Markdown:
    """Tree representation for a Markdown file and its headings"""
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

    def __str__(self) -> str:
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
        """Size fo the tree, counting its leaves"""
        return 1 + sum(len(child) for child in self.children)

    def iter(self, f, other_markdowns:Union[Markdown, List[Markdown]]=[], 
             output_path:Path=None, last_title='the end', display_progress=False):
        """
        Iterates over a Markdown structure, applying the function `f` to each node.

        Parameters:
        - `f`: the function to apply to each Markdown node (signature: `f(node:Markdown, **other_nodes:Markdown, next_title:str) -> None`)
        - `other_markdowns` (optional, default to []): one, or a list of, markdown to be processed along the primary one
        - `output_path` (optional): where to save intermediate results
        - `last_title` (optional, default to 'the end'): title used for the last node in the sequence
        - `display_progress` (optional, default to False): should we display progress as we go?
        """
        # information needed to dipslay progress
        nb_headings = len(self)
        current_heading = 0
        # recurcive function called
        def iter_rec(node:Markdown, other_nodes:List[Markdown], last_title:str):
            # display progress
            if display_progress:
                nonlocal current_heading
                current_heading += 1
                print(f"[{current_heading}/{nb_headings}] Processing '{node.title}'.")
            # load the next title
            next_titles = [child.title for child in node.children] + [last_title]
            next_title = next_titles[0]
            # runs the function
            f(node, *other_nodes, next_title)
            # saves intermediate result
            if output_path is not None:
                write_file(output_path, self.__str__())
            # runs on children
            for i in range(len(node.children)):
                child = node.children[i]
                other_children = [other_node.children[i] for other_node in other_nodes]
                child_title = next_titles[i+1]
                iter_rec(child, other_children, child_title)
        # runs the function recurcively
        other_nodes = other_markdowns if isinstance(other_markdowns, List) else [other_markdowns]
        iter_rec(self, other_nodes, last_title)

    @classmethod
    def from_text(cls, document: str):
        """Import a string as a tree."""
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