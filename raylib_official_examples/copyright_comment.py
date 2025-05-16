#!/usr/bin/env python3
"""
Script to migrate comments from C files to Python docstrings.

Scripts generated automatically by tool, so use with care.
"""
import argparse
import difflib
import re
import textwrap
from pathlib import Path
import sys
import logging

REPO_DIR = Path(__file__).parent.parent

def extract_c_comment(c_file):
    """Extract the initial comment block from a C file."""
    try:
        content = c_file.read_text(encoding='utf-8')
        
        # Search for C comment blocks /* ... */
        comment_match = re.match(r'/\*(.*?)\*/', content, re.DOTALL)
        
        if comment_match:
            return comment_match.group(1)
        return None
    except UnicodeDecodeError:
        logging.warning(f"Could not decode {c_file} as UTF-8, trying with latin-1")
        try:
            content = c_file.read_text(encoding='latin-1')
            comment_match = re.match(r'/\*(.*?)\*/', content, re.DOTALL)
            if comment_match:
                return comment_match.group(1)
            return None
        except Exception as e:
            logging.error(f"Failed to read {c_file}: {e}")
            return None

def process_c_comment(comment):
    """Process C comment to create a Python docstring."""
    if not comment:
        return None
    
    # Split into lines and strip whitespace
    lines = comment.strip().split('\n')
    
    # Remove lines containing only asterisks
    filtered_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped and stripped != '*' and not re.match(r'^\*+$', stripped):
            # Remove asterisks at the beginning of the line
            cleaned = re.sub(r'^\s*\*\s?', '', line)
            filtered_lines.append(cleaned)
    
    # Join filtered lines and dedent the entire block to remove common leading whitespace
    joined_text = '\n'.join(filtered_lines)
    dedented_text = textwrap.dedent(joined_text)

    # Split again to add the conversion note
    result_lines = dedented_text.split('\n')
    result_lines.append("")
    result_lines.append("This source has been converted from C raylib examples to Python.")
    
    # Create docstring
    docstring = '"""' + '\n'.join(result_lines) + '\n"""'
    return docstring

def update_python_file(py_file, docstring):
    """Update Python file with new docstring."""
    # Read file content, preserving the final newline if present
    with py_file.open('r', encoding='utf-8') as f:
        content = f.read()

    # Check if the file ends with a newline
    ends_with_newline = content.endswith('\n')

    lines = content.splitlines()
    
    # Find the first import statement
    import_index = -1
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_index = i
            break

    # If an import statement was found, keep only from that point onwards
    if import_index >= 0:
        content = '\n'.join(lines[import_index:])
    else:
        # If no imports found, remove any potential docstrings/comments and keep the rest
        content = content.lstrip()

        # Check if content starts with a docstring
        if content.startswith('"""') or content.startswith("'''"):
            quote_type = '"""' if content.startswith('"""') else "'''"
            end_idx = content.find(quote_type, len(quote_type))

            if end_idx != -1:
                # Remove the docstring and any leading whitespace after it
                content = content[end_idx + len(quote_type):].lstrip()
    
    # Add new docstring and preserve the final newline if it was present
    result = docstring + '\n\n' + content
    if ends_with_newline and not result.endswith('\n'):
        result += '\n'

    return result

def find_matching_c_file(py_file, py_examples_dir, c_examples_dir):
    """
    Find the matching C file for a given Python file with special handling for the gui directory.
    
    Args:
        py_file: Path object for the Python file
        py_examples_dir: Base directory for Python examples
        c_examples_dir: Base directory for C examples
    
    Returns:
        Path object to the matching C file or None if not found
    """
    rel_path = py_file.relative_to(py_examples_dir)
    file_name = py_file.stem
    
    # Special handling for the gui directory
    if rel_path.parts and rel_path.parts[0] == 'gui':
        # Try the nested structure first: gui/name/name.c
        nested_c_file = c_examples_dir / rel_path.parent / file_name / f"{file_name}.c"
        
        if nested_c_file.exists():
            return nested_c_file
        
    # Standard matching: same directory structure with .c extension
    standard_c_file = c_examples_dir / rel_path.with_suffix('.c')
    if standard_c_file.exists():
        return standard_c_file
    
    # If we're here, no matching file was found
    return None

def main():
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(description='Migrate C licensing comments to Python docstrings')
    parser.add_argument('--do', action='store_true', help='Apply changes to files')
    parser.add_argument('-y', '--yes', action='store_true', help='Apply all changes without prompting')
    args = parser.parse_args()
    
    # Paths relative to script directory
    raylib_official_examples = REPO_DIR / 'raylib_official_examples'
    raylib_c_examples = REPO_DIR / 'raylib_c_examples'
    
    # Verify directories exist
    if not raylib_official_examples.exists() or not raylib_c_examples.exists():
        logging.error(f"Directories not found. Looking for {raylib_official_examples} and {raylib_c_examples}")
        return 1
    
    # Find all Python files in raylib_official_examples and subdirectories
    py_files = list(raylib_official_examples.glob('**/*.py'))
    
    processed_count = 0
    updated_count = 0
    
    for py_file in py_files:
        # Ignore the copyright_comment.py script itself
        if py_file.name == 'copyright_comment.py':
            continue
            
        # Find the corresponding C file with special handling for gui directory
        c_file = find_matching_c_file(py_file, raylib_official_examples, raylib_c_examples)
        
        # Verify the C file exists
        if not c_file:
            rel_path = py_file.relative_to(raylib_official_examples)
            logging.warning(f"No corresponding C file found for {rel_path}")
            continue
        
        processed_count += 1
        
        # Extract comment from C file and generate docstring
        c_comment = extract_c_comment(c_file)
        if not c_comment:
            logging.warning(f"No comment found in {c_file}")
            continue
        
        docstring = process_c_comment(c_comment)
        new_content = update_python_file(py_file, docstring)
        original_content = py_file.read_text(encoding='utf-8')
        
        # Check if content would actually change with more accurate comparison
        if new_content == original_content:
            rel_path = py_file.relative_to(raylib_official_examples)
            logging.info(f"No changes needed for {rel_path}")
            continue
            
        updated_count += 1
        rel_path = py_file.relative_to(raylib_official_examples)
        
        if args.do:
            # When --do is passed but --yes is not, prompt for confirmation
            if not args.yes:
                # Display diff first
                print(f"Diff for: {rel_path}")
                diff = difflib.unified_diff(
                    original_content.splitlines(keepends=True),
                    new_content.splitlines(keepends=True),
                    fromfile=str(rel_path),
                    tofile=str(rel_path) + ' (updated)'
                )
                sys.stdout.writelines(diff)

                # Ask for confirmation
                while True:
                    response = input(f"\nUpdate {rel_path}? [y/N]: ").lower()
                    if response in ('y', 'yes'):
                        # Save updated Python file
                        py_file.write_text(new_content, encoding='utf-8')
                        logging.info(f"Updated: {rel_path}")
                        break
                    elif response in ('', 'n', 'no'):
                        logging.info(f"Skipped: {rel_path}")
                        break
                    else:
                        print("Please answer 'y' or 'n'")
            else:
                # Save updated Python file without prompting
                py_file.write_text(new_content, encoding='utf-8')
                logging.info(f"Updated: {rel_path}")
        else:
            # Display diff
            print(f"Diff for: {rel_path}")
            diff = difflib.unified_diff(
                original_content.splitlines(keepends=True),
                new_content.splitlines(keepends=True),
                fromfile=str(rel_path),
                tofile=str(rel_path) + ' (updated)'
            )
            sys.stdout.writelines(diff)
            print()
    
    logging.info(f"Processed {processed_count} files, {updated_count} (would be) updated")
    return 0

if __name__ == "__main__":
    sys.exit(main())
