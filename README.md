## İHA YAZILIM AlGORİTMALARI DAĞILIM ŞEMASI

# Siha_algoritma/

```text
gorev_yoneticisi.py # Ana program, döngü, başlatma
durum_makinesi.py # Görev durumları (KALKIŞ, ARAMA, KİLİT, QR...)
karar_verme.py # Duruma göre aksiyon seçimi (RL + kural tabanlı)
haberlesme.py # MAVLink ile Pixhawk haberleşmesi
guvenlik.py # Geofence, irtifa/hız sınırları
fail_safe.py # Acil durum yönetimi (bağlantı kopması, pil)
fotograf_gonderici.py # 4 saniyede bir yer istasyonuna fotoğraf
yer_istasyonu.py # Özel komutlar, telemetri loglama (opsiyonel)
rota_planlama.py # Görev noktalarını yükleme, sıralama
veri_kaydi.py # Uçuş verilerini ve deneyimleri kaydetme
logger.py # Loglama sistemi
```
```bash
\görüntü_işleme # Görüntü işleme modülü
\nesne_tespiti.py # YOLO ile nesne tespiti
\nesne_takibi.py # Nesne takibi (CSRT veya Re3 benzeri)
\görüntü_stab.py # Görüntü sabitleme sınıfı
\kalman.py #Kalman filtresi sınıfı
\qr_okuyucu.py
```
```text
\tahmin etme alg.
\ model.py # Ağ mimarisi (aktör, eleştiri)
\ödül_hesaplama.py # Durum ve ödül hesaplama fonksiyonları
\ per_güncel.py # RL ajanı (buffer, güncelleme)
\trainer.py # (opsiyonel) periyodik eğitim döngüsü

\yard_fonk.py # Yardımcı fonksiyonlar (açı hesaplama vb.)


\ayarlar.py # Tüm ayarlar (PID katsayıları, port, vs.)
```

