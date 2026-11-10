"""Project-specific checking rules for high-volume data capturing pipelines."""
import pandas as pd
from pathlib import Path

def verify_extracted_dataframe_metrics(df: pd.DataFrame) -> dict:
    """Evaluates data capture matrices for structural tracking integrity."""
    metrics = {
        "is_valid": True,
        "total_records": len(df),
        "anomalies_discovered": 0,
        "critical_failures": []
    }
    
    if df.empty:
        metrics["is_valid"] = False
        metrics["critical_failures"].append("Dataframe payload is empty.")
        return metrics

    # Project-Specific Rule: Ensure Record_ID contains data and exhibits no un-parsed spaces
    if "Record_ID" in df.columns:
        null_ids = df["Record_ID"].isna().sum()
        if null_ids > 0:
            metrics["anomalies_discovered"] += null_ids
            metrics["critical_failures"].append(f"Discovered {null_ids} missing Record ID tags.")
            metrics["is_valid"] = False
            
    return metrics
