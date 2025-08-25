import re, zlib, gc

def calculate_crc32(file_path, chunk_size=65536):
    """Calculate the CRC32 checksum for the given file."""
    crc = 0
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            crc = zlib.crc32(chunk, crc)
    del chunk
    gc.collect()
    return format(crc & 0xFFFFFFFF, "08X")

def extract_crc32_from_name(filename):
    """Try to extract an 8-char hex CRC32 from the filename."""
    match = re.search(r'([0-9A-Fa-f]{8})', filename)
    return match.group(1).upper() if match else None