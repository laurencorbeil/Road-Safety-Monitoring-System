import json
import os
import shutil
from sklearn.model_selection import train_test_split

# CONFIGURATION
# Adjust these paths to match your actual folder structure
SOURCE_IMAGES_DIR = "images"  # Where your h_pics, l_pics folders are
OUTPUT_DIR = "dataset_cls"    # Where we will put files for training

def setup_directories():
    for split in ['train', 'val', 'test']:
        for label in ['safe', 'hazardous']:
            os.makedirs(os.path.join(OUTPUT_DIR, split, label), exist_ok=True)

def get_image_path(filename_prefix, node_id, image_idx):
    # Helper to reconstruct your file paths (e.g., images/h_pics/h1_1.png)
    # You might need to adjust logic based on who owns which node (h, l, c, s)
    # This is a simplified mapper:
    prefix = ""
    if 'h' in node_id: prefix = "h_pics"
    elif 'l' in node_id: prefix = "l_pics"
    elif 'c' in node_id: prefix = "c_pics"
    elif 's' in node_id: prefix = "s_pics"
    
    filename = f"{node_id}_{image_idx}.png"
    return os.path.join(SOURCE_IMAGES_DIR, prefix, filename)

def main():
    setup_directories()
    
    with open('image_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    all_samples = []

    # 1. Parse JSON to get list of (image_path, label)
    for node_id, node_data in data.items():
        for i in range(1, 7):
            key = f"Image {i}"
            if key in node_data:
                severity = node_data[key].get('Severity')
                
                # CLASSIFICATION LOGIC:
                # Severity 0 = Safe, Severity > 0 = Hazardous
                label = 'safe' if severity == 0 else 'hazardous'
                
                # Construct source path
                src_path = get_image_path(None, node_id, i)
                
                # Only add if file actually exists
                if os.path.exists(src_path):
                    all_samples.append((src_path, label))
                else:
                    # print(f"Warning: Image not found {src_path}")
                    pass

    # 2. Split Data (70% Train, 15% Val, 15% Test)
    train_data, test_val_data = train_test_split(all_samples, test_size=0.3, random_state=42)
    val_data, test_data = train_test_split(test_val_data, test_size=0.5, random_state=42)

    # 3. Copy files to destination
    def copy_files(dataset, split_name):
        print(f"Preparing {split_name} set with {len(dataset)} images...")
        for src, label in dataset:
            filename = os.path.basename(src)
            dst = os.path.join(OUTPUT_DIR, split_name, label, filename)
            shutil.copy(src, dst)

    copy_files(train_data, 'train')
    copy_files(val_data, 'val')
    copy_files(test_data, 'test')
    
    print("\nDataset preparation complete! Ready for training.")

if __name__ == "__main__":
    main()