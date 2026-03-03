from ultralytics import YOLO

# Sıfırdan, temiz bir zihinle başlıyoruz
model = YOLO('yolov8n.pt') 

if __name__ == '__main__':
    model.train(
        data='final_dataset/data.yaml', # Orijinal ve 5.000 İHA'ya düşürülmüş veri setin
        epochs=50,                      # 50 turluk test eğitimi
        imgsz=640,
        device=0,                       # GTX 1650 ekran kartını kullanıyoruz
        workers=2,                      # İşlemciyi boğmamak için
        name='savasan_iha_v2_temiz'     # Yeni modelinin kaydedileceği klasör adı
    )