import cv2
import numpy as np
import os
import urllib.request
import sys

MODEL_URLS = {
    "detect.prototxt": "https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/wechat_qrcode/detect.prototxt",
    "detect.caffemodel": "https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/wechat_qrcode/detect.caffemodel",
    "sr.prototxt": "https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/wechat_qrcode/sr.prototxt",
    "sr.caffemodel": "https://raw.githubusercontent.com/WeChatCV/opencv_3rdparty/wechat_qrcode/sr.caffemodel"
}

def download_models():
    if not os.path.exists("models"):
        os.makedirs("models")
    
    print("Checking for WeChatQRCode models...")
    for filename, url in MODEL_URLS.items():
        filepath = os.path.join("models", filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename}...")
            try:
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f"Error downloading {filename}: {e}")
                sys.exit(1)
    print("All models ready.")

def main():
    # 1. Ensure models are present
    download_models()

    detector = cv2.wechat_qrcode_WeChatQRCode(
        "models/detect.prototxt", 
        "models/detect.caffemodel", 
        "models/sr.prototxt", 
        "models/sr.caffemodel"
    )

    cap = cv2.VideoCapture(0)
    # Set high resolution for better long-distance detection
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1) # Ensure autofocus is ON

    print("Scanner started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        res, points = detector.detectAndDecode(frame)

        # 4. Draw results
        if len(res) > 0:
            for i, data in enumerate(res):
                rect = points[i].astype(int)
                
                for j in range(4):
                    cv2.line(frame, tuple(rect[j]), tuple(rect[(j+1)%4]), (0, 255, 0), 2)
                
                # Draw text with background for readability
                text_pos = (rect[0][0], rect[0][1] - 10)
                (w, h), _ = cv2.getTextSize(data, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                
                # Ensure text doesn't go off-screen
                t_x = max(text_pos[0], 0)
                t_y = max(text_pos[1], h + 5)
                
                cv2.rectangle(frame, (t_x, t_y - h - 5), (t_x + w, t_y + 5), (0,0,0), -1)
                cv2.putText(frame, data, (t_x, t_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                print(f"Decoded: {data}")

        cv2.imshow("WeChat QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()