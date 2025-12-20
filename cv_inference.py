from ultralytics import YOLO
import cv2

class RoadScanner:
    def __init__(self, model_path):
        # Load the model you trained (path will usually be in runs/...)
        self.model = YOLO(model_path)

    def scan_image(self, image_source): 
    # image_source can be a file path string OR a numpy array (cv2 image)
    
        """
        Returns a dictionary with status and safety score.
        """
        # Run prediction
        results = self.model(image_source)
        
        # Extract results
        # names maps index to label (e.g., {0: 'hazardous', 1: 'safe'})
        probs = results[0].probs
        
        # Get the probability of it being "hazardous"
        # We assume label 'hazardous' is index 0 or 1. We check names to be sure.
        class_dict = results[0].names
        
        hazard_index = None
        for k, v in class_dict.items():
            if v == 'hazardous':
                hazard_index = k
                break
        
        hazard_prob = float(probs.data[hazard_index])
        
        return {
            "is_hazardous": hazard_prob > 0.5,
            "hazard_score": hazard_prob, # Use this for your graph edge weights!
            "prediction": class_dict[probs.top1]
        }

# Example usage
if __name__ == "__main__":
    # Point this to your "best.pt" file created after running train_model.py
    scanner = RoadScanner('road_safety_project/hazard_classifier/weights/best.pt')
    
    result = scanner.scan_image('images/h_pics/h1_1.png')
    print(f"Road Analysis: {result}")