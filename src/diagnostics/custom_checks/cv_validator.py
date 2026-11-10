"""Validation rules engine specifically for CV layout data formats."""

def validate_cv_json_schema(cv_data: dict) -> dict:
    """Evaluates the professional experience and key skills inside a custom json template."""
    report = {"is_valid": True, "missing_keys": [], "empty_fields": []}
    
    # Strict validation rules for the AI CV Generator profile format
    mandatory_nodes = ["name", "professional_summary", "key_skills", "professional_experience"]
    
    for node in mandatory_nodes:
        if node not in cv_data:
            report["missing_keys"].append(node)
            report["is_valid"] = False
        elif not cv_data[node]:
            report["empty_fields"].append(node)
            
    return report
