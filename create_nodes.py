# This file is used to turn the project metadata into usable nodes for graphing.
# Each node contains the fields that are common across all data points in image_metadata.
# These nodes can later be turned into graphs for future use.
# The source of information within this project is contained in the image_metadata.json file.

import json
import cv2
import os

directory = os.path.dirname(__file__)

class create_nodes:
    def __init__(self, node_id, coordinate):
        self.id = node_id
        self.coordinate = coordinate
        self.connections = []
        self.images = []

    def add_connection(self, neighbour_id, distance, direction):
        self.connections.append({
            'neighbor': neighbour_id,
            'distance': distance,
            'direction': direction
        })

    def add_image(self, image_data):
        self.images.append(image_data)

# Makes an array of all the images in order of the json node data.
def open_images():
    images = []

    def load_img(*parts):
        path = os.path.join(directory, *parts)
        return cv2.imread(path) if os.path.isfile(path) else None

    for i in range(1, 25):
        for j in range(1, 7):
            img = load_img('images', 'h_pics', f'h{i}_{j}.png')
            images.append(img)

    for i in range(1, 25):
        for j in range(1, 7):
            img = load_img('images', 'l_pics', f'l{i}_{j}.png')
            images.append(img)

    for i in range(1, 22):
        for j in range(1, 7):
            img = load_img('images', 'c_pics', f'c{i}_{j}.png')
            images.append(img)

    for i in range(1, 26):
        for j in range(1, 7):
            img = load_img('images', 's_pics', f's{i}_{j}.png')
            images.append(img)

    return images

def parse_metadata(images):
    # OPEN file relative to module directory
    json_path = os.path.join(directory, 'image_metadata.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    #LIST OF NODES
    nodes = {}
    image_index = 0

    for node_id, node_data in data.items():
        #CREATE NODES
        node = create_nodes(node_id, node_data.get('Coordinate'))

        #IMAGES AND IMAGE METADATA
        for i in range(1, 7):
            image_name = f"Image {i}"

            if image_name in node_data:
                image_data = node_data[image_name]
                if image_index < len(images):
                    node.add_image({
                        'image': i,
                        'year': image_data.get('Timestamp'),
                        'severity': image_data.get('Severity'),
                        'issue': image_data.get('Issue'),
                        'picture': images[image_index]
                    })
                    image_index += 1
       
        #CONNECTIONS
        if 'Connections' in node_data and 'Distances' in node_data:
            for i, neighbor in enumerate(node_data['Connections']):
                if i < len(node_data['Distances']):
                    distance = node_data['Distances'][i]
                    direction = (
                        node_data.get('Directions', [None])[i] 
                        if i < len(node_data.get('Directions', [])) 
                        else None
                    )
                    node.add_connection(neighbor, distance, direction)
        nodes[node_id] = node

    return nodes


# Test to show that images are properly stored in each node. Can be deleted when no longer needed.
if __name__ == "__main__":

    images = open_images()
    nodes = parse_metadata(images)

    for node_id, node in nodes.items():
        for img_data in node.images:
            img = img_data['picture']
            window_name = f"Node {node_id} - Image {img_data['image']}"
            if img is None:
                print(f"Skipped missing image: {window_name}")
                continue
            cv2.imshow(window_name, img)
            cv2.waitKey(0)
            cv2.destroyWindow(window_name)
    cv2.destroyAllWindows()