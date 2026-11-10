# =====================================================================
# 🧪 BOILERPLATE CACHE-PROTECTED APPLICATION SANDBOX (MASTER TEMPLATE)
# =====================================================================
import os
import sys
import json
import hashlib
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

SANDBOX_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SANDBOX_DIR.parent
CACHE_DIR = PROJECT_ROOT / ".data_cache"

os.chdir(PROJECT_ROOT)
load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

def calculate_content_hash(*inputs: str) -> str:
    """Generates a unique validation hash from arbitrary text inputs to check for modifications."""
    combined = "".join(inputs).encode("utf-8")
    return hashlib.md5(combined).hexdigest()

# >>> INJECTED LOGIC BOILERPLATE START >>>
# >>> START SANDBOX LOGIC >>>
def execute_high_volume_capture(input_file: Path, output_excel: Path) -> bool:
    """
    High-volume text parser that scales cleanly across large datasets.
    Extracts structured text data blocks into a tabular Pandas DataFrame matrix.
    """
    if not input_file.exists():
        print(f"[ERROR] Target data dump stream not discovered at: {input_file}")
        return False

    records = []
    current_record = {}
    current_key = None
    line_idx = 0
    
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            for line_idx, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                if line.startswith("RECORD_ID:"):
                    if current_record:
                        records.append(current_record)
                    current_record = {
                        "Record_ID": line.split(":", 1)[1].strip(),
                        "Category": "",
                        "Question_Text": "",
                        "Option_A": "",
                        "Option_B": "",
                        "Option_C": "",
                        "Option_D": "",
                        "Correct_Answer": "",
                        "Explanation": ""
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

        print(f"[PARSER] Ingestion complete. Raw records discovered: {len(records)}")

        if not records:
            print("[WARN] No valid records extracted from file template structures.")
            return False

        df = pd.DataFrame(records)
        df.drop_duplicates(subset=["Record_ID"], keep="first", inplace=True)
        
        print(f"[CLEAN] Formatted structured matrix dimension: {df.shape}")
        df.to_excel(output_excel, index=False, sheet_name="Captured Data Database")
        print(f"[SUCCESS] Excel workbook successfully deployed to: {output_excel}")
        return True

    except Exception as e:
        print(f"[CRITICAL] Error parsing text records on line {line_idx}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
# <<< END SANDBOX LOGIC <<<
# >>> INJECTED LOGIC BOILERPLATE END >>>

def run_isolated_task():
    print("🔬 Smart Sandbox Room: Initializing local workspace data registers...")
    CACHE_DIR.mkdir(exist_ok=True)
    
    user_data_dir = PROJECT_ROOT / "User_Data"
    output_dir = PROJECT_ROOT / "Output"
    
    user_data_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)

    while True:
        print(f"\n📂 Available data sources in User_Data: {[f.name for f in user_data_dir.glob('*.txt')]}")
        input_file = input("Please enter the name of the input file (e.g., questions_dump.txt) or type 'exit': ").strip()
        
        if input_file.lower() == 'exit':
            print("❌ Pipeline execution aborted by user choice.")
            return

        INPUT_PATH = user_data_dir / input_file
        if INPUT_PATH.is_file():
            print(f"✅ Target validation check passed: Linked to file entry stream.")
            break
        else:
            print(f"⚠️ [ERROR]: File path entry target does not exist: {INPUT_PATH.name}")

    OUTPUT_PATH = output_dir / "captured_questions.xlsx"
    handshake_success = execute_high_volume_capture(INPUT_PATH, OUTPUT_PATH)
    print(f"\n📊 Pipeline operational completion handshake code: {handshake_success}")
    
if __name__ == "__main__":
    run_isolated_task()
    input("\n[Sandbox Script Concluded] Press Enter to safely exit terminal loop...")
