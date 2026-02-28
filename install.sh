#!/bin/bash

# Renkler
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${GREEN}Sistem güncelleniyor...${NC}"
sudo apt update && sudo apt upgrade -y

echo -e "${GREEN}Sistem bağımlılıkları yükleniyor (OpenCV ve PyZbar için)...${NC}"
sudo apt install -y python3-pip libzbar0 libgl1-mesa-glx libglib2.0-0

echo -e "${GREEN}Python kütüphaneleri requirements.txt üzerinden sistem genelinde kuruluyor...${NC}"
# --break-system-packages parametresi Raspberry Pi OS Bookworm (Debian 12) için gereklidir.
sudo pip install -r requirements.txt --break-system-packages

echo -e "${GREEN}Kurulum başarıyla tamamlandı!${NC}"
