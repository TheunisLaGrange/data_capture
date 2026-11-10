import os
import sys
import asyncio
from pathlib import Path

# Connect to your new custom modular components
from src.data_pipeline.loader import read_raw_text_stream
from src.data_pipeline.processor import transform_lines_to_dataframe
from src.data_pipeline.exporter import write_dataframe_to_excel

PROJECT_ROOT = Path(__file__).resolve().parent

# =====================================================================
# 🖥️ APPLICATION INTERFACE / EXTENSION ZONE (GUI HOOKS)
# =====================================================================
# >>> START GUI PLUGINS >>>
# >>> END GUI PLUGINS >>>

async def run_pipeline_orchestration():
    print("🔬 Launching modular data capture orchestration framework...")
    
    # 1. Establish workspace directory paths
    input_file = PROJECT_ROOT / "User_Data" / "industrial_engineering_questions_100.txt"
    output_excel = PROJECT_ROOT / "Output" / "captured_questions.xlsx"
    
    try:
        # Phase 1: Ingestion
        print(f"[STAGE 1] Ingesting text streams from: {input_file.name}")
        raw_lines = read_raw_text_stream(input_file)
        
        # Phase 2: Processing & Data Transformation
        print(f"[STAGE 2] Running data parsing and matrix transformations...")
        df = transform_lines_to_dataframe(raw_lines)
        print(f"   -> Extracted data shape: {df.shape}")
        
        # Phase 3: Exporting
        print(f"[STAGE 3] Exporting worksheet matrix to disk: {output_excel.name}")
        write_dataframe_to_excel(df, output_excel)
        
        print("\n============================================================")
        print("🎉 PIPELINE COMPLETED SUCCESSFULLY WITH MODULAR PACKAGES")
        print("============================================================\n")

    except Exception as e:
        print(f"❌ [CRITICAL PIPELINE EXCEPTION]: {str(e)}")

if __name__ == "__main__":
    # If your boilerplate scripts inject a GUI class later, it launches from here
    if 'initialize_desktop_window' in globals():
        globals()['initialize_desktop_window']()
    else:
        asyncio.run(run_pipeline_orchestration())
        input("\n[Execution Concluded] Press Enter to exit workspace...")
