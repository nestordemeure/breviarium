from pathlib import Path

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