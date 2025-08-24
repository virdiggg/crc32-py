import os, zlib, shutil, re
from helper import color_text, handle_exit
from crc_config import INPUT_DIR, OUTPUT_DIR

def calculate_crc32(file_path):
    """Calculate the CRC32 checksum for the given file."""
    crc32 = 0
    with open(file_path, 'rb') as f:
        while chunk := f.read(65536):
            crc32 = zlib.crc32(chunk, crc32)
    return format(crc32 & 0xFFFFFFFF, '08x')

def rename_and_move(src_dir, dest_dir):
    files = [f for f in os.listdir(src_dir) if f != '.gitignore' and os.path.isfile(os.path.join(src_dir, f))]

    if not files:
        print(color_text(f"The '{src_dir}' folder is empty (or only contains subfolders).", 'red'))
        return

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
    import signal
    signal.signal(signal.SIGINT, handle_exit)

    rename_and_move(INPUT_DIR, OUTPUT_DIR)
