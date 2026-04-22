import os
import shutil

DOWNLOADS_FOLDER = os.path.expanduser("~/Downloads")

FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx"],
    "Videos": [".mp4", ".mkv"],
    "Zips": [".zip", ".rar"],
    "Others": []
}

def get_folder(file_name):
    for folder, extensions in FILE_TYPES.items():
        for ext in extensions:
            if file_name.endswith(ext):
                return folder
    return "Others"


def organize():
    for file in os.listdir(DOWNLOADS_FOLDER):
        file_path = os.path.join(DOWNLOADS_FOLDER, file)

        if os.path.isfile(file_path):
            folder_name = get_folder(file)

            target_folder = os.path.join(DOWNLOADS_FOLDER, folder_name)
            os.makedirs(target_folder, exist_ok=True)

            shutil.move(file_path, os.path.join(target_folder, file))
            print(f"Moved: {file} -> {folder_name}")


if __name__ == "__main__":
    organize()