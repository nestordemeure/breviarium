import re

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