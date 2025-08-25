# 🎞️ MKV Re-Merge & CRC32 Renamer

A simple tool to help you:

- 🧩 **Re-merge video files** (pick audio/subtitle tracks, keep attachments)
- 📂 **Merge full folders** (video + subtitles + audios + fonts + chapters into one MKV)
- 🏷️ **Rename files with their CRC32 hash** for easier verification and organization

---

## 📁 Folder Structure

```
ROOT/
├── input/         # Place files/folders here
│   ├── movie.mkv              # Single-file re-merge
│   └── MyMovie/               # Folder merge
│       ├── video.mp4
│       ├── subtitle.ass
│       ├── soundtrack.flac
│       ├── font1.ttf
│       └── chapters.xml
├── output/        # Final output files after renaming
├── scan/          # Place files here to calculate or compare their CRC32
├── logs/          # Logs for mkvmerge commands
├── toolnix.py     # Main script (merge + rename)
├── rename.py      # Rename only
```

---

## 🚀 How to Use

### 1. 🔧 Rename File(s) with CRC32
- Place your file(s) inside the `input/` folder.
- Run:
  ```sh
  python rename.py
  ```
- The script will:
  - Calculate the CRC32 checksum
  - Rename the file to include the CRC (e.g., `video.mkv` → `video [1A2B3C4D].mkv`)
  - Move it to the `output/` folder

---

### 2. 🎬 Re-Merge a Single File
- Place a `.mkv` (or other video file) inside the `input/` folder.
- Run:
  ```sh
  python toolnix.py
  ```
- You will be prompted to:
  1. **Select audio tracks** (comma-separated numbers, e.g. `1,3`)
  2. **Select subtitle tracks** (comma-separated numbers, e.g. `1,3`)
  3. **Enter video title** (shown in MediaInfo / players)
  4. **Enter output filename** (default = title, or auto-picked if `<video>.txt` exists)

The script will:
- Re-mux with `mkvmerge`
- Keep selected tracks (first audio/subtitle set as default)
- Save merged file back to `input/`
- Automatically rename with CRC32 and move to `output/`

---

### 3. 📂 Merge a Folder of Sources
- Create a subfolder under `input/` (e.g. `input/MyMovie/`).
- Put inside:
  - **Video** (`.mkv`, `.mp4`, `.avi`, `.mov`, `.ts`)
  - **Subtitles** (`.srt`, `.ass`, `.ssa`)
  - **Extra audio** (`.flac`, `.aac`, `.mp3`, `.m4a`, `.ogg`)
  - **Fonts** (`.ttf`, `.otf`)
  - **Chapters** (`.xml`)
  - *(Optional)* A `.txt` file → if present, its filename (without extension) will be used as the **output name**, skipping the prompt
- Run:
  ```sh
  python toolnix.py
  ```
- You will be prompted for:
  - **Video title** (default = same as folder name)
  - **Output filename** (default = title, or auto-picked from `.txt` file)

The script will:
- Multiplex all contents into one `.mkv`
- Place the merged file in `input/`
- Rename with CRC32 and move to `output/`
- Delete the original folder after merging

---

### 4. 🎬 Comparing or calculate CRC32 of files
- Place a file (anything) inside the `scan/` folder.
- Run:
  ```sh
  python calculate.py
  ```

The script will:
- Calculate CRC32 has of any file inside `scan/`
- Check if the filename already contains a CRC32 hash:
  - If the CRC32 in the filename matches the calculated value → prints `match` (green)
  - If it doesn't match → prints `not match` (red) and shows the correct hash
  - If no CRC32 is found in the filename → prints the calculated CRC with the correct hash

---

Logs for each `mkvmerge` run are saved in `logs/log-YYYY-MM-DD.log`.

---

## 🧰 Requirements

- Python 3.7+

---

## 📝 License

MIT License – Use freely for personal or commercial projects.

---
