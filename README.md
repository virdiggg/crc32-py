# 🎞️ MKV Re-Merge & CRC32 Renamer

A simple tool to help you:
- 🧩 **Re-merge MKV files** using `mkvmerge` with selected audio, subtitle, and attachments
- 🏷️ **Rename files with their CRC32 hash** for easier verification and organization

---

## 📁 Folder Structure

```
ROOT/
├── input/         # Files to be renamed with CRC32
├── init/          # Files to be re-merged
├── output/        # Final output files after renaming
├── logs/          # Logs for mkvmerge commands
├── toolnix.py     # Re-merge and rename
├── rename.py      # Rename only
```

---

## 🚀 How to Use

### 1. 🔧 Rename File with CRC32
- Place your file(s) inside the `input/` folder.
- Run:
  ```sh
  python rename.py
  ```
- The script will:
  - Calculate the file's CRC32 checksum
  - Rename it to include the CRC (e.g., `video.mkv` → `video [1A2B3C4D].mkv`)
  - Move it to the `output/` folder

---

### 2. 🎬 Re-Merge File, Then Rename with CRC32
- Place your `.mkv` file inside the `init/` folder.
- Run:
  ```sh
  python toolnix.py
  ```

You will be prompted to:
1. **Select audio tracks** (enter numbers comma-separated, e.g., `2` or `1,3`)
2. **Select subtitle tracks** (same format)
3. **Enter the video title** (shown in MediaInfo or in your video player when you play the video)
4. **Enter the output filename** (press Enter to use the title)

The script will:
- Use `mkvmerge` to combine selected tracks
- Set the **first selected audio and subtitle as default**
- Save the output to `input/`
- Automatically rename it with CRC32 and move to `output/`

Logs for each `mkvmerge` run are saved in `logs/mkvmerge-YYYY-MM-DD.log`.

---

## 🧰 Requirements

- Python 3.7+

---

## 📝 License

MIT License – Use freely for personal or commercial projects.

---
