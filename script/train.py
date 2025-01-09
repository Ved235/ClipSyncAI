from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO("yolov8n.pt")  # Use a pre-trained model (n=Nano, s=Small, etc.)

# Train the model
model.train(data="data/data.yaml", epochs=50, imgsz=640)

