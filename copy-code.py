import os

def combine_files(input_list_file, output_md_file):
    """
    Reads a list of file paths from input_list_file, reads their content,
    and writes them into output_md_file formatted as Markdown.
    """
    
    # Check if the list file exists before proceeding
    if not os.path.exists(input_list_file):
        print(f"Error: The input list file '{input_list_file}' was not found.")
        return

    print(f"Reading paths from: {input_list_file}")
    print(f"Writing output to:  {output_md_file}\n" + "-"*30)

    # Open the output file in write mode ('w')
    # Use utf-8 encoding to handle special characters correctly
    with open(output_md_file, 'w', encoding='utf-8') as out_f:
        
        # Open the input list file
        with open(input_list_file, 'r', encoding='utf-8') as in_f:
            lines = in_f.readlines()

        for line in lines:
            # Clean up the path (remove whitespace/newlines)
            file_path = line.strip()

            # Skip empty lines
            if not file_path:
                continue

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
                    
                    print(f"Success: Added '{file_path}'")

                except Exception as e:
                    # Handle permission errors or encoding errors
                    print(f"Error: Could not read '{file_path}'. Reason: {e}")
                    out_f.write(f"## {file_path}\n\n> **Error reading file:** {e}\n\n")
            else:
                # Handle missing files
                print(f"Skipping: '{file_path}' (File not found)")
                out_f.write(f"## {file_path}\n\n> **File not found**\n\n")

    print("-" * 30)
    print("Job complete.")

if __name__ == "__main__":
    # Configuration
    LIST_FILE = 'files_to_read.txt'
    OUTPUT_FILE = 'combined_code.md'
    
    combine_files(LIST_FILE, OUTPUT_FILE)
