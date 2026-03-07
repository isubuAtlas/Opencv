from ultralytics import YOLO
import cv2
import time
import threading
from collections import deque
import tracking 

# ==========================================
# 1. CAMERA STREAM CLASS
# ==========================================
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
            time.sleep(1 / self.fps)

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

# ==========================================
# 2. MAIN CONFIGURATION & VARIABLES
# ==========================================
IHA_CLASS_ID = 2

# Failsafe Settings
EDGE_MARGIN = 15
LOCK_THRESHOLD = 3
MAX_LOST_FRAMES = 15
VALIDATION_INTERVAL = 10 

stream = CameraStream(0).start()
model = YOLO("best.engine", task="detect")
wait_ms = int(1000 / stream.fps) if stream.is_file else 1

fps_buffer = deque(maxlen=30)
prev_time = time.time()

# State Machine Variables
state = "DETECTION"
locked_frames = 0
lost_frames = 0
frames_since_validation = 0
failed_validations = 0
tracker = None
best_bbox = None

# ==========================================
# 3. MAIN LOOP
# ==========================================
while True:
    if stream.stopped:
        break

    frame = stream.read()
    if frame is None:
        continue

    frame_h, frame_w = frame.shape[:2]
    screen_cx, screen_cy = frame_w // 2, frame_h // 2

    # ---------------------------------------------------------
    # YOLO INFERENCE (DETECTION, ACQUIRING, SEARCHING)
    # ---------------------------------------------------------
    if state in ["DETECTION", "ACQUIRING", "SEARCHING"]:
        results = model.track(source=frame, conf=0.5, persist=True, device="cuda", half=True, imgsz=640, verbose=False)
        
        iha_found_this_frame = False

        if results:
            frame = results[0].plot()
            for box in results[0].boxes:
                if int(box.cls) == IHA_CLASS_ID and float(box.conf) > 0.6:
                    obj_cx, obj_cy, w, h = map(int, box.xywh[0])
                    
                    x1 = int(obj_cx - (w / 2))
                    y1 = int(obj_cy - (h / 2))
                    best_bbox = (x1, y1, w, h)
                    
                    cv2.line(frame, (screen_cx, screen_cy), (obj_cx, obj_cy), (0, 0, 255), 2)
                    iha_found_this_frame = True
                    break 

        if iha_found_this_frame:
            if state == "DETECTION":
                state = "ACQUIRING"
                locked_frames = 1
            elif state == "ACQUIRING":
                locked_frames += 1
                if locked_frames >= LOCK_THRESHOLD:
                    tracker = tracking.init(frame, best_bbox)
                    state = "LOCKED"
                    frames_since_validation = 0
                    failed_validations = 0
            elif state == "SEARCHING":
                tracker = tracking.init(frame, best_bbox)
                state = "LOCKED"
                frames_since_validation = 0
                failed_validations = 0
        else:
            if state == "ACQUIRING":
                state = "DETECTION"
                locked_frames = 0
            elif state == "SEARCHING":
                lost_frames += 1
                if lost_frames >= MAX_LOST_FRAMES:
                    state = "DETECTION"

    # ---------------------------------------------------------
    # CSRT TRACKING (LOCKED)
    # ---------------------------------------------------------
    elif state == "LOCKED":
        frame, success, kcf_bbox = tracking.update(tracker, frame, screen_cx, screen_cy)
        frames_since_validation += 1

        if success:
            x, y, w, h = map(int, kcf_bbox)
            
            # --- 1. Edge Kill Switch ---
            if x < EDGE_MARGIN or y < EDGE_MARGIN or (x + w) > (frame_w - EDGE_MARGIN) or (y + h) > (frame_h - EDGE_MARGIN):
                print("Target hit frame boundary. Dropping track.")
                success = False

            # --- 2. YOLO Validation Check (Center-in-Box + Strike System) ---
            elif frames_since_validation >= VALIDATION_INTERVAL:
                frames_since_validation = 0
                
                # Using predict() instead of track() to avoid ByteTrack ID conflicts
                val_results = model.predict(source=frame, conf=0.45, device="cuda", half=True, imgsz=640, verbose=False)
                yolo_confirmed = False
                
                if val_results:
                    for box in val_results[0].boxes:
                        if int(box.cls) == IHA_CLASS_ID:
                            obj_cx, obj_cy, _, _ = map(int, box.xywh[0])
                            
                            # 20 pixel margin to allow for slight bounding box differences
                            margin = 20
                            if (x - margin) < obj_cx < (x + w + margin) and \
                               (y - margin) < obj_cy < (y + h + margin):
                                yolo_confirmed = True
                                break
                
                if yolo_confirmed:
                    failed_validations = 0 
                else:
                    failed_validations += 1
                    print(f"Validation Warning: YOLO missed target (Strike {failed_validations}/2)")
                    if failed_validations >= 2:
                        print("Validation Failed permanently. Dropping track.")
                        success = False
                        failed_validations = 0

        if success:
            lost_frames = 0
        else:
            state = "SEARCHING"
            lost_frames = 0
            tracker = None
            failed_validations = 0

    # ---------------------------------------------------------
    # OVERLAYS & FPS
    # ---------------------------------------------------------
    cv2.circle(frame, (screen_cx, screen_cy), 6, (0, 0, 255), -1)

    curr_time = time.time()
    fps_buffer.append(1 / (curr_time - prev_time))
    prev_time = curr_time
    avg_fps = sum(fps_buffer) / len(fps_buffer)

    colors = {
        "DETECTION": (0, 255, 255),
        "ACQUIRING": (255, 255, 0),
        "LOCKED": (0, 255, 0),
        "SEARCHING": (0, 165, 255)
    }
    mode_color = colors.get(state, (255, 255, 255))

    cv2.putText(frame, f"FPS: {int(avg_fps)}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(frame, f"MODE: {state}", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, mode_color, 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(wait_ms) == ord("q"):
        break

stream.stop()
cv2.destroyAllWindows()