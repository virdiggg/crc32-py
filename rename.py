import os, shutil, subprocess
from dotenv import load_dotenv
from helper import color_text, handle_exit
from crc_config import ROOT_DIR, INPUT_DIR, OUTPUT_DIR
from crc32 import calculate_crc32, extract_crc32_from_name

load_dotenv()

def rename_and_move(src_dir, dest_dir):
    files = [f for f in os.listdir(src_dir) if f != '.gitignore' and os.path.isfile(os.path.join(src_dir, f))]

    if not files:
        print(color_text(f"The '{src_dir}' folder is empty (or only contains subfolders).", 'red'))
        return

    for file in files:
        src = os.path.join(src_dir, file)
        name, ext = os.path.splitext(file)
        file_crc = extract_crc32_from_name(name)
        calc_crc = calculate_crc32(src).upper()

        # Check if filename already has a CRC32 pattern at the end like "name [AB12CD34].ext"
        if file_crc:
            new_name = file  # Already has CRC32, no change
        else:
            base_name = name.replace('_output', '')
            new_name = f"{base_name} [{calc_crc}]{ext}"

        dest = os.path.join(dest_dir, new_name)
        shutil.move(src, dest)
        print(color_text(f"Moved: {file} -> {new_name}", 'green'))

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, handle_exit)

    rename_and_move(INPUT_DIR, OUTPUT_DIR)

    API_KEY = os.getenv('PIXELDRAIN_API_KEY')
    WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

    if API_KEY and WEBHOOK_URL:
        subprocess.run(['python', os.path.join(ROOT_DIR, 'pixeldrain.py')])
