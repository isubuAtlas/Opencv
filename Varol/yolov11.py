from ultralytics import YOLO
import cv2
import time
import threading

class CameraStream:
    def __init__(self, src=0):
        self.src = src
        self.cap = cv2.VideoCapture(src)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0 or self.fps > 120: self.fps = 30
        self.ret = False
        self.frame = None
        self.stopped = False
        self.is_file = isinstance(src, str)

    def start(self):
        if not self.is_file:
            threading.Thread(target=self.update, daemon=True).start()
        return self

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if not ret:
                self.stop()
                break
            self.frame = frame
            self.ret = True
            time.sleep(0.005)

    def read(self):
        if self.is_file:
            ret, frame = self.cap.read()
            if not ret:
                self.stopped = True
                return None
            return frame
        return self.frame if self.ret else None

    def stop(self):
        self.stopped = True
        self.cap.release()

video_path = r"C:\Users\Varol\Desktop\Python\drone_test.mp4"
stream = CameraStream(video_path).start()
model = YOLO("yolo11s.engine", task="detect")

wait_ms = int(1000 / stream.fps) if stream.is_file else 1
prev_time = time.time()

while True:
    if stream.stopped:
        break

    frame = stream.read()
    if frame is None:
        continue

    t0 = time.time()
    
    results = model.predict(
        source=frame,
        conf=0.4,
        iou=0.4,
        device="cuda",
        half=True,
        imgsz=640,
        verbose=False
    )

    # results = model.track(source=frame, persist=True)
    
    infer_time = time.time() - t0
    infer_fps = 1 / infer_time

    for r in results:
        frame = r.plot()

    cv2.putText(frame, f"INF FPS: {int(infer_fps)}", (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    cv2.imshow("YOLO11 Player", frame)

    if cv2.waitKey(wait_ms) == ord("q"):
        break

stream.stop()
cv2.destroyAllWindows()