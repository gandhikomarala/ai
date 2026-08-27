import re
from typing import List, Dict, Any

class GitDiffAnalyzer:
    def parse_unified_diff(self, diff_text: str) -> List[Dict[str, Any]]:
        file_diffs = []
        current_file = None
        additions = 0
        deletions = 0
        hunks = []

        for line in diff_text.splitlines():
            if line.startswith("diff --git"):
                if current_file:
                    file_diffs.append({
                        "file_path": current_file,
                        "additions": additions,
                        "deletions": deletions,
                        "hunks": hunks
                    })
                parts = line.split()
                current_file = parts[2].replace("a/", "") if len(parts) > 2 else "unknown"
                additions = 0
                deletions = 0
                hunks = []
            elif line.startswith("+") and not line.startswith("+++"):
                additions += 1
            elif line.startswith("-") and not line.startswith("---"):
                deletions += 1
            elif line.startswith("@@"):
                hunks.append(line)

        if current_file:
            file_diffs.append({
                "file_path": current_file,
                "additions": additions,
                "deletions": deletions,
                "hunks": hunks
            })
        return file_diffs

git_diff_analyzer = GitDiffAnalyzer()
