import os
from collections import Counter

labels_path = "final_dataset/train/labels"
  # eğer hata verirse yolu değiştiririz

counter = Counter()

for file in os.listdir(labels_path):
    if file.endswith(".txt"):
        with open(os.path.join(labels_path, file), "r") as f:
            for line in f:
                class_id = line.strip().split()[0]
                counter[class_id] += 1

print("Class dağılımı:")
for k, v in sorted(counter.items()):
    print(f"Class {k}: {v} adet")
