# This file is used to turn the project metadata into usable nodes for graphing.
# Each node contains the fields that are common across all data points in image_metadata.
# These nodes can later be turned into graphs for future use.

# The source of information within this project is contained in the image_metadata.json file.

import json

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

def parse_metadata():
    #OPEN FILE (NEEDS TO KNOW THAT WE ARE USING UTF-8 ENCODING)
    with open('image_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    #LIST OF NODES
    nodes = {}

    for node_id, node_data in data.items():
        #CREATE NODES
        node = create_nodes(node_id, node_data['Coordinate'])

        #IMAGES AND IMAGE METADATA
        for i in range(1, 7):
            image_name = f"Image {i}"

            if image_name in node_data:
                image_data = node_data[image_name]
                node.add_image({
                    'image': i,
                    'year': image_data.get('Timestamp'),
                    'severity': image_data.get('Severity'),
                    'issue': image_data.get('Issue')
                })
            
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


#
#   THIS PART IS FOR TESTING THE CREATION OF NODES AND SEEING HOW THE DATA IS STORED IN THE NODE
#
 
# if __name__ == "__main__":
#     nodes = parse_metadata()
        
#     # CHOOSE HOW MANY NODES TO SHOW
#     num_nodes_to_show = 5
    
#     # SHOW METADATA
#     for i, (node_id, node) in enumerate(nodes.items()):
#         if i >= num_nodes_to_show:
#             break
#         print(f"NODE: {node_id}")
#         print(f"Coordinate: {node.coordinate}")
        
#         # CONECTIONS
#         print(f"\nCONNECTIONS ({len(node.connections)}):")
#         for conn in node.connections:
#             print(f"{conn['neighbor']} ({conn['distance']}m, {conn['direction']})")
        
#         # IMAGE METADATA
#         print(f"\nIMAGE METADATA ({len(node.images)} images):")
        
#         for img in node.images:
#             print(f"\nImage {img['image']}:")
#             print(f"  Year: {img['year']}")
#             print(f"  Severity: {img['severity']}")
#             print(f"  Issue: {img['issue']}")