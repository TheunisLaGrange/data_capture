"""Module to handle workbook formatting and data exportation functions."""
from pathlib import Path
import pandas as pd

def write_dataframe_to_excel(df: pd.DataFrame, output_path: Path) -> None:
    """Writes a Pandas DataFrame to an Excel spreadsheet file with distinct formatting."""
    if df.empty:
        raise ValueError("Cannot export an empty dataset.")
        
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Flush structured matrix directly out to worksheet
        df.to_excel(output_path, index=False, sheet_name="Data Capture Log")
    except Exception as e:
        raise IOError(f"Excel generation failure: {str(e)}")