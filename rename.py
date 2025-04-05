import os
import zlib
import shutil
from helper import color_text

INPUT_DIR = "input"
OUTPUT_DIR = "output"

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum for the given file."""
    crc32 = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536):
            crc32 = zlib.crc32(chunk, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def rename_and_move(src_dir, dest_dir):
    files = [f for f in os.listdir(src_dir) if f != '.gitignore']
    if not files:
        print(color_text(f"The '{src_dir}' folder is empty.", 'red'))
        return

    import re
    for file in files:
        src = os.path.join(src_dir, file)
        name, ext = os.path.splitext(file)

        # Check if filename already has a CRC32 pattern at the end like "name [AB12CD34].ext"
        if re.search(r"\[[0-9A-F]{8}\]$", name, re.IGNORECASE):
            new_name = file  # Already has CRC32, no change
        else:
            crc = calculate_crc32(src).upper()
            base_name = name.replace('_output', '')
            new_name = f"{base_name} [{crc}]{ext}"

        dest = os.path.join(dest_dir, new_name)
        shutil.move(src, dest)
        print(color_text(f"Moved: {file} -> {new_name}", 'green'))

if __name__ == "__main__":
    input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_DIR)
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT_DIR)
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    rename_and_move(input_dir, output_dir)
