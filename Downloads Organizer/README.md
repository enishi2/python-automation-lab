# 📁 Downloads Organizer

Automatically organizes your **Downloads folder** by sorting files into categorized subfolders based on their extension — no more hunting for that PDF buried under 200 random files.

---

## Usage

**Organize your Downloads folder:**
```bash
python downloads_organizer.py
```

---

## Categories

| Folder | Extensions |
|--------|------------|
| Images | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` |
| Documents | `.pdf` `.docx` `.doc` `.txt` `.xlsx` `.csv` `.pptx` |
| Videos | `.mp4` `.mov` `.avi` `.mkv` `.wmv` |
| Audio | `.mp3` `.wav` `.flac` `.aac` `.ogg` |
| Compressed | `.zip` `.rar` `.7z` `.tar` `.gz` |
| Executables | `.exe` `.msi` `.dmg` `.pkg` |
| Code | `.py` `.js` `.html` `.css` `.json` `.xml` |
| Others | anything not listed above |

---

## Customization

To add or change categories, edit the `CATEGORIES` dictionary at the top of the script:

```python
CATEGORIES = {
    "MyFolder": [".xyz", ".abc"],
    # ...
}
```

---

## Requirements

- Python 3.10+
- No external packages needed
