"""Module to handle raw file ingestion and data validation checks."""
from pathlib import Path
from typing import List, Tuple

def read_raw_text_stream(input_file: Path) -> List[str]:
    """Reads lines from an unstructured text file, stripping trailing whitespace."""
    if not input_file.is_file():
        raise FileNotFoundError(f"Target data stream not found: {input_file.name}")
        
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            # Buffer lines into an array while filtering out empty padding rows
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        raise IOError(f"Failed to ingest data stream file: {str(e)}")
