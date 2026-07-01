import cv2, torch, torch.nn as nn
from torchvision import transforms, models
from ultralytics import YOLO

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
classes = ["cat_a", "cat_b"]

# rebuild the same architecture and load your trained weights
model = models.resnet18()
model.fc = nn.Linear(model.fc.in_features, 2)
model.load_state_dict(torch.load("cat_model.pth", map_location=device))
model.to(device).eval()

tf = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

detector = YOLO("yolov8n.pt")
cap = cv2.VideoCapture(0)

while True:
    ok, frame = cap.read()
    if not ok: break
    results = detector(frame, verbose=False)[0]
    for box in results.boxes:
        if int(box.cls) == 15 and float(box.conf) > 0.5:   # cat
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0: continue
            with torch.no_grad():
                t = tf(crop).unsqueeze(0).to(device)
                probs = torch.softmax(model(t), 1)[0]
                idx = int(probs.argmax())
                conf = float(probs[idx])
            label = f"{classes[idx]} {conf:.0%}"
            cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
            cv2.putText(frame, label, (x1, y1-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
    cv2.imshow("Cat ID", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cap.release(); cv2.destroyAllWindows()