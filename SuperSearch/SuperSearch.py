import re
from pathlib import Path

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

VALID_TEXT_EXTENSIONS = {
    ".txt", ".csv", ".log", ".md", ".py", ".json", ".xml", ".html",
    ".htm", ".yaml", ".yml", ".ini", ".cfg", ".bat", ".ps1", ".sql"
}
VALID_EXTENSIONS = VALID_TEXT_EXTENSIONS | {".pdf"}


def build_patterns(words):
    patterns = []
    for word in words:
        clean_word = word.strip()
        if clean_word:
            patterns.append((clean_word, re.compile(re.escape(clean_word), re.IGNORECASE)))
    return patterns



def search_in_line(line, patterns):
    found_words = []
    total_in_line = 0

    for original_word, pattern in patterns:
        matches = list(pattern.finditer(line))
        if matches:
            count = len(matches)
            total_in_line += count
            found_words.append((original_word, count))

    return found_words, total_in_line



def search_in_text_file(file_path, patterns):
    results = []
    total_occurrences = 0

    with open(file_path, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            found_words, line_total = search_in_line(line, patterns)
            if found_words:
                total_occurrences += line_total
                results.append({
                    "source": f"Line {line_number}",
                    "content": line.strip(),
                    "count": line_total,
                    "words": found_words,
                })

    return results, total_occurrences



def search_in_pdf(file_path, patterns):
    results = []
    total_occurrences = 0

    reader = PdfReader(str(file_path))

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        if not text:
            continue

        for line_number, line in enumerate(text.splitlines(), start=1):
            found_words, line_total = search_in_line(line, patterns)
            if found_words:
                total_occurrences += line_total
                results.append({
                    "source": f"Page {page_number}, line {line_number}",
                    "content": line.strip(),
                    "count": line_total,
                    "words": found_words,
                })

    return results, total_occurrences



def get_valid_files_in_folder(base_path):
    return sorted(
        [file for file in base_path.iterdir() if file.is_file() and file.suffix.lower() in VALID_EXTENSIONS],
        key=lambda item: item.name.lower(),
    )



def ask_file_mode():
    print("\nHow would you like to search?")
    print("1. Search in all valid files in this folder")
    print("2. Search only in specific files")

    while True:
        choice = input("Choose 1 or 2: ").strip()
        if choice in {"1", "2"}:
            return choice
        print("Invalid option. Please type 1 or 2.")



def choose_files(base_path):
    mode = ask_file_mode()

    if mode == "1":
        files = get_valid_files_in_folder(base_path)
        if not files:
            print("No valid text or PDF files were found in this folder.")
            return []

        print("\nValid files found in this folder:")
        for file in files:
            print(f"- {file.name}")
        return files

    file_input = input(
        "\nEnter the file name or several file names separated by commas\n"
        "Example: notes.txt, report.pdf, data.csv\n"
        "Files: "
    ).strip()

    if not file_input:
        return []

    return [base_path / name.strip() for name in file_input.split(",") if name.strip()]



def format_found_words(found_words):
    return ", ".join(f"{word} ({count})" for word, count in found_words)



def main():
    base_path = Path(__file__).parent

    selected_files = choose_files(base_path)
    if not selected_files:
        print("No files were selected.")
        return

    words_input = input(
        "\nEnter one or more words separated by commas\n"
        "Example: love, peace, hope\n"
        "Words: "
    ).strip()

    if not words_input:
        print("No words were entered.")
        return

    words = [word.strip() for word in words_input.split(",") if word.strip()]
    patterns = build_patterns(words)

    if not patterns:
        print("No valid words were entered.")
        return

    results_to_save = []
    total_overall = 0

    print("\n" + "=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)

    for file_path in selected_files:
        if not file_path.exists():
            message = f"File not found: {file_path.name}"
            print(message)
            results_to_save.append(message)
            results_to_save.append("")
            continue

        if not file_path.is_file():
            message = f"This is not a valid file: {file_path.name}"
            print(message)
            results_to_save.append(message)
            results_to_save.append("")
            continue

        extension = file_path.suffix.lower()
        if extension not in VALID_EXTENSIONS:
            message = f"Unsupported file type: {file_path.name}"
            print(message)
            results_to_save.append(message)
            results_to_save.append("")
            continue

        try:
            if extension == ".pdf":
                if PdfReader is None:
                    message = (
                        f"Could not read '{file_path.name}' because PyPDF2 is not installed. "
                        f"Install it with: pip install PyPDF2"
                    )
                    print(message)
                    results_to_save.append(message)
                    results_to_save.append("")
                    continue

                results, file_total = search_in_pdf(file_path, patterns)
            else:
                results, file_total = search_in_text_file(file_path, patterns)

            if results:
                total_overall += file_total
                header = f"File: {file_path.name}"
                summary = f"Total occurrences in '{file_path.name}': {file_total}"

                print(f"\n{header}")
                print("-" * 60)
                results_to_save.append(header)
                results_to_save.append("-" * 60)

                for item in results:
                    found_words_text = format_found_words(item["words"])
                    print(f"{item['source']}: {item['content']}")
                    print(f"Found words: {found_words_text}")
                    print(f"Occurrences in this section: {item['count']}\n")

                    results_to_save.append(f"{item['source']}: {item['content']}")
                    results_to_save.append(f"Found words: {found_words_text}")
                    results_to_save.append(f"Occurrences in this section: {item['count']}")
                    results_to_save.append("")

                print(summary)
                print("-" * 60)
                results_to_save.append(summary)
                results_to_save.append("-" * 60)
                results_to_save.append("")
            else:
                message = f"No occurrences found in '{file_path.name}'."
                print(f"\n{message}")
                print("-" * 60)
                results_to_save.append(message)
                results_to_save.append("-" * 60)
                results_to_save.append("")

        except UnicodeDecodeError:
            message = f"The file '{file_path.name}' does not appear to be a readable UTF-8 text file."
            print(message)
            results_to_save.append(message)
            results_to_save.append("")
        except Exception as error:
            message = f"Error while reading '{file_path.name}': {error}"
            print(message)
            results_to_save.append(message)
            results_to_save.append("")

    print(f"\nOverall total occurrences across all files: {total_overall}")

    save_choice = input("\nDo you want to save the results to a .txt file? (y/n): ").strip().lower()

    if save_choice == "y":
        output_name = input("Enter the output file name (example: results.txt): ").strip()

        if not output_name:
            output_name = "results.txt"

        if not output_name.lower().endswith(".txt"):
            output_name += ".txt"

        output_path = base_path / output_name

        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write("SEARCH RESULTS\n")
            output_file.write("=" * 60 + "\n\n")
            output_file.write(f"Searched words: {', '.join(words)}\n\n")

            for item in results_to_save:
                output_file.write(item + "\n")

            output_file.write(f"Overall total occurrences: {total_overall}\n")

        print(f"Results saved successfully to: {output_path.name}")
    else:
        print("Results were not saved.")


if __name__ == "__main__":
    main()
