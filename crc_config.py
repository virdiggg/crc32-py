import os
from datetime import datetime

ROOT_DIR   = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR  = os.path.join(ROOT_DIR, "input")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")
LOG_DIR    = os.path.join(ROOT_DIR, "logs")

os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

MKVTOOLNIX = os.path.join(ROOT_DIR, "mkvtoolnix", "mkvmerge.exe")

VIDEO_EXTS = (".mkv", ".mp4", ".avi", ".mov", ".ts")
AUDIO_EXTS = (".flac", ".aac", ".mp3", ".ogg", ".m4a")
SUB_EXTS   = (".srt", ".ass", ".ssa")
FONT_EXTS  = (".ttf", ".otf")

CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")
LOG_FILE = os.path.join(LOG_DIR, f"log-{CURRENT_DATE}.log")
