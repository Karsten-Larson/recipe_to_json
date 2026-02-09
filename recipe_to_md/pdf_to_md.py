from pathlib import Path
from markitdown import MarkItDown

def convert(file_path: Path) -> str:
    md = MarkItDown(enable_plugins=False)
    result = md.convert(file_path)
    text = result.text_content

    return text