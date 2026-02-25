#!/usr/bin/env python3
import os
import fnmatch
from pathlib import Path

# -------------------------------------------------------------------------
# CONFIGURATION
# -------------------------------------------------------------------------

# Exclusion list populated for DRF (Django Rest Framework) + Next.js
# Supports exact names and wildcards (e.g., *.pyc)
EXCLUSIONS = [
    # General / Git
    '.git',
    '.gitignore',
    '.DS_Store',       # macOS specific
    '.idea',           # JetBrains
    '.vscode',         # VS Code

    # Python / Django (DRF)
    '__pycache__',
    '*.pyc',
    '*.pyo',
    'venv',
    '.venv',
    'env',
    'db.sqlite3',      # Usually don't want to list the binary db file
    '.env',            # Secrets file
    'media',           # User uploaded files (often too large to list)
    'staticfiles',     # Collected static files

    # Next.js / Node
    'node_modules',
    '.next',           # Next.js build output
    'coverage',        # Test coverage
    'build',           # Generic build folder
    'dist',            # Generic dist folder
    'package-lock.json', # Optional: makes tree noisy
    'yarn.lock',       # Optional: makes tree noisy
]

OTHER_EXCLUSIONS = ['migrations', 'tests', 'test_utils', 'static', 'templates', 'public']

MODIFIED_EXLUSIONS = EXCLUSIONS + OTHER_EXCLUSIONS

# -------------------------------------------------------------------------
# FUNCTIONS
# -------------------------------------------------------------------------

def should_exclude(name):
    """
    Checks if a file or folder name matches any of the exclusion patterns.
    """
    for pattern in MODIFIED_EXLUSIONS:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def generate_tree(dir_path, prefix=""):
    """
    Recursively generates and prints the file tree structure.
    """
    path = Path(dir_path)
    
    # Get all items in directory, sorted alphabetically
    try:
        # We assume dir_path is a directory because of the check in main()
        # or previous recursion.
        items = sorted(list(path.iterdir()))
    except PermissionError:
        print(f"{prefix}└── [Permission Denied]")
        return

    # Filter out exclusions
    filtered_items = [item for item in items if not should_exclude(item.name)]
    
    # Iterate over items to print
    total_items = len(filtered_items)
    
    for index, item in enumerate(filtered_items):
        # Determine if this is the last item in the current branch
        is_last = (index == total_items - 1)
        
        connector = "└── " if is_last else "├── "
        
        print(f"{prefix}{connector}{item.name}")
        
        if item.is_dir():
            # Prepare the prefix for the next level
            # If this was the last item, the vertical bar is not needed for children
            extension = "    " if is_last else "│   "
            generate_tree(item, prefix + extension)

# -------------------------------------------------------------------------
# MAIN EXECUTION
# -------------------------------------------------------------------------

def main():
    print("--- File Tree Generator ---")
    user_input = input("Enter the project folder path (press Enter for current dir): ").strip()
    
    # Default to current directory if input is empty
    target_dir = user_input if user_input else "."
    
    path_obj = Path(target_dir)

    if not path_obj.exists():
        print(f"Error: The path '{target_dir}' does not exist.")
        return

    if not path_obj.is_dir():
        print(f"Error: The path '{target_dir}' is not a directory.")
        return

    print(f"\n{path_obj.resolve().name}/")
    generate_tree(path_obj)
    print("\n--- End of Tree ---")

if __name__ == "__main__":
    # Force the current working directory to be the folder where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
    input("Press Enter to exit...")
