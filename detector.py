from ultralytics import YOLO
import config

class DroneDetector:
    def __init__(self):
        self.model = YOLO(config.MODEL_PATH)

    def detect(self, frame):
        results = self.model(frame, verbose=False)

        boxes = results[0].boxes

        if boxes is None or len(boxes) == 0:
            return None

        # Confidence filtresi
        filtered = [b for b in boxes if float(b.conf[0]) > config.CONF_THRESHOLD]

        if len(filtered) == 0:
            return None

        # En büyük box seç
        best_box = max(
            filtered,
            key=lambda b: (b.xyxy[0][2]-b.xyxy[0][0]) *
                          (b.xyxy[0][3]-b.xyxy[0][1])
        )

        x1, y1, x2, y2 = best_box.xyxy[0]
        center_x = int((x1 + x2) / 2)
        center_y = int((y1 + y2) / 2)

        return center_x, center_y