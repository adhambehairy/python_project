import os
import shutil

# 1. Path to your Downloads folder
folder_path = "Downloads"

# 2. File categories
file_types = {
    "PDF": [".pdf"],
    "Images": [".jpg", ".png", ".jpeg",".JPG"],
    "Videos": [".mp4", ".mkv"],
    "Others": []
}

# 3. Create folders if not exist
for folder in file_types.keys():
    path = os.path.join(folder_path, folder)
    if not os.path.exists(path):
        os.mkdir(path)

# 4. Loop through files
for file in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file)

    # Skip folders
    if os.path.isdir(file_path):
        continue

    moved = False
    
    for folder_name, extensions in file_types.items():
        for ext in extensions:
            if file.endswith(ext):
                shutil.move(file_path, os.path.join(folder_path, folder_name, file))
                print(f"Moved: {file} → {folder_name}")
                moved = True
                break
        if moved:
            break

    # 6. If no match → Others
    if not moved:
        shutil.move(file_path, os.path.join(folder_path, "Others", file))
        print(f"Moved: {file} → Others")