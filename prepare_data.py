import json
import os
import shutil
from sklearn.model_selection import train_test_split

# --- CONFIGURATION ---
# The folder where our subfolders (h_pics, l_pics, etc.) are located.
# Change this if our images are in a different spot!
SOURCE_IMAGES_DIR = "images"  
OUTPUT_DIR = "dataset_cls"

def setup_directories():
    """
    Creates the folder structure required by YOLOv8 for classification.
    Structure:
       dataset_cls/
          train/
             safe/
             hazardous/
          val/
             ...
          test/
             ...
    """
    # If the output directory already exists, delete it to start fresh
    if os.path.exists(OUTPUT_DIR):
        print(f"Cleaning up old {OUTPUT_DIR}...")
        shutil.rmtree(OUTPUT_DIR)
    
    # Create the standard Train/Val/Test splits
    for split in ['train', 'val', 'test']:
        for label in ['safe', 'hazardous']:
            os.makedirs(os.path.join(OUTPUT_DIR, split, label), exist_ok=True)

def get_image_path(node_id, image_idx):
    """
    Reconstructs the file path for an image based on its Node ID.
    
    Args:
        node_id (str): The ID from the JSON (e.g., 'h1', 'l5', 'c3').
        image_idx (int): The image number (1-6).
        
    Returns:
        str: The full relative path to the image file (e.g., 'images/h_pics/h1_1.png').
    """
    # Determine the subfolder based on the first letter of the node ID
    prefix = ""
    if node_id.startswith('h'): prefix = "h_pics"
    elif node_id.startswith('l'): prefix = "l_pics"
    elif node_id.startswith('c'): prefix = "c_pics"
    elif node_id.startswith('s'): prefix = "s_pics"
    
    # Construct the filename matching our project convention
    filename = f"{node_id}_{image_idx}.png"
    return os.path.join(SOURCE_IMAGES_DIR, prefix, filename)

def main():
    """
    Main execution flow:
    1. Validates that the source image directory exists.
    2. Reads the metadata JSON.
    3. Scans for images and assigns labels (Safe vs Hazardous).
    4. Splits the found images into Train (70%), Validation (15%), and Test (15%).
    5. Copies the files into the final dataset structure.
    """
    # Debug: Print where Python is looking for files
    print(f"Current Working Directory: {os.getcwd()}")
    
    # Safety Check: Stop if the images folder isn't found
    if not os.path.exists(SOURCE_IMAGES_DIR):
        print(f"CRITICAL ERROR: The folder '{SOURCE_IMAGES_DIR}' was not found.")
        print("Please ensure you are running this script from the project root.")
        return

    setup_directories()
    
    # Load our metadata file
    with open('image_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_samples = []
    missing_count = 0

    print("Scanning for images...")

    # Iterate through every node in the JSON
    for node_id, node_data in data.items():
        # Check all 6 possible images for this node
        for i in range(1, 7):
            key = f"Image {i}"
            if key in node_data:
                severity = node_data[key].get('Severity')
                
                # Skip entries where data is null/missing
                if severity is None:
                    continue

                # --- CLASSIFICATION LOGIC ---
                # This is where we decide what counts as "Hazardous".
                # Current Rule: Severity 0 is Safe. Anything else (1, 2, 3) is Hazardous.
                label = 'safe' if severity == 0 else 'hazardous'
                
                # Get the path to where the image *should* be
                src_path = get_image_path(node_id, i)
                
                # Verify the file actually exists before adding it to our list
                if not os.path.exists(src_path):
                    missing_count += 1
                    # Debug print for the first missing file to help troubleshooting
                    if missing_count == 1:
                        print(f"\n[DEBUG] Failed to find file at: {os.path.abspath(src_path)}")
                else:
                    all_samples.append((src_path, label))

    print(f"\nScan Complete. Found: {len(all_samples)} images. Missing: {missing_count}.")

    if len(all_samples) == 0:
        print("ERROR: No images found. Cannot proceed.")
        return

    # Split the list of found images into 3 groups
    # random_state=42 ensures the split is the same every time we run this
    train_data, test_val_data = train_test_split(all_samples, test_size=0.3, random_state=42)
    val_data, test_data = train_test_split(test_val_data, test_size=0.5, random_state=42)

    # Helper function to perform the actual file copying
    def copy_files(dataset, split_name):
        print(f"Copying {len(dataset)} images to {split_name}...")
        for src, label in dataset:
            filename = os.path.basename(src)
            # Destination: dataset_cls/train/hazardous/h1_1.png
            dst = os.path.join(OUTPUT_DIR, split_name, label, filename)
            shutil.copy(src, dst)

    # execute copies
    copy_files(train_data, 'train')
    copy_files(val_data, 'val')
    copy_files(test_data, 'test')
    
    print("\nDataset preparation complete! You can now run train_model.py.")

if __name__ == "__main__":
    main()