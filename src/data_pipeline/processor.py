"""Module to parse text blocks and build structured DataFrames."""
from typing import List, Dict, Any
import pandas as pd

def transform_lines_to_dataframe(raw_lines: List[str]) -> pd.DataFrame:
    """Parses sequential data blocks into a structured and deduplicated DataFrame."""
    records: List[Dict[str, Any]] = []
    current_record: Dict[str, Any] = {}
    current_key = None

    for line in raw_lines:
        if line.startswith("RECORD_ID:"):
            if current_record:
                records.append(current_record)
            current_record = {
                "Record_ID": line.split(":", 1)[1].strip(),
                "Category": "", "Question_Text": "",
                "Option_A": "", "Option_B": "", "Option_C": "", "Option_D": "",
                "Correct_Answer": "", "Explanation": ""
            }
            current_key = "Record_ID"
        elif line.startswith("CATEGORY:") and current_record:
            current_record["Category"] = line.split(":", 1)[1].strip()
            current_key = "Category"
        elif line.startswith("QUESTION:") and current_record:
            current_record["Question_Text"] = line.split(":", 1)[1].strip()
            current_key = "Question_Text"
        elif line.startswith("OPTIONS:") and current_record:
            current_key = "Options_List"
        elif line.startswith("A)") and current_record:
            current_record["Option_A"] = line.split(")", 1)[1].strip()
            current_key = "Option_A"
        elif line.startswith("B)") and current_record:
            current_record["Option_B"] = line.split(")", 1)[1].strip()
            current_key = "Option_B"
        elif line.startswith("C)") and current_record:
            current_record["Option_C"] = line.split(")", 1)[1].strip()
            current_key = "Option_C"
        elif line.startswith("D)") and current_record:
            current_record["Option_D"] = line.split(")", 1)[1].strip()
            current_key = "Option_D"
        elif line.startswith("CORRECT_ANSWER:") and current_record:
            current_record["Correct_Answer"] = line.split(":", 1)[1].strip()
            current_key = "Correct_Answer"
        elif line.startswith("EXPLANATION:") and current_record:
            current_record["Explanation"] = line.split(":", 1)[1].strip()
            current_key = "Explanation"
        else:
            if current_record and current_key and current_key in current_record:
                current_record[current_key] += " " + line

    if current_record:
        records.append(current_record)

    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)
    # Deduplicate matching indices
    df.drop_duplicates(subset=["Record_ID"], keep="first", inplace=True)
    return df
