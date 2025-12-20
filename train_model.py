from ultralytics import YOLO

def train():
    """
    Loads a pre-trained YOLOv8 model and fine-tunes it on our road data.
    """
    
    # 1. Load the Model
    # 'yolov8n-cls.pt' is the "Nano" classification model. 
    # It is small, fast, and good for running on laptops without massive GPUs.
    # It has already been trained on millions of images (ImageNet), so it knows basic shapes.
    print("Loading YOLOv8 Nano model...")
    model = YOLO('yolov8n-cls.pt') 

    # 2. Train the Model
    # This loop feeds our images into the neural network.
    print("Starting training...")
    results = model.train(
        data='dataset_cls',  # Points to the folder created by prepare_data.py
        epochs=20,           # How many times it sees the whole dataset. 20 is a good start.
        imgsz=224,           # Resizes all images to 224x224 pixels (standard for AI).
        project='road_safety_project', # The name of the output folder.
        name='hazard_classifier'       # The specific name for this run.
    )
    
    # 3. Validate
    # After training, we run a check to see how accurate it is on images it hasn't seen.
    metrics = model.val()
    print(f"Top-1 Accuracy: {metrics.top1}")
    print("Training complete. The best model is saved in 'road_safety_project/hazard_classifier/weights/best.pt'")

if __name__ == '__main__':
    train()