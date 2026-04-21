# SuperSearch

SuperSearch is a beginner-friendly Python script that searches for one or more words across multiple files in the same folder.

It supports both common text files and PDF files, shows where each match was found, counts occurrences per file, and can save the full report to a `.txt` file.

## Features

- Search for one or more words at the same time
- Case-insensitive search
- Safe literal search using escaped patterns
- Search in all valid files in the folder or only in selected files
- Show the file name for each result
- Show line numbers for text files
- Show page and line references for PDF files
- Count occurrences per file
- Show the overall total across all searched files
- Save results to a `.txt` report

## Supported File Types

Text-based files:

- `.txt`
- `.csv`
- `.log`
- `.md`
- `.py`
- `.json`
- `.xml`
- `.html`
- `.htm`
- `.yaml`
- `.yml`
- `.ini`
- `.cfg`
- `.bat`
- `.ps1`
- `.sql`

PDF files:

- `.pdf`

## Requirements

- Python 3.10 or newer recommended
- `PyPDF2` for PDF support

Install the PDF dependency with:

```bash
pip install PyPDF2
```

If `PyPDF2` is not installed, the script will still work for text files, but PDF search will be unavailable.

## How It Works

When you run the script, it asks you:

1. Whether you want to search all valid files in the current folder or only specific files
2. Which words you want to search for
3. Whether you want to save the results to a `.txt` file

The script searches using literal text matching, not advanced regular expressions. This makes it safer and easier for non-technical users.

## Usage

Place `SuperSearch.py` in the folder that contains the files you want to search.

Run the script:

```bash
python SuperSearch.py
```

Then follow the prompts in the terminal.

## Example Flow

```text
How would you like to search?
1. Search in all valid files in this folder
2. Search only in specific files
Choose 1 or 2: 2

Enter the file name or several file names separated by commas
Example: notes.txt, report.pdf, data.csv
Files: notes.txt, report.pdf

Enter one or more words separated by commas
Example: love, peace, hope
Words: automation, python, search
```

## Output Example

```text
SEARCH RESULTS
============================================================

File: notes.txt
------------------------------------------------------------
Line 12: This search tool was built with Python.
Found words: python (1), search (1)
Occurrences in this section: 2

Total occurrences in 'notes.txt': 2
```

## Notes and Limitations

- The script searches only in the same folder where `SuperSearch.py` is located
- It does not search subfolders
- Text files are read as UTF-8
- Some PDF files may not return text correctly if they are scanned images instead of selectable text
- For scanned PDFs, OCR would be needed for reliable search

## Who This Is For

This project is designed for:

- beginners learning Python automation
- users who want a simple search tool without complex commands
- quick keyword searches in mixed folders containing text files and PDFs

## Possible Future Improvements

- Search inside subfolders
- Export results to CSV
- Count totals for each searched word separately
- Highlight found words in the output
- Add support for scanned PDF OCR
