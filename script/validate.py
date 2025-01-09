from ultralytics import YOLO

# Load the trained model
model = YOLO("runs/detect/train12/weights/best.pt")

# Print out the class names and their IDs
# Assuming 'model' is your loaded YOLO model
print(model.names)  # Prints the list of class names with their corresponding IDs

# Validate the model
model.val(data="data/data.yaml")
