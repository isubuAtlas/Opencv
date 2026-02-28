import os

# Görsel ve etiket klasörlerinin yolları
image_folders = [
    "final_dataset/train/images",
    "final_dataset/valid/images",
    "final_dataset/test/images"
]
label_folders = [
    "final_dataset/train/labels",
    "final_dataset/valid/labels",
    "final_dataset/test/labels"
]

MIN_SIZE = 0.02   # Görüntünün %2'sinden küçükse
IHA_CLASS_ID = 2  # Senin listene göre İHA'nın ID'si

deleted_count = 0

for img_folder, lbl_folder in zip(image_folders, label_folders):
    if not os.path.exists(lbl_folder):
        continue
        
    for label_file in os.listdir(lbl_folder):
        lbl_path = os.path.join(lbl_folder, label_file)

        with open(lbl_path, "r") as f:
            lines = f.readlines()

        should_delete = False
        for line in lines:
            parts = line.strip().split()
            if len(parts) < 5: continue
            
            class_id = int(parts[0])
            width = float(parts[3])
            height = float(parts[4])

            # Eğer obje İHA ise VE çok küçükse, bu görseli fişle
            if class_id == IHA_CLASS_ID and (width < MIN_SIZE or height < MIN_SIZE):
                should_delete = True
                break 

        # Eğer görsel fişlendiyse kökünden sil
        if should_delete:
            os.remove(lbl_path) # txt'yi sil
            
            # Aynı isimdeki fotoğrafı bul ve sil (.jpg veya .png olabilir)
            base_name = os.path.splitext(label_file)[0]
            for ext in [".jpg", ".png", ".jpeg"]:
                img_path = os.path.join(img_folder, base_name + ext)
                if os.path.exists(img_path):
                    os.remove(img_path)
                    break
                    
            deleted_count += 1

print(f"Büyük Operasyon Tamamlandı! Toplam {deleted_count} adet çöp görsel tamamen silindi.")