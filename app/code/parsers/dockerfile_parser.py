"""AST & Symbol Table Parser for Dockerfile."""
from typing import Dict, Any, List

class DockerfileParser:
    """Extracts symbols, function signatures, classes, imports, and docstrings for dockerfile codebases."""
    
    def __init__(self):
        self.language = "dockerfile"

    def parse(self, source_code: str) -> Dict[str, Any]:
        lines = source_code.splitlines()
        functions = []
        classes = []
        imports = []
        
        for idx, line in enumerate(lines):
            line_str = line.strip()
            if line_str.startswith("def ") or line_str.startswith("func ") or line_str.startswith("function "):
                name = line_str.split("(")[0].split()[-1]
                functions.append({"name": name, "line": idx + 1})
            elif line_str.startswith("class ") or line_str.startswith("type ") or line_str.startswith("struct "):
                name = line_str.split()[1] if len(line_str.split()) > 1 else "Unknown"
                classes.append({"name": name, "line": idx + 1})
            elif line_str.startswith("import ") or line_str.startswith("from ") or line_str.startswith("use "):
                imports.append(line_str)

        return {
            "language": self.language,
            "total_loc": len(lines),
            "functions": functions,
            "classes": classes,
            "imports": imports
        }
