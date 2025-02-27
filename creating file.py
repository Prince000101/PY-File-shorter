import os

# Define file categories and their extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Music": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".sh", ".bat"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".c", ".php"]
}

def create_test_files(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)  # Create directory if it doesn't exist

    for category, extensions in FILE_CATEGORIES.items():
        for i, ext in enumerate(extensions, 1):
            file_name = f"test_file_{category.lower()}_{i}{ext}"
            file_path = os.path.join(directory, file_name)

            # Create an empty file
            with open(file_path, "w") as f:
                f.write(f"Test file for {category} ({ext})")  # Sample content

            print(f"Created: {file_path}")

    print("\nTest files have been created successfully!")

# Get user input
if __name__ == "__main__":
    target_directory = input("Enter the directory where you want to create test files: ").strip()
    create_test_files(target_directory)

