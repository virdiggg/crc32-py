import os
import zlib
import shutil
from helpers.str import StrHelper

str_helper = StrHelper()

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum for the given file."""
    buf_size = 65536  # Read in 64kb chunks
    crc32 = 0

    with open(file_path, 'rb') as f:
        while chunk := f.read(buf_size):
            crc32 = zlib.crc32(chunk, crc32)

    # Ensure crc32 is always positive
    return format(crc32 & 0xFFFFFFFF, '08x')

def rename_and_move_files(input_folder, output_folder):
    """Scan the input folder, calculate CRC32, rename the files, and move them to the output folder."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file == ".gitignore":
                continue

            original_file_path = os.path.join(root, file)
            file_name, file_ext = os.path.splitext(file)
            crc32_value = calculate_crc32(original_file_path).upper()
            new_file_name = f"{file_name} [{crc32_value}]{file_ext}"
            new_file_path = os.path.join(output_folder, new_file_name)

            # Move and rename the file
            shutil.move(original_file_path, new_file_path)
            str_helper.prGreen(f"Renamed and moved: {file} -> {new_file_name}")

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    input_folder = os.path.join(root, 'input')
    output_folder = os.path.join(root, 'output')

    rename_and_move_files(input_folder, output_folder)
