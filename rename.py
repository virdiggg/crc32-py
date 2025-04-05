import os
import zlib
import shutil
from str import color_text

INPUT_DIR = "input"
OUTPUT_DIR = "output"

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum for the given file."""
    crc32 = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536):
            crc32 = zlib.crc32(chunk, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def rename_and_move(src_dir, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)

    files = [f for f in os.listdir(src_dir) if f != '.gitignore']
    if not files:
        print(color_text(f"The '{src_dir}' folder is empty.", 'red'))
        return

    for file in files:
        src = os.path.join(src_dir, file)
        name, ext = os.path.splitext(file)
        crc = calculate_crc32(src).upper()
        new_name = f"{name} [{crc}]{ext}"
        dest = os.path.join(dest_dir, new_name)
        shutil.move(src, dest)
        print(color_text(f"Renamed and moved: {file} -> {new_name}", 'green'))

if __name__ == "__main__":
    rename_and_move(INPUT_DIR, OUTPUT_DIR)
