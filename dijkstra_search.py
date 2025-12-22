import heapq

def Dijkstra(graph, start_node_id, end_node_id):
    
    print("Running Dijkstra's Algorithm...")

    queue = []
    heapq.heappush(queue, (0, start_node_id))

    distances = {node_id: float('inf') for node_id in graph.nodes}
    distances[start_node_id] = 0

    previous_nodes = {node_id: None for node_id in graph.nodes}

    while queue:
        current_distance, current_node_id = heapq.heappop(queue)

        # Early exit
        if current_node_id == end_node_id:
            break

        if current_distance > distances[current_node_id]:
            continue

        for neighbor_id, edge_data in graph.adjacency.get(current_node_id, {}).items():
            weight = edge_data['weight']
            distance = current_distance + weight

            print(
                f"{current_node_id} → {neighbor_id} | "
                f"base={edge_data.get('distance', '?')} "
                f"safety={edge_data.get('safety_score', 0.0):.2f} "
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