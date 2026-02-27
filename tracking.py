from pid import FlightPID
import cv2
import numpy as np

pid = FlightPID()
cap = cv2.VideoCapture(0)

BASE_PWM = 1500

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Örnek error (gerçek detection yerine)
    error = 50

    control = pid.update(error)
    pwm = int(BASE_PWM + control)

    print("PWM:", pwm)

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()