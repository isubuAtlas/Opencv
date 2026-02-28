<<<<<<< HEAD
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    results = model(frame, conf=0.75)  # confidence yükselttik
    
    annotated_frame = frame.copy()

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            # SADECE IHA ÇİZ
            if class_name == "iha":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(annotated_frame, f"iha {conf:.2f}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0,255,0),
                            2)

    cv2.imshow("Drone Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
=======
from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/train3/weights/best.pt")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    results = model(frame, conf=0.75)  # confidence yükselttik
    
    annotated_frame = frame.copy()

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            # SADECE IHA ÇİZ
            if class_name == "iha":
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(annotated_frame, f"iha {conf:.2f}",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0,255,0),
                            2)

    cv2.imshow("Drone Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
>>>>>>> ca300630efc322be52ec4652b8ea01f7244fe926
