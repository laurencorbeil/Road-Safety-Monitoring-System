from create_nodes import open_images
from create_nodes import parse_metadata
from create_graph import create_graph
import cv2

def main():
    images = open_images()
    nodes = parse_metadata(images)

    #TODO: Add input from user depennding on desired star/end locations

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

def Dijkstra(graph, start_node_id, end_node_id):
    import heapq

    print("Running Dijkstra's Algorithm...")

    queue = []
    heapq.heappush(queue, (0, start_node_id))

    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_node_id] = 0

    previous_nodes = {node_id: None for node_id in graph.nodes}

    while queue:
        current_distance, current_node_id = heapq.heappop(queue)

        # Early exit (since you DO know the end node)
        if current_node_id == end_node_id:
            break

        if current_distance > distances[current_node_id]:
            continue

        for neighbor_id, edge_data in graph.adjacency[current_node_id].items():
            weight = edge_data['weight'] 
            distance = current_distance + weight

            print(
                f"{current_node_id} → {neighbor_id} | "
                f"base={edge_data['distance']} "
                f"safety={edge_data['safety_score']:.2f} "
                f"weight={edge_data['weight']:.2f} "
                f"total_dist={distance:.2f}"
                )

            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                previous_nodes[neighbor_id] = current_node_id
                heapq.heappush(queue, (distance, neighbor_id))

    # Reconstruct path
    path = []
    current_node_id = end_node_id
    while current_node_id is not None:
        path.append(current_node_id)
        current_node_id = previous_nodes[current_node_id]
    path.reverse()

    return path, distances[end_node_id]


if __name__ == "__main__":
    main()

    