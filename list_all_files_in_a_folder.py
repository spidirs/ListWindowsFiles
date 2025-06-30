import os
import sys
import tempfile
import subprocess

def generate_tree(root_dir, prefix=''):
    entries = sorted(os.listdir(root_dir))
    entries_count = len(entries)

    tree_lines = []
    for idx, entry in enumerate(entries):
        path = os.path.join(root_dir, entry)
        connector = '└── ' if idx == entries_count - 1 else '├── '

        tree_lines.append(f"{prefix}{connector}{entry}")

        if os.path.isdir(path):
            extension = '    ' if idx == entries_count - 1 else '│   '
            tree_lines.extend(generate_tree(path, prefix + extension))

    return tree_lines

def get_script_directory():
    if getattr(sys, 'frozen', False):
        # Running as PyInstaller EXE
        return os.path.dirname(sys.executable)
    else:
        # Running as normal .py script
        return os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    script_directory = get_script_directory()
    print(f"\nScanning directory tree from: '{script_directory}'...")

    tree_output = generate_tree(script_directory)

    # Create a temporary text file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
    temp_file_path = temp_file.name

    for line in tree_output:
        temp_file.write(line + "\n")

    temp_file.close()

    print(f"\nDirectory tree saved to temporary file:\n{temp_file_path}")

    # Open the output file in Notepad
    try:
        subprocess.Popen(['notepad.exe', temp_file_path])
    except Exception as e:
        print(f"Could not open Notepad automatically: {e}")
