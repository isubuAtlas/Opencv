import cv2
import numpy as np
from pyzbar.pyzbar import decode
from collections import deque


def confirm_qr(data):
    print(f"===== QR CONFIRMED: {data} =====\n")


def main():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

    #  Ayarlar 
    CONFIRM_COUNT = 5
    BUFFER_SIZE = 10
    MIN_AREA = 500         
    CENTER_TOLERANCE = 150
    SCALE = 2    

    qr_buffer = deque(maxlen=BUFFER_SIZE)

    print("pyzbar QR Scanner started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image_center_x = frame.shape[1] // 2
        image_center_y = frame.shape[0] // 2

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        enlarged = cv2.resize(gray, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_CUBIC)

        decoded_objects = decode(enlarged)

        detected_this_frame = None

        for obj in decoded_objects:
            data = obj.data.decode("utf-8").strip()

            points = np.array([[p.x // SCALE, p.y // SCALE] for p in obj.polygon], dtype=np.int32)

            if len(points) == 4:
                rect = points
            else:
                hull = cv2.convexHull(points)
                rect = hull.reshape(-1, 2)

            area = cv2.contourArea(rect)
            qr_center_x = int(np.mean(rect[:, 0]))
            qr_center_y = int(np.mean(rect[:, 1]))

            cv2.line(frame,
                     (image_center_x, image_center_y),
                     (qr_center_x, qr_center_y),
                     (255, 0, 0), 2)

            for j in range(len(rect)):
                cv2.line(frame,
                         tuple(rect[j]),
                         tuple(rect[(j + 1) % len(rect)]),
                         (0, 255, 0), 2)

            cv2.putText(frame, data,
                        (10,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.5, (0, 255, 0), 5)

            near_center = (abs(qr_center_x - image_center_x) < CENTER_TOLERANCE and
                           abs(qr_center_y - image_center_y) < CENTER_TOLERANCE)

            if area > MIN_AREA and near_center:
                detected_this_frame = data
                break

        qr_buffer.append(detected_this_frame if detected_this_frame else None)

        non_none = [d for d in qr_buffer if d]
        if non_none:
            most_common = max(set(non_none), key=non_none.count)
            count = non_none.count(most_common)
            if count >= CONFIRM_COUNT:
                confirm_qr(most_common)
                qr_buffer.clear()

        cv2.circle(frame, (image_center_x, image_center_y), 6, (255, 0, 0), -1)

        cv2.imshow("pyzbar QR Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()