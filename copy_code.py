#!/usr/bin/env python3

import os
import sys

def get_output_filename():
    """
    Prompts user for output filename with a default.
    Returns a valid filename.
    """
    default_name = "copy_code_output.md"
    
    print(f"Enter output filename (default: '{default_name}'):")
    filename = input("> ").strip()
    
    if not filename:
        filename = default_name
        print(f"Using default filename: '{filename}'")
    
    # Ensure it has .md extension
    if not filename.lower().endswith('.md'):
        filename += '.md'
    
    return filename

def check_file_permissions(filename):
    """
    Checks if we have write permissions for the file.
    Returns True if writable, False otherwise.
    """
    if os.path.exists(filename):
        # Check if file is writable
        if not os.access(filename, os.W_OK):
            print(f"✗ Warning: File '{filename}' exists and is not writable.")
            print("  It might be open in another program or you don't have write permissions.")
            return False
    else:
        # Check if directory is writable
        dir_path = os.path.dirname(filename) or '.'
        if not os.access(dir_path, os.W_OK):
            print(f"✗ Error: Cannot write to directory '{dir_path}'")
            return False
    
    return True

def get_alternative_filename(original_name):
    """
    Suggests an alternative filename if the original is not writable.
    """
    base, ext = os.path.splitext(original_name)
    counter = 1
    
    while True:
        new_name = f"{base}_{counter}{ext}"
        if not os.path.exists(new_name) or os.access(new_name, os.W_OK):
            return new_name
        counter += 1
        if counter > 100:  # Safety limit
            return None

def combine_files_from_input(output_md_file):
    """
    Prompts user for file paths (paste all at once), reads their content,
    and writes them into output_md_file formatted as Markdown.
    """
    
    print(f"\nAttempting to write output to: {output_md_file}")
    
    # Check permissions before starting
    if not check_file_permissions(output_md_file):
        if os.path.exists(output_md_file):
            # File exists but not writable
            alternative = get_alternative_filename(output_md_file)
            if alternative:
                print(f"  Suggestion: Use '{alternative}' instead")
            else:
                print("  Could not find a writable alternative filename.")
            return None  # Signal fatal error
        else:
            # Directory not writable
            print(f"  Cannot create file in this directory.")
            return None  # Signal fatal error
    
    print("Paste all file paths (one per line, separated by newlines).")
    print("Press Enter, then Ctrl+D (Linux/Mac) or Ctrl+Z then Enter (Windows) when done.")
    print("-" * 30)
    
    # Collect all file paths at once using readlines
    print("Paste your file paths below:")
    try:
        # Read all lines from stdin at once
        lines = []
        while True:
            try:
                line = input()
                lines.append(line)
            except EOFError:
                break
    except KeyboardInterrupt:
        print("\n\nInput cancelled by user.")
        return False  # User cancelled, not a fatal error
    
    # Process all pasted lines
    file_paths = []
    for line in lines:
        line = line.strip()
        if line:  # Only add non-empty lines
            # Also split by common separators just in case
            for separator in ['\n', '\r', '\t', ';', '|']:
                if separator in line:
                    split_files = [f.strip() for f in line.split(separator) if f.strip()]
                    file_paths.extend(split_files)
                    break
            else:
                file_paths.append(line)
    
    if len(file_paths) == 0:
        print("No files entered.")
        return False  # No files, not a fatal error
    
    print(f"\nFound {len(file_paths)} file(s) to process:")
    for i, fp in enumerate(file_paths[:10], 1):  # Show first 10 files
        print(f"  {i:3}. {fp}")
    if len(file_paths) > 10:
        print(f"  ... and {len(file_paths) - 10} more")
    print("-" * 30)

    try:
        # Open the output file in write mode ('w')
        # Use utf-8 encoding to handle special characters correctly
        with open(output_md_file, 'w', encoding='utf-8') as out_f:
            
            success_count = 0
            error_count = 0
            
            for file_path in file_paths:
                # Check if the target file actually exists
                if os.path.isfile(file_path):
                    try:
                        # Read the content of the target file
                        with open(file_path, 'r', encoding='utf-8') as code_f:
                            content = code_f.read()

                        # Determine file extension for syntax highlighting (optional but nice)
                        # e.g., 'script.py' -> 'py'
                        _, ext = os.path.splitext(file_path)
                        language = ext.lstrip('.') if ext else ''

                        # Write the Header
                        out_f.write(f"## {file_path}\n\n")

                        # Write the Code Block
                        out_f.write(f"```{language}\n")
                        out_f.write(content)
                        
                        # Ensure there is a newline before closing the block
                        if content and not content.endswith('\n'):
                            out_f.write('\n')
                        
                        out_f.write("```\n\n")
                        
                        print(f"✓ {file_path}")
                        success_count += 1

                    except PermissionError:
                        print(f"✗ Permission denied: '{file_path}'")
                        out_f.write(f"## {file_path}\n\n> **Permission denied**\n\n")
                        error_count += 1
                    except Exception as e:
                        # Handle other errors
                        print(f"✗ Error reading '{file_path}': {e}")
                        out_f.write(f"## {file_path}\n\n> **Error reading file:** {e}\n\n")
                        error_count += 1
                else:
                    # Handle missing files
                    print(f"✗ File not found: '{file_path}'")
                    out_f.write(f"## {file_path}\n\n> **File not found**\n\n")
                    error_count += 1

        print("-" * 30)
        if success_count == 0 and error_count > 0:
            print(f"❌ Failed to process any files. {error_count} errors.")
            return False
        elif error_count > 0:
            print(f"⚠️  Processed {success_count} files with {error_count} errors.")
            return False
        else:
            print(f"✅ Successfully processed {success_count} files.")
            return True
        
    except PermissionError:
        print(f"\n❌ Fatal Error: Permission denied when writing to '{output_md_file}'")
        print("The file might be open in another program (like Word, browser, or another editor).")
        print("Please close the file in other programs and try again.")
        return None  # Signal fatal error
    except Exception as e:
        print(f"\n❌ Fatal Error writing to '{output_md_file}': {e}")
        return None  # Signal fatal error

if __name__ == "__main__":
    # Force the current working directory to be the folder where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    try:
        # Get output filename from user
        output_file = get_output_filename()
        
        # Try to process files
        result = combine_files_from_input(output_file)
        
        # Interpret the result
        if result is None:
            # Fatal error - couldn't even start writing
            print(f"\n❌ Cannot write to '{output_file}'. No output created.")
            print("Possible solutions:")
            print("  1. Close the file if it's open in another program")
            print("  2. Choose a different filename")
            print("  3. Run from a different directory")
        elif result is False:
            # Partial failure or user cancelled
            print(f"\n⚠️  Output saved to '{output_file}' with some issues.")
        elif result is True:
            # Complete success
            print(f"\n✅ Output successfully saved to: {output_file}")
        
        # Always keep the window open
        input("\nPress Enter to exit...")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user.")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Traceback:", file=sys.stderr)
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")
        sys.exit(1)
