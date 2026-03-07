import cv2

def init(frame, bbox):
    # Options: CSRT (accurate), KCF (fast), MOSSE (fastest)
    tracker = cv2.TrackerCSRT_create() 
    tracker.init(frame, bbox)
    return tracker

def update(tracker, frame, screen_cx, screen_cy):
    success, bbox = tracker.update(frame)

    if success:
        x, y, w, h = map(int, bbox)
        cx = x + w // 2
        cy = y + h // 2
        
        # Draw bounding box and center point
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
        
        # Draw status text
        cv2.putText(frame, "TRACKING", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Draw aiming line
        cv2.line(frame, (screen_cx, screen_cy), (cx, cy), (0, 255, 0), 2)

    else:
        cv2.putText(frame, "TRACKING LOST", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    return frame, success, bbox if success else None