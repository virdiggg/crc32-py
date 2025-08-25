import os
from helper import handle_exit, color_text
from crc_config import SCAN_DIR
from crc32 import calculate_crc32, extract_crc32_from_name

def scan_folder(folder_path):
    for root, _, files in os.walk(folder_path):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                calc_crc = calculate_crc32(file_path)
                file_crc = extract_crc32_from_name(name)

                if file_crc:
                    if calc_crc == file_crc:
                        status = color_text("match", "green")
                    else:
                        status = color_text("not match", "red")
                    print(f"{file_path} -> calc CRC: {calc_crc} => {status}")
                else:
                    print(f"{file_path} -> no CRC32 found in name, calc CRC: {color_text(calc_crc, "yellow")}")

            except Exception as e:
                print(color_text(f"Error reading {file_path}: {e}", "red"))

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, handle_exit)

    scan_folder(SCAN_DIR)
