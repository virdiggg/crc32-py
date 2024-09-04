import os
import json
import subprocess
from helpers.str import StrHelper

str_helper = StrHelper()

def load_track_info(video_file):
    # Load the track information using mkvmerge -J (JSON output)
    command = [r"C:\Program Files\MKVToolNix\mkvmerge.exe", "-J", video_file]
    result = subprocess.run(command, capture_output=True, text=True)
    return json.loads(result.stdout)

def select_tracks(tracks, track_type):
    print(f"\nAvailable {track_type} tracks:")
    for i, track in enumerate(tracks):
        print(f"{i + 1}: {track['properties']['language']} ({track.get('properties').get('track_name', 'No Name')})")

    choices = input(f"Enter the numbers of the {track_type} tracks to include (comma-separated): ")
    selected_tracks = [tracks[int(i) - 1]["id"] for i in choices.split(",")]

    return selected_tracks

def construct_mkvmerge_command(video_file, audio_tracks, subtitle_tracks, attachments_tracks, title, output_name):
    output_path = os.path.join("input", f"{str_helper.clean_utf8(output_name)}.mkv")
    command = [
        r"C:\Program Files\MKVToolNix\mkvmerge.exe", "-o", output_path,
        "--title", title,
        "--video-tracks", "0",  # Assuming the video track is ID 0
    ]

    if audio_tracks:
        command += ["--audio-tracks", ",".join(map(str, audio_tracks))]

    if subtitle_tracks:
        command += ["--subtitle-tracks", ",".join(map(str, subtitle_tracks))]

    if attachments_tracks:
        command += ["--attach-file"] + attachments_tracks

    command.append(video_file)

    return command

def main():
    input_directory = "init"

    for root, _, files in os.walk(input_directory):
        for file in files:
            if file == ".gitignore":
                continue

            str_helper.prGreen(f"Input file: {file}")
            video_file = os.path.join(os.path.dirname(__file__), input_directory, file)

            # Load track information
            track_info = load_track_info(video_file)
            audio_tracks = [track for track in track_info["tracks"] if track["type"] == "audio"]
            subtitle_tracks = [track for track in track_info["tracks"] if track["type"] == "subtitles"]
            attachments_tracks = [track for track in track_info["tracks"] if track["type"] == "attachments"]

            # Select audio and subtitle tracks
            selected_audio_tracks = select_tracks(audio_tracks, "audio")
            selected_subtitle_tracks = select_tracks(subtitle_tracks, "subtitle")
            selected_attachments_tracks = [track["file"] for track in attachments_tracks]  # Use the file path for attachments

            title = input("Enter the title for the video: ")
            output_name = input("Enter the output file name: ")

            # Construct the mkvmerge command
            command = construct_mkvmerge_command(video_file, selected_audio_tracks, selected_subtitle_tracks, selected_attachments_tracks, title, output_name)

            # Execute the mkvmerge command
            subprocess.run(command)

if __name__ == "__main__":
    main()

    rename = os.path.join(os.path.dirname(__file__), 'run.py')
    subprocess.run(['python', rename])