#!/usr/bin/env python3
"""
Script to prompt for a directory and output all absolute file paths within it.
"""

import os
import sys
from pathlib import Path

def get_all_file_paths(directory_path):
    """
    Recursively get all file paths in a directory and its subdirectories.
    
    Args:
        directory_path: Path object of the directory to search
        
    Returns:
        List of absolute paths to all files
    """
    file_paths = []
    
    try:
        # Walk through directory recursively
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                # Create absolute path and add to list
                file_path = os.path.join(root, file)
                file_paths.append(os.path.abspath(file_path))
    except Exception as e:
        print(f"Error walking directory: {e}", file=sys.stderr)
        return []
    
    return file_paths

def main():
    # Prompt user for directory path
    user_input = input("Enter directory path: ").strip()
    
    # Handle empty input
    if not user_input:
        print("No directory provided. Exiting.", file=sys.stderr)
        sys.exit(1)
    
    # Convert to Path object
    directory_path = Path(user_input)
    
    # Check if directory exists
    if not directory_path.exists():
        print(f"Error: Directory '{user_input}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Check if it's actually a directory
    if not directory_path.is_dir():
        print(f"Error: '{user_input}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    # Get all file paths
    print("\nFetching file paths...\n")
    file_paths = get_all_file_paths(directory_path)
    
    # Check if any files were found
    if not file_paths:
        print("No files found in the specified directory.", file=sys.stderr)
        sys.exit(0)
    
    # Output all file paths
    print(f"Found {len(file_paths)} files:\n")
    for i, file_path in enumerate(file_paths, 1):
        print(file_path)

if __name__ == "__main__":
    # Force the current working directory to be the folder where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
    input("Press Enter to exit...")