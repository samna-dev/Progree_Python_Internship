# File Organizer & Cleanup Utility
# Sorts the files in data_folder into subfolders by extension
# Extracts emails and transaction IDs from log files using regex
# Saves the results to a master CSV file

import os
import shutil
import logging
import re
import csv

# ---- Settings ----
# Use a folder next to this script, so it works from any terminal location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
folder = os.path.join(BASE_DIR, "data_folder")
csv_path = os.path.join(BASE_DIR, "master_log.csv")

# Record every action in a log file with date and time
logging.basicConfig(
    filename=os.path.join(BASE_DIR, "organizer.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M",
)

# Extension to category folder
categories = {
    ".pdf": "Documents",
    ".txt": "Documents",
    ".docx": "Documents",
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".mp4": "Videos",
    ".mkv": "Videos",
    ".zip": "Archives",
    ".rar": "Archives",
    ".py": "Code",
    ".html": "Code",
    ".log": "Logs",
}

# Regex patterns for the text extraction
email_pattern = r"[\w.-]+@[\w-]+\.[\w.]+"
txn_pattern = r"TXN\d{6}"

# Stop early if the folder does not exist
if not os.path.isdir(folder):
    print("Folder not found. Create a folder named 'data_folder' next to organizer.py.")
    exit()

# Counters for the final summary
moved = 0
failed = 0

# Main loop
for name in os.listdir(folder):
    full_path = os.path.join(folder, name)

    # Skip folders, only move files
    if not os.path.isfile(full_path):
        continue

    # Find the category from the extension
    base, ext = os.path.splitext(name)
    category = categories.get(ext.lower(), "Others")

    # Create the category folder if it does not exist
    target = os.path.join(folder, category)
    os.makedirs(target, exist_ok=True)

    # Handle name collisions: photo.jpg -> photo_1.jpg
    destination = os.path.join(target, name)
    counter = 1
    while os.path.exists(destination):
        new_name = f"{base}_{counter}{ext}"
        destination = os.path.join(target, new_name)
        counter += 1

    # Move the file and record the result
    try:
        shutil.move(full_path, destination)
        print("Moved:", name, "->", category)
        logging.info(f"Moved {name} -> {category}")
        moved += 1
    except PermissionError:
        print("Permission denied:", name)
        logging.error(f"Permission denied: {name}")
        failed += 1
    except Exception as e:
        print("Error with", name, ":", e)
        logging.error(f"Error with {name}: {e}")
        failed += 1

# Summary
print("\n===== Summary ======")
print(f"files moved: {moved}")
print(f"files failed: {failed}")
logging.info(f"Summary: {moved} moved, {failed} failed")

# ----- Log parsing -----
logs_folder = os.path.join(folder, "Logs")
if not os.path.isdir(logs_folder):
    print("No Logs folder found, nothing to parse.")
    exit()

rows = []
for log_name in os.listdir(logs_folder):
    log_path = os.path.join(logs_folder, log_name)
    with open(log_path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            emails = re.findall(email_pattern, line)
            ids = re.findall(txn_pattern, line)

            # Keep the line only if it has an email or a transaction ID
            if emails or ids:
                rows.append([log_name, line_number, ";".join(emails), ";".join(ids)])

# Write the master CSV
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["File", "Line", "Email", "Transaction ID"])
    writer.writerows(rows)

print("===Parsing Summary===")
print(f"Rows saved to master_log.csv: {len(rows)}")
logging.info(f"Parsed logs: {len(rows)} rows saved to master_log.csv")