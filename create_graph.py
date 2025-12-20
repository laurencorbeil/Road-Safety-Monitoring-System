# This file is used to turn nodes into a graphical format
# Updated to include Computer Vision integration for safety scoring

# Try to import the RoadScanner from our inference file
# I (skyler) made it use try/except so the graph still works even if the AI model isn't trained yet
try:
    from cv_inference import RoadScanner
except ImportError:
    RoadScanner = None

class create_graph:

    # INITIALIZE EMPTY GRAPH
    def __init__(self, model_path='road_safety_project/hazard_classifier/weights/best.pt'):
        self.nodes = {}
        self.adjacency = {}
        
        # Initialize the AI Model if available
        self.scanner = None
        if RoadScanner:
            try:
                # Initialize the model with the path to our trained weights
                self.scanner = RoadScanner(model_path)
                print("AI Road Scanner loaded successfully.")
            except Exception as e:
                print(f"Warning: Could not load AI model. Graph will use default weights. ({e})")
        else:
            print("Warning: cv_inference.py not found. AI safety features are disabled.")

    def get_node_safety_score(self, node):
        """
        Analyzes all images attached to a node to calculate a safety score.
        Returns a float between 0.0 (Safe) and 1.0 (Hazardous).
        """
        # If AI is disabled or node has no images, assume it's safe (0.0)
        if not self.scanner or not node.images:
            return 0.0

        scores = []
        for img_data in node.images:
            # We use the raw image (numpy array) stored in 'picture' by create_nodes.py
            image = img_data.get('picture')
            
            # Only scan if the image was loaded successfully
            if image is not None:
                # Scan the image using the loaded AI model
                # Note: Ensure our cv_inference.py accepts numpy arrays (cv2 images)
                result = self.scanner.scan_image(image)
                scores.append(result['hazard_score'])
        
        # Strategy: Return the average hazard score of all images at this location
        if scores:
            return sum(scores) / len(scores)
        
        return 0.0

    def build_graph(self, all_nodes):
        # STORE ALL NODES IN THE GRAPH
        self.nodes = all_nodes

        # CHECK CONNECTIONS
        for node_id, node in self.nodes.items():
            self.adjacency[node_id] = {}

            # Calculate the safety score for this location (Node) using Computer Vision
            # 0.0 = Safe, 1.0 = Highly Hazardous
            node_hazard_score = self.get_node_safety_score(node)

            for connection in node.connections:
                neighbor_id = connection['neighbor']

                if neighbor_id in self.nodes:
                    base_distance = connection['distance']
                    
                    # --- AI SAFETY INTEGRATION ---
                    # We modify the 'weight' used for pathfinding based on the hazard score.
                    # Formula: Effective Distance = Real Distance * (1 + (Hazard Score * Penalty))
                    
                    # Example: If hazard is 1.0 (100%), and penalty is 5.0, 
                    # the road will "look" 6 times longer to the pathfinding algorithm.
                    penalty_factor = 5.0 
                    adjusted_weight = base_distance * (1 + (node_hazard_score * penalty_factor))

                    self.adjacency[node_id][neighbor_id] = {
                        'distance': base_distance,
                        'direction': connection['direction'],
                        'safety_score': node_hazard_score,   # Store score for UI display
                        'weight': adjusted_weight            # Use this for Dijkstra/A*
                    }
        return self