# 📂 File Organizer

A Python-based file sorting script with a GUI using Tkinter. It organizes files in a selected directory into categorized folders such as **Images, Videos, Documents, Music, Archives, Executables, and Code**. It also supports **undoing** the sorting process.

![Unsorted](unshorted.png)  
*Example of an unsorted directory.*

## 🚀 Features
- Automatically sorts files into appropriate folders.
- Supports undo functionality to restore files to their original locations.
- Prevents overwriting by renaming duplicate files.
- Uses a **GUI (Tkinter)** for easy directory selection.
- Saves sorting history in a JSON file for undo functionality.
- Logs moved files in `file_sorting.log`.

## 📌 Requirements
Ensure you have the following installed:
- **Python 3.x**
- Required libraries:
  ```bash
  pip install tk
  ```

## 📁 File Categories
| Category      | Extensions |
|--------------|------------|
| **Images**    | `.jpg, .jpeg, .png, .gif, .bmp, .svg, .webp` |
| **Videos**    | `.mp4, .mkv, .flv, .avi, .mov, .wmv` |
| **Documents** | `.pdf, .docx, .doc, .txt, .xlsx, .pptx, .csv` |
| **Music**     | `.mp3, .wav, .aac, .flac, .ogg` |
| **Archives**  | `.zip, .rar, .7z, .tar, .gz` |
| **Executables** | `.exe, .msi, .sh, .bat` |
| **Code**      | `.py, .js, .html, .css, .cpp, .java, .c, .php` |

## 🖼️ Before & After
### ❌ Before Sorting (Unsorted)
![Unsorted](unshorted.png)

### ✅ After Sorting (Sorted)
![Sorted](shorted.png)

## 📝 Logging
- All moved files are logged in `file_sorting.log`.

## 📜 License
This project is **open-source** under the MIT License.
