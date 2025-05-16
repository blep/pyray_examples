#!/usr/bin/env python3
"""
Identifies working Python examples by comparing a list of all examples
against a list of examples with known migration issues.

This script scans a specified directory for all '.py' example files,
reads a markdown file to identify examples with issues, and then
computes the set of working examples. The paths of working examples
and examples with issues are written to separate text files.
Finally, it prints a summary of the findings.
"""
import argparse
from pathlib import Path
import re
from typing import Set

THIS_DIR: Path = Path(__file__).parent
REPO_DIR: Path = THIS_DIR.parent

EXAMPLES_DIR_NAME: str = "raylib_official_examples"
MIGRATION_ISSUES_FILENAME: str = "migration_issues.md"
OUTPUT_WORKING_FILENAME: str = "examples_list_working.txt"
OUTPUT_ISSUES_FILENAME: str = "examples_list_with_issues.txt"


def scan_all_examples(examples_base_dir: Path, repo_dir: Path) -> Set[str]:
    """Scans the directory for all .py example files."""
    all_examples_paths: Set[str] = set()
    if examples_base_dir.is_dir():
        for py_file in examples_base_dir.rglob("*.py"):
            if py_file.resolve() != Path(__file__).resolve():  # Exclude self
                all_examples_paths.add(py_file.relative_to(repo_dir).as_posix())
    else:
        print(f"WARNING: Examples directory {examples_base_dir} not found.")
    return all_examples_paths


def get_issue_examples(migration_issues_file: Path, all_examples: Set[str]) -> Set[str]:
    """Reads the migration issues file and returns a set of issue example paths."""
    issue_examples_paths_from_md: Set[str] = set()
    if migration_issues_file.is_file():
        content: str = migration_issues_file.read_text(encoding="utf-8")
        path_pattern = re.escape(EXAMPLES_DIR_NAME) + r"/[^\s`\)]+\.py"
        found_paths: list[str] = re.findall(r"[\s`\(]?(" + path_pattern + r")[\s`\)]?", content)
        for path in found_paths:
            issue_examples_paths_from_md.add(path)
    else:
        raise ValueError(f'File {migration_issues_file} not found.')

    # Filter to only include paths that are actual examples
    actual_issue_examples: Set[str] = {
        path for path in issue_examples_paths_from_md if path in all_examples
    }
    return actual_issue_examples


def _save_path_set_to_file(paths_set: Set[str], output_dir: Path, filename: str, repo_dir: Path
                           ) -> None:
    """Helper function to save a set of paths to a file.
    Paths are made relative to output_dir (THIS_DIR) before writing."""
    output_file: Path = output_dir / filename

    # Convert paths to be relative to output_dir (THIS_DIR)
    # Original paths are relative to repo_dir
    paths_relative_to_output_dir = [
        (repo_dir / path_str).resolve().relative_to(output_dir.resolve()).as_posix()
        for path_str in sorted(list(paths_set))
    ]
    content = "\n".join(paths_relative_to_output_dir) + "\n"
    output_file.write_text(content, encoding="utf-8")
    print(f"List of paths written to: {output_file}")


def main() -> None:
    """
    Main function to identify and list working examples.
    """
    parser = argparse.ArgumentParser(description="Identifies working pyray examples.")
    _ = parser.parse_args()

    examples_base_dir: Path = REPO_DIR / EXAMPLES_DIR_NAME
    migration_issues_file: Path = THIS_DIR / MIGRATION_ISSUES_FILENAME

    all_examples_paths: Set[str] = scan_all_examples(examples_base_dir, REPO_DIR)

    if not all_examples_paths:
        print("\nNo examples found in the specified directory.")
        return

    actual_issue_examples_paths: Set[str] = get_issue_examples(migration_issues_file, all_examples_paths)

    working_examples_paths: Set[str] = all_examples_paths - actual_issue_examples_paths

    _save_path_set_to_file(working_examples_paths, THIS_DIR, OUTPUT_WORKING_FILENAME, REPO_DIR)
    _save_path_set_to_file(actual_issue_examples_paths, THIS_DIR, OUTPUT_ISSUES_FILENAME, REPO_DIR)

    num_working: int = len(working_examples_paths)
    num_total: int = len(all_examples_paths)

    # num_total is checked by the early return if all_examples_paths is empty
    percentage_working: float = (num_working / num_total) * 100
    print(f"\n{num_working}/{num_total} (~{percentage_working:.0f}%) examples work without issues.")


if __name__ == "__main__":
    main()
