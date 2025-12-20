from ultralytics import YOLO
import cv2

class RoadScanner:
    """
    A wrapper class for the YOLOv8 classification model.
    It simplifies the complex model output into a simple score for the graph.
    """

    def __init__(self, model_path):
        """
        Initialize the scanner by loading the trained weights.
        
        Args:
            model_path (str): Path to the .pt file (e.g., 'runs/detect/train/weights/best.pt')
        """
        print(f"Loading AI Model from {model_path}...")
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def scan_image(self, image_source):
        """
        Analyzes a single image and returns a hazard report.
        
        Args:
            image_source: Can be a file path (str) OR a numpy array (loaded by cv2.imread).
                          This flexibility is crucial because create_nodes.py loads images 
                          as numpy arrays.
        
        Returns:
            dict: Contains 'is_hazardous' (bool), 'hazard_score' (0.0-1.0), and the label.
        """
        # Run the image through the neural network
        results = self.model(image_source, verbose=False)
        
        # The result object contains 'probs' (probabilities)
        probs = results[0].probs
        class_dict = results[0].names  # e.g., {0: 'hazardous', 1: 'safe'}
        
        # We need to find which index corresponds to "hazardous"
        # because YOLO might assign it index 0 or index 1 depending on folder order.
        hazard_index = None
        for k, v in class_dict.items():
            if v == 'hazardous':
                hazard_index = k
                break
        
        # If the model predicts the "hazardous" class, get that probability.
        # If 'hazardous' wasn't one of the classes, default to 0.0.
        if hazard_index is not None:
            hazard_prob = float(probs.data[hazard_index])
        else:
            hazard_prob = 0.0
        
        # Return a standardized dictionary that the Graph Builder can easily use
        return {
            "is_hazardous": hazard_prob > 0.5, # True if more than 50% sure it's bad
            "hazard_score": hazard_prob,       # Exact score (e.g., 0.85)
            "prediction": class_dict[probs.top1] # The text label (e.g., "hazardous")
        }

# --- TEST BLOCK ---
# This only runs if you run this file directly (not when imported by create_graph.py)
if __name__ == "__main__":
    # Define where the trained model lives
    model_path = 'road_safety_project/hazard_classifier/weights/best.pt'
    
    # Check if the model exists before trying to load it
    import os
    if os.path.exists(model_path):
        scanner = RoadScanner(model_path)
        
        # Test it on a specific image (change this path to test different images)
        test_img = 'images/h_pics/h1_1.png'
        if os.path.exists(test_img):
            result = scanner.scan_image(test_img)
            print(f"Test Result for {test_img}:")
            print(result)
        else:
            print(f"Test image not found: {test_img}")
    else:
        print("Model file not found. Run train_model.py first!")