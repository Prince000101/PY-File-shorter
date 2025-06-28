import os
import shutil
import json
import logging
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QLabel, QLineEdit, QPushButton, QFileDialog,
                             QMessageBox, QCheckBox, QGroupBox, QHBoxLayout,
                             QProgressBar, QStyle)
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor

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
HISTORY_FILE = os.path.join(os.path.expanduser("~"), "file_organizer_history.json")


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DraggableLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                path = url.toLocalFile()
                if os.path.isdir(path):
                    self.setText(path)
                else:
                    self.setText(os.path.dirname(path))


class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Organizer")
        self.setGeometry(100, 100, 600, 300)

        # Set window icon
        icon_path = resource_path("icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        else:
            self.setWindowIcon(self.style().standardIcon(QStyle.SP_DirIcon))

        self.set_dark_theme()
        self.initUI()

    def set_dark_theme(self):
        """Sets a dark grey/black theme for the application."""
        palette = QPalette()

        # Dark background
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)

        # Widget colors
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)

        # Button colors
        palette.setColor(QPalette.Button, QColor(80, 80, 80))
        palette.setColor(QPalette.ButtonText, Qt.white)

        # Highlight colors
        palette.setColor(QPalette.Highlight, QColor(100, 100, 100))
        palette.setColor(QPalette.HighlightedText, Qt.white)

        # Disabled colors
        palette.setColor(QPalette.Disabled, QPalette.Text, Qt.darkGray)
        palette.setColor(QPalette.Disabled, QPalette.ButtonText, Qt.darkGray)

        QApplication.setPalette(palette)

        # Set style sheet for additional styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #353535;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                color: #ccc;
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QPushButton {
                background-color: #505050;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 8px;
                min-width: 80px;
                color: white;
            }
            QPushButton:hover {
                background-color: #606060;
                border: 1px solid #666;
            }
            QPushButton:pressed {
                background-color: #404040;
            }
            QLineEdit {
                background-color: #353535;
                border: 1px solid #555;
                border-radius: 3px;
                padding: 5px;
                color: white;
                selection-background-color: #505050;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 3px;
                text-align: center;
                background-color: #353535;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #505050;
                width: 10px;
            }
            QCheckBox {
                color: white;
            }
            QLabel {
                color: white;
            }
            QMessageBox {
                background-color: #353535;
            }
            QMessageBox QLabel {
                color: white;
            }
        """)

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()

        # Header
        header = QLabel("File Organizer")
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("color: #aaa; margin-bottom: 15px;")

        # Directory selection group
        dir_group = QGroupBox("Folder to Organize")
        dir_layout = QVBoxLayout()

        self.dir_input = DraggableLineEdit()
        self.dir_input.setPlaceholderText("Select or drag a folder here...")

        browse_button = QPushButton("Browse Folder")
        browse_button.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
        browse_button.clicked.connect(self.browse_directory)

        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(browse_button)
        dir_group.setLayout(dir_layout)

        # Options group
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout()

        self.keep_sorted_checkbox = QCheckBox("Preserve existing organization")
        self.keep_sorted_checkbox.setChecked(True)
        self.keep_sorted_checkbox.setToolTip("When checked, keeps previously sorted files in their folders")

        options_layout.addWidget(self.keep_sorted_checkbox)
        options_group.setLayout(options_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()

        # Action buttons
        button_layout = QHBoxLayout()

        self.sort_button = QPushButton("Organize Files")
        self.sort_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowForward))
        self.sort_button.clicked.connect(self.start_sorting)
        self.sort_button.setToolTip("Organize files into categorized folders")

        self.undo_button = QPushButton("Undo Last Action")
        self.undo_button.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.undo_button.clicked.connect(self.start_undo)
        self.undo_button.setToolTip("Revert the last organization action")

        button_layout.addWidget(self.sort_button)
        button_layout.addWidget(self.undo_button)

        # Add widgets to main layout
        layout.addWidget(header)
        layout.addWidget(dir_group)
        layout.addWidget(options_group)
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)
        layout.addStretch(1)

        main_widget.setLayout(layout)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Folder to Organize")
        if directory:
            self.dir_input.setText(directory)

    def start_sorting(self):
        target_directory = self.dir_input.text().strip()
        if target_directory:
            self.progress_bar.show()
            keep_existing = self.keep_sorted_checkbox.isChecked()
            self.organize_directory(target_directory, keep_existing)
            self.progress_bar.hide()
        else:
            QMessageBox.warning(self, "Warning", "Please select a folder first.")

    def start_undo(self):
        self.progress_bar.show()
        self.undo_sorting()
        self.progress_bar.hide()

    def log_move(self, file, category):
        """Logs moved files."""
        logging.info(f"Moved: {file} → {category}/")

    def get_unique_filename(self, folder, filename):
        """Prevents overwriting by renaming duplicate files."""
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename

        while os.path.exists(os.path.join(folder, new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1

        return new_filename

    def save_sorting_history(self, original_path, new_path):
        """Saves original file locations to a history file for undo."""
        history = {}

        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r") as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = {}

        history[new_path] = original_path  # Store new_path -> original_path mapping

        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)

    def organize_directory(self, directory, keep_existing=True):
        """Sorts files into categorized folders inside a 'Sorted' directory."""
        if not os.path.exists(directory):
            QMessageBox.critical(self, "Error", "The selected folder does not exist.")
            return

        directory = os.path.abspath(directory)
        sorted_folder = os.path.join(directory, "Sorted")

        # Get all files to process
        try:
            files_to_process = [f for f in os.listdir(directory)
                                if os.path.isfile(os.path.join(directory, f)) and
                                not f.startswith('.')]  # Skip hidden files
        except PermissionError:
            QMessageBox.critical(self, "Error", f"Permission denied when accessing {directory}")
            return

        if not files_to_process:
            QMessageBox.information(self, "Info", "No files found to organize in the selected folder.")
            return

        # Create Sorted folder if it doesn't exist
        if not os.path.exists(sorted_folder):
            try:
                os.makedirs(sorted_folder)
            except PermissionError:
                QMessageBox.critical(self, "Error", f"Permission denied when creating {sorted_folder}")
                return

        # If not keeping existing, clean up previous sorted folders
        if not keep_existing:
            for category in FILE_CATEGORIES.keys():
                category_folder = os.path.join(sorted_folder, category)
                if os.path.exists(category_folder):
                    try:
                        shutil.rmtree(category_folder)
                    except PermissionError:
                        logging.error(f"Permission denied when removing {category_folder}")
                        continue
            others_folder = os.path.join(sorted_folder, "Others")
            if os.path.exists(others_folder):
                try:
                    shutil.rmtree(others_folder)
                except PermissionError:
                    logging.error(f"Permission denied when removing {others_folder}")

        total_files = len(files_to_process)
        processed_files = 0
        moved_files = 0
        skipped_files = 0

        for filename in files_to_process:
            file_path = os.path.join(directory, filename)
            self.progress_bar.setValue(int((processed_files / total_files) * 100))
            QApplication.processEvents()  # Keep UI responsive

            file_extension = os.path.splitext(filename)[1].lower()
            category = "Others"  # Default category

            for cat, extensions in FILE_CATEGORIES.items():
                if file_extension in extensions:
                    category = cat
                    break

            # Create category folder inside "Sorted/"
            category_folder = os.path.join(sorted_folder, category)
            if not os.path.exists(category_folder):
                try:
                    os.makedirs(category_folder)
                except PermissionError:
                    logging.error(f"Permission denied when creating {category_folder}")
                    continue

            # Check if file is already in the correct sorted location
            potential_new_path = os.path.join(category_folder, filename)
            if file_path == potential_new_path:
                skipped_files += 1
                processed_files += 1
                continue

            # Check if file is already sorted (maybe from previous run)
            already_sorted = False
            for cat in list(FILE_CATEGORIES.keys()) + ["Others"]:
                check_folder = os.path.join(sorted_folder, cat)
                if os.path.exists(os.path.join(check_folder, filename)):
                    already_sorted = True
                    break

            if already_sorted:
                skipped_files += 1
                processed_files += 1
                continue

            # Get unique filename if needed
            new_filename = self.get_unique_filename(category_folder, filename)
            new_file_path = os.path.join(category_folder, new_filename)

            # Move file
            try:
                shutil.move(file_path, new_file_path)
                self.log_move(filename, category)
                self.save_sorting_history(file_path, new_file_path)
                moved_files += 1
            except PermissionError:
                logging.error(f"Permission denied when moving {filename}")
            except Exception as e:
                logging.error(f"Failed to move {filename}: {str(e)}")

            processed_files += 1

        self.progress_bar.setValue(100)

        # Show summary of operations
        summary = []
        if moved_files > 0:
            summary.append(f"✓ Organized {moved_files} new files")
        if skipped_files > 0:
            summary.append(f"⏩ Skipped {skipped_files} already organized files")

        if summary:
            msg = QMessageBox(self)
            msg.setWindowTitle("Organization Complete")
            msg.setIcon(QMessageBox.Information)
            msg.setText("\n".join(summary))
            msg.exec_()
        else:
            QMessageBox.information(self, "Info", "No files needed to be organized.")

    def undo_sorting(self):
        """Moves files back to their original locations."""
        if not os.path.exists(HISTORY_FILE):
            QMessageBox.information(self, "Info", "No previous organization to undo.")
            return

        reply = QMessageBox.question(self, 'Confirm Undo',
                                     "This will move all files back to their original locations.\nDo you want to continue?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply != QMessageBox.Yes:
            return

        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Error", "Failed to read history file. It may be corrupted.")
            return

        total_files = len(history)
        processed_files = 0
        restored_files = 0
        failed_files = 0

        for new_path, original_path in history.items():
            self.progress_bar.setValue(int((processed_files / total_files) * 100))
            QApplication.processEvents()  # Keep UI responsive

            if os.path.exists(new_path):
                try:
                    # Ensure the original directory exists
                    original_dir = os.path.dirname(original_path)
                    if not os.path.exists(original_dir):
                        os.makedirs(original_dir)

                    shutil.move(new_path, original_path)
                    restored_files += 1
                except PermissionError:
                    logging.error(f"Permission denied when restoring {new_path}")
                    failed_files += 1
                except Exception as e:
                    logging.error(f"Failed to restore {new_path}: {str(e)}")
                    failed_files += 1
            else:
                logging.warning(f"File not found: {new_path}")
                failed_files += 1

            processed_files += 1

        self.progress_bar.setValue(100)

        # Clear history after undo
        try:
            if os.path.exists(HISTORY_FILE):
                os.remove(HISTORY_FILE)
        except PermissionError:
            logging.error(f"Permission denied when removing {HISTORY_FILE}")

        # Show summary
        summary = []
        if restored_files > 0:
            summary.append(f"✓ Restored {restored_files} files")
        if failed_files > 0:
            summary.append(f"✗ Failed to restore {failed_files} files")

        if summary:
            QMessageBox.information(self, "Undo Complete", "\n".join(summary))
        else:
            QMessageBox.information(self, "Info", "No files were restored.")


if __name__ == "__main__":
    # Enable high DPI scaling for Windows
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # Set application style for a more modern look
    app.setStyle("Fusion")

    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec_())