import os

def write_file(filepath: str, content: str):
    """Writes content to a file, creating directories if needed."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

def read_file(filepath: str) -> str:
    """Reads content from a file."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()
