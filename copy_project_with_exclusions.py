#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def copy_project_with_exclusions(src_dir, dest_dir):
    # Common files and directories to exclude
    default_exclusions = {
        'node_modules', '.venv', '__pycache__', '.git', '.svn', '.hg',
        '.idea', '.vscode', 'build', 'dist', '*.pyc', '*.pyo', '*.pyd',
        '*.so', '*.dll', '*.exe', 'Thumbs.db', '.DS_Store', '*.egg-info',
        '.mypy_cache', '.pytest_cache', '.coverage', '*.log', 'npm-debug.log*',
        'yarn-debug.log*', 'yarn-error.log*', '*.app', '*.deb', '*.rpm',
        '*.msi', '*.dmg', '.next', '.husky', '.github',
    }
    
    other_exclusions = {'migrations', 'media', 'static', 'templates', 'public', '__mocks__', '__tests__', '__init__.py', 'cypress'}
    
    exclusions = default_exclusions | other_exclusions
    
    def should_ignore(path):
        # Convert to Path object for easier handling
        rel_path = Path(path).relative_to(src_dir) if path != src_dir else Path()
        
        # Check if any part of the path matches exclusions
        for part in rel_path.parts:
            if part in exclusions:
                return True
            # Check wildcard patterns
            if any(part.endswith(ext[1:]) for ext in exclusions if ext.startswith('*')):
                return True
        
        return False

    try:
        # Create destination directory
        os.makedirs(dest_dir, exist_ok=True)
        
        # Walk through source directory
        for root, dirs, files in os.walk(src_dir):
            # Skip ignored directories
            if should_ignore(root):
                continue

            # Create relative path for destination
            rel_path = os.path.relpath(root, src_dir)
            dest_path = os.path.join(dest_dir, rel_path)
            
            # Create directory in destination if it doesn't exist
            if rel_path != '.':
                os.makedirs(dest_path, exist_ok=True)

            # Copy files
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_path, file)
                
                if not should_ignore(src_file):
                    shutil.copy2(src_file, dest_file)
                    print(f"Copied: {src_file} -> {dest_file}")
        
        print(f"\nSuccessfully copied project from '{src_dir}' to '{dest_dir}'")
        print("Excluded common development files and directories")
        
    except Exception as e:
        print(f"Error during copy operation: {str(e)}")

def main():
    print("Project Folder Duplicator")
    print("=" * 50)
    
    # Get source directory
    while True:
        src_dir = input("\nEnter source directory path: ").strip()
        if os.path.isdir(src_dir):
            break
        print("Error: Source directory does not exist. Please try again.")
    
    # Get destination directory
    while True:
        dest_dir = input("Enter destination directory path: ").strip()
        if dest_dir:
            if os.path.exists(dest_dir):
                overwrite = input("Destination directory exists. Overwrite? (y/n): ").strip().lower()
                if overwrite != 'y':
                    continue
            break
        print("Error: Please enter a valid destination path.")
    
    # Confirm operation
    print(f"\nAbout to copy:")
    print(f"From: {src_dir}")
    print(f"To: {dest_dir}")
    print("\nThis will exclude common development files (node_modules, .venv, etc.)")
    
    confirm = input("\nProceed? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Perform the copy
    copy_project_with_exclusions(src_dir, dest_dir)

if __name__ == "__main__":
    # Force the current working directory to be the folder where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
    input("Press Enter to exit...")
