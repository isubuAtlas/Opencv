<<<<<<< HEAD
import os

label_folders = [
    "final_dataset/train/labels",
    "final_dataset/valid/labels",
    "final_dataset/test/labels"
]

total_files = 0
total_objects = 0
iha_count = 0
bird_count = 0

for folder in label_folders:
    for file in os.listdir(folder):
        total_files += 1
        path = os.path.join(folder, file)

        with open(path, "r") as f:
            lines = f.readlines()
            total_objects += len(lines)

            for line in lines:
                class_id = int(line.split()[0])
                if class_id == 2:
                    iha_count += 1
                elif class_id == 1:
                    bird_count += 1

print("Toplam label dosyası:", total_files)
print("Toplam obje:", total_objects)
print("IHA sayısı:", iha_count)
print("Kuş sayısı:", bird_count)
=======
import os

label_folders = [
    "final_dataset/train/labels",
    "final_dataset/valid/labels",
    "final_dataset/test/labels"
]

total_files = 0
total_objects = 0
iha_count = 0
bird_count = 0

for folder in label_folders:
    for file in os.listdir(folder):
        total_files += 1
        path = os.path.join(folder, file)

        with open(path, "r") as f:
            lines = f.readlines()
            total_objects += len(lines)

            for line in lines:
                class_id = int(line.split()[0])
                if class_id == 2:
                    iha_count += 1
                elif class_id == 1:
                    bird_count += 1

print("Toplam label dosyası:", total_files)
print("Toplam obje:", total_objects)
print("IHA sayısı:", iha_count)
print("Kuş sayısı:", bird_count)
>>>>>>> ca300630efc322be52ec4652b8ea01f7244fe926
