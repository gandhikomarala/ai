import ast
import re
from typing import List, Dict, Any

class CodeASTParser:
    def parse_python(self, code: str) -> Dict[str, Any]:
        try:
            tree = ast.parse(code)
            classes = []
            functions = []
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    classes.append({
                        "name": node.name,
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "docstring": ast.get_docstring(node) or ""
                    })
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append({
                        "name": node.name,
                        "start_line": node.lineno,
                        "end_line": getattr(node, "end_lineno", node.lineno),
                        "docstring": ast.get_docstring(node) or "",
                        "is_async": isinstance(node, ast.AsyncFunctionDef)
                    })
                elif isinstance(node, ast.Import):
                    for n in node.names:
                        imports.append(n.name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(node.module or "")
            return {
                "language": "python",
                "classes": classes,
                "functions": functions,
                "imports": list(set(imports)),
                "total_loc": len(code.splitlines())
            }
        except Exception as e:
            return {"language": "python", "error": str(e), "total_loc": len(code.splitlines())}

    def parse_generic(self, code: str, language: str) -> Dict[str, Any]:
        # Regex-based symbol extraction for TypeScript, Go, Java
        func_patterns = re.findall(r"(?:export\s+)?(?:async\s+)?function\s+([a-zA-Z0-9_]+)|func\s+([a-zA-Z0-9_]+)", code)
        class_patterns = re.findall(r"class\s+([a-zA-Z0-9_]+)", code)
        symbols = [f[0] or f[1] for f in func_patterns if f[0] or f[1]]
        return {
            "language": language,
            "classes": [{"name": c} for c in class_patterns],
            "functions": [{"name": s} for s in symbols],
            "total_loc": len(code.splitlines())
        }

code_ast_parser = CodeASTParser()
