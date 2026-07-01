import cv2
from ultralytics import YOLO
import os
import time

# Which folder to save into — change to "cat_b" when capturing the other cat
SAVE_DIR = "cat_b"
os.makedirs(SAVE_DIR, exist_ok=True)

model = YOLO("yolov8n.pt")  # nano model, auto-downloads first run
CAT_CLASS = 15  # "cat" in COCO

# Open camera. iPhone via Continuity is often index 0 or 1 — try 0 first,
# if you get the wrong camera, change to 1.
cap = cv2.VideoCapture(0)

saved = 0
while True:
    ok, frame = cap.read()
    if not ok:
        break

    results = model(frame, verbose=False)[0]
    crop = None

    for box in results.boxes:
        if int(box.cls) == CAT_CLASS and float(box.conf) > 0.5:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            crop = frame[y1:y2, x1:x2]  # the cat region

    cv2.putText(frame, f"Saved: {saved}  Press 's' to save, 'q' to quit",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Cat capture", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("s") and crop is not None and crop.size > 0:
        fn = os.path.join(SAVE_DIR, f"{int(time.time()*1000)}.jpg")
        cv2.imwrite(fn, crop)
        saved += 1
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()