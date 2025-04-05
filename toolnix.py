# toolnix.py
import os
import json
import subprocess
from helper import clean_utf8, color_text, handle_exit

MKVTOOLNIX = os.path.join('mkvtoolnix', 'mkvmerge.exe')
INPUT_DIR = "input"

os.makedirs(INPUT_DIR, exist_ok=True)

def load_track_info(file):
    result = subprocess.run([MKVTOOLNIX, "-J", file], capture_output=True, text=True)
    return json.loads(result.stdout)

def select_tracks(tracks, ttype):
    print(color_text(f"\nAvailable {ttype} tracks:", 'green'))
    for i, track in enumerate(tracks):
        lang = track['properties'].get('language', 'und')
        name = track['properties'].get('track_name', 'No Name')
        print(color_text(f"{i + 1}: {lang} ({name})", 'yellow'))
    ids = input(color_text(f"Enter the numbers of {ttype} tracks to include (comma-separated): "), 'green')
    return [tracks[int(i)-1]['id'] for i in ids.split(',') if i.strip().isdigit()]

def build_mkvmerge_cmd(file, aud, sub, att, title, out_name):
    out_path = os.path.join(INPUT_DIR, f"{clean_utf8(out_name)}_output.mkv")
    cmd = [MKVTOOLNIX, "-o", out_path, "--title", title, "--video-tracks", "0"]

    if aud: cmd += ["--audio-tracks", ",".join(map(str, aud))]
    if sub: cmd += ["--subtitle-tracks", ",".join(map(str, sub))]
    if att: cmd += ["--attach-file"] + att
    cmd.append(file)
    return cmd

def main():
    for file in os.listdir(INPUT_DIR):
        if file == '.gitignore': continue
        if '_output' in file: continue

        path = os.path.join(INPUT_DIR, file)
        print(color_text(f"Input file: {file}", 'green'))

        info = load_track_info(path)
        aud = select_tracks([t for t in info['tracks'] if t['type'] == 'audio'], "audio")
        sub = select_tracks([t for t in info['tracks'] if t['type'] == 'subtitles'], "subtitle")
        att = [t['file'] for t in info['tracks'] if t['type'] == 'attachments']

        title = input(color_text("Enter video title: ", 'green'))
        out_name = input(color_text("Enter output filename (without extension): ", 'green'))

        subprocess.run(build_mkvmerge_cmd(path, aud, sub, att, title, out_name))

        os.remove(path)

    subprocess.run(['python', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rename.py')])

if __name__ == "__main__":
    import signal
    signal.signal(signal.SIGINT, handle_exit)

    main()
