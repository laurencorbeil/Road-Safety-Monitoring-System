from ultralytics import YOLO

def train():
    # 1. Load a pre-trained model (yolov8n-cls.pt is the nano classification model)
    model = YOLO('yolov8n-cls.pt') 

    # 2. Train the model
    # 'data' argument points to the folder we created in Step 1
    results = model.train(
        data='dataset_cls', 
        epochs=20,           # Adjust based on how fast your computer is
        imgsz=224,           # Standard size for classification
        project='road_safety_project',
        name='hazard_classifier'
    )
    
    # 3. Validate performance
    metrics = model.val()
    print(f"Top-1 Accuracy: {metrics.top1}")

if __name__ == '__main__':
    train()