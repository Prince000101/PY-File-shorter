import os
import shutil
import json
import logging
import tkinter as tk
from tkinter import filedialog

# Configure logging
logging.basicConfig(filename="file_sorting.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# File type categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".sh", ".bat"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".c", ".php"]
}

# File to store sorting history for undo
HISTORY_FILE = "sorting_history.json"

def log_move(file, category):
    """Logs moved files."""
    logging.info(f"Moved: {file} → {category}/")

def get_unique_filename(folder, filename):
    """Prevents overwriting by renaming duplicate files."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(folder, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1

    return new_filename

def save_sorting_history(original_path, new_path):
    """Saves original file locations to a history file for undo."""
    history = {}

    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history[original_path] = new_path

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

def organize_directory(directory):
    """Sorts files into categorized folders inside a 'Sorted' directory."""
    if not os.path.exists(directory):
        print("Directory does not exist.")
        return

    directory = os.path.abspath(directory)  # Get absolute path
    sorted_folder = os.path.join(directory, "Sorted")  # Main sorted folder

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        if os.path.isdir(file_path):  # Ignore directories
            continue

        file_extension = os.path.splitext(filename)[1].lower()
        category = "Others"  # Default category

        for cat, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                category = cat
                break

        # Create category folder inside "Sorted/"
        category_folder = os.path.join(sorted_folder, category)
        if not os.path.exists(category_folder):
            os.makedirs(category_folder)

        # Check if file is already sorted
        new_filename = get_unique_filename(category_folder, filename)
        new_file_path = os.path.join(category_folder, new_filename)

        if file_path == new_file_path:
            continue  # Skip if already sorted

        # Move file
        shutil.move(file_path, new_file_path)
        log_move(filename, category)
        save_sorting_history(file_path, new_file_path)
        print(f"Moved {filename} → {category}/")

    print("\nSorting completed!")

def undo_sorting():
    """Moves files back to their original locations."""
    if not os.path.exists(HISTORY_FILE):
        print("No sorting history found.")
        return

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    for new_path, original_path in history.items():
        if os.path.exists(new_path):
            shutil.move(new_path, original_path)
            print(f"Restored: {new_path} → {original_path}")
        else:
            print(f"File not found: {new_path}")

    # Clear history after undo
    os.remove(HISTORY_FILE)
    print("\nUndo completed!")

def browse_directory():
    """Opens a file dialog to select a directory."""
    folder_selected = filedialog.askdirectory()
    entry_var.set(folder_selected)

def start_sorting():
    """Starts sorting process from the GUI."""
    target_directory = entry_var.get().strip()
    if target_directory:
        organize_directory(target_directory)

def start_undo():
    """Starts undo process from the GUI."""
    undo_sorting()

# GUI Setup
root = tk.Tk()
root.title("File Organizer")

entry_var = tk.StringVar()

tk.Label(root, text="Select Directory:").pack()
tk.Entry(root, textvariable=entry_var, width=40).pack()
tk.Button(root, text="Browse", command=browse_directory).pack()
tk.Button(root, text="Sort Files", command=start_sorting).pack()
tk.Button(root, text="Undo Sorting", command=start_undo).pack()

root.mainloop()
