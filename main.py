from create_nodes import open_images
from create_nodes import parse_metadata
from create_graph import create_graph
from dijkstra_search import Dijkstra
from a_star_search import A_star
from coordinate_conversion import dms_to_decimal
import cv2

def main():
    images = open_images()
    nodes = parse_metadata(images)

    #TODO: Add input from user depennding on desired star/end locations

    # Convert all node coordinates from DMS to decimal degrees before using algorithms
    for node in nodes.values():
        node.coordinate = dms_to_decimal(node.coordinate)

    #Get first node
    startNode = nodes["h1"]
    endNode = nodes["s25"]

    #Displaying start/end info
    print("Start from: " + startNode.id)
    print("End at: " + endNode.id)
    print("Node ID:", startNode.id)
    print("Coordinate:", startNode.coordinate)
    print("Connections:", startNode.connections)
    print("Number of images:", len(startNode.images))

    #Create the connections between all nodes, so we now have a full weighted graph
    graph = create_graph()
    graph.build_graph(nodes)

    Dijkstra_path, total_distance = Dijkstra(graph, start_node_id=startNode.id, end_node_id=endNode.id)
    print("Dijkstra Path:", Dijkstra_path)
    print("Total Distance:", total_distance)

    path, total_distance = A_star(graph, startNode.id, endNode.id)
    print("A* Path:", path)
    print("Total Distance:", total_distance)

if __name__ == "__main__":
    main()