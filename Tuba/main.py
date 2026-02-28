import cv2
import time
import config
from ultralytics import YOLO
from pid import PID
from tracker import Tracker

def main():

    model = YOLO(config.MODEL_PATH)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Kamera açılamadı")
        return

    pid = PID()
    tracker = Tracker()

    prev_time = time.time()
    frame_count = 0

    smoothed_x = None  # 🔥 center filtresi

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_h, frame_w = frame.shape[:2]
        frame_center_x = frame_w // 2

        results = model(frame, verbose=False)

        detection_center = None
        best_conf = 0

        # 🔥 En güvenli detection seç
        for r in results:
            for box in r.boxes:
                conf = float(box.conf[0])

                if conf > config.CONF_THRESHOLD and conf > best_conf:
                    best_conf = conf
                    x1, y1, x2, y2 = box.xyxy[0]
                    cx = int((x1 + x2) / 2)
                    cy = int((y1 + y2) / 2)
                    detection_center = (cx, cy)

        if detection_center is not None:

            tracked = tracker.update(*detection_center)

            if tracked is not None:

                tracked_x, tracked_y = tracked

                # 🔥 LOW PASS FILTER (bounding box jitter azaltma)
                if smoothed_x is None:
                    smoothed_x = tracked_x
                else:
                    smoothed_x = 0.8 * smoothed_x + 0.2 * tracked_x

                error = frame_center_x - smoothed_x

                # 🔥 Her 2 frame'de bir PID (stabilite için)
                if frame_count % 2 == 0:
                    control = pid.update(error)

                    pwm = int(config.PWM_NEUTRAL + control * 500)
                    pwm = max(config.PWM_MIN, min(config.PWM_MAX, pwm))

                    print(f"PWM: {pwm} | Error: {int(error)}")

                # Görsel debug
                cv2.circle(frame, (int(smoothed_x), tracked_y), 6, (0,255,0), -1)
                cv2.line(frame, (frame_center_x,0), (frame_center_x,frame_h), (255,0,0), 2)

        # FPS
        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.putText(frame, f"FPS: {int(fps)}", (20,40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.imshow("Tracking", frame)

        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()