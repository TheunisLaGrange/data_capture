"""
Project Structural Auditor and Artifact Generator.
Analyzes directory trees and files to auto-update README, requirements, and gitignore.
"""
import os
import re
from pathlib import Path
from typing import Set

class WorkspaceAuditor:
    def __init__(self, root_dir: Path):
        self.root = Path(root_dir)
        self.project_name = self.root.name

    def scan_directory_tree(self) -> str:
        """Generates a clean text-based visualization of the active project structure."""
        lines = []
        # Rules to skip noisy or hidden development caches
        skip_dirs = {".git", "__pycache__", ".data_cache", ".venv"}
        
        def _build_tree(dir_path: Path, prefix: str = ""):
            try:
                items = sorted(list(dir_path.iterdir()), key=lambda x: (x.is_file(), x.name.lower()))
                for idx, item in enumerate(items):
                    if item.is_dir() and item.name in skip_dirs:
                        continue
                    
                    is_last = (idx == len(items) - 1)
                    connector = "└── " if is_last else "├── "
                    lines.append(f"{prefix}{connector}{item.name}")
                    
                    if item.is_dir():
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        _build_tree(item, next_prefix)
            except PermissionError:
                pass

        lines.append(f"📁 {self.project_name}/")
        _build_tree(self.root)
        return "\n".join(lines)

    def extract_functional_dependencies(self) -> Set[str]:
        """Scans all Python files to extract external third-party module imports."""
        dependencies = set()
        # Baseline modules built into standard Python that don't need tracking in requirements.txt
        std_lib = {
            "os", "sys", "pathlib", "asyncio", "logging", "json", "hashlib", 
            "re", "uuid", "abc", "typing", "traceback", "time"
        }
        
        for py_file in self.root.rglob("*.py"):
            if ".venv" in py_file.parts or "__pycache__" in py_file.parts:
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                # Locate top-level absolute imports
                for match in re.finditer(r"^\s*(?:import|from)\s+([a-zA-Z0-9_]+)", content, re.MULTILINE):
                    module = match.group(1)
                    if module not in std_lib and not (self.root / "src" / module).exists():
                        dependencies.add(module)
            except Exception:
                pass
        return dependencies

    def refactor_requirements_manifest(self, deps: Set[str]):
        """Dynamically tracks and updates requirements.txt with third-party module versions."""
        requirements_path = self.root / "requirements.txt"
        
        # Professional standard tracking versions tailored for your pipeline layout
        version_mappings = {
            "pandas": "pandas>=2.2.0",
            "openpyxl": "openpyxl>=3.1.0",
            "google": "google-genai>=1.0.0",
            "pydantic": "pydantic>=2.0.0",
            "yaml": "PyYAML>=6.0.0",
            "reportlab": "reportlab>=4.0.0",
            "pypdf": "pypdf>=4.0.0",
            "dotenv": "python-dotenv>=1.0.0"
        }
        
        compiled_lines = []
        for dep in sorted(list(deps)):
            dep_lower = dep.lower()
            if dep_lower in version_mappings:
                compiled_lines.append(version_mappings[dep_lower])
            else:
                # Fallback for unexpected or custom dependencies found in code
                compiled_lines.append(f"{dep}>=1.0.0")
                
        if compiled_lines:
            requirements_path.write_text("\n".join(compiled_lines) + "\n", encoding="utf-8")
            print(f"[AUDITOR] Dynamic requirements.txt refactored at: {requirements_path.name}")
        else:
            print("[AUDITOR] No external dependencies detected; skipping requirements.txt rewrite.")

    def refactor_markdown_documentation(self, tree_str: str, deps: Set[str]):
        """Generates a professional README file featuring the active directory layout tree."""
        readme_path = self.root / "README.md"
        dep_list = "\n".join([f"* `{d}`" for d in deps]) if deps else "* Pure standard library dependencies only."
        
        content = f"""# {self.project_name}

Modular, production-grade automation system developed with strict data-isolation patterns.

## 🛠️ Repository Architecture Map
```text
{tree_str}
```

## 📦 Extracted Module Dependencies
{dep_list}

## 🚀 Execution Loop Instantiation
Ensure your local environment configuration variables (`.env`) match runtime criteria, then launch via:
```bash
python main.py
```
*Generated automatically by WorkspaceAuditor before deployment.*
"""
        readme_path.write_text(content.strip(), encoding="utf-8")
        print(f"[AUDITOR] Professional README.md refactored at: {readme_path.name}")

    def execute_pre_flight_audit(self):
        """Orchestrates sequential execution of all artifact refactoring phases."""
        print(f"[AUDITOR] Initializing repository architecture scan for: {self.project_name}")
        tree_str = self.scan_directory_tree()
        deps = self.extract_functional_dependencies()
        
        self.refactor_requirements_manifest(deps)
        self.refactor_markdown_documentation(tree_str, deps)
        print("[AUDITOR] Pre-flight structural validation complete. Ready for GitHub push.")

if __name__ == "__main__":
    # Anchored tightly to the active deployment directory path
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
    auditor = WorkspaceAuditor(PROJECT_ROOT)
    auditor.execute_pre_flight_audit()
