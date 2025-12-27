import re
import os
import csv

def detect_numbers_in_folder(folder_path, output_file):
    # pattern to match Arabic or Nepali digits
    number_pattern = r"[0-9०-९]+"
    # pattern to detect timestamp lines (SRT/VTT format)
    timestamp_pattern = r"^\d{2}:\d{2}:\d{2}[.,]\d{3} --> \d{2}:\d{2}:\d{2}[.,]\d{3}"
    # pattern to detect index lines (lines containing only digits)
    index_pattern = r"^\d+$"

    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["File Name", "Line Number", "Detected Numbers"])

        for root, dirs, files in os.walk(folder_path):
            for filename in files:
                if filename.endswith((".srt", ".vtt")):
                    file_path = os.path.join(root, filename)
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        for line_num, line in enumerate(f, start=1):
                            line = line.strip()
                            # skip timestamp lines and index lines
                            if re.match(timestamp_pattern, line) or re.match(index_pattern, line):
                                continue
                            numbers = re.findall(number_pattern, line)
                            if numbers:
                                writer.writerow([filename, line_num, ", ".join(numbers)])

if __name__ == "__main__":
    folder = input("Enter folder path containing subtitle files: ")
    output_file = input("Enter output CSV file name (e.g., detected_numbers.csv): ")
    detect_numbers_in_folder(folder, output_file)
    print(f"Done! Numbers saved to {output_file}")
