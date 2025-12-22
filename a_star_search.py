#This file is the implementation of the A* algorithm to find the best/shortest path

import heapq
import math
from typing import Tuple, List

def A_star(graph, start: str, goal: str) -> Tuple[List[str], float]:
    #Run A* on the graph from the start node to the goal node
    #Returns (path_list, total_cost)
    #If the goal is unreachable, returns ([goal], float('inf'))

    #Euclidean distance heuristic between two nodes
    #returns 0.0 on error
    def euclidean_distance_heuristic(a, b):
        try:
            a_x, a_y = graph.nodes[a].coordinate
            b_x, b_y = graph.nodes[b].coordinate
            return math.hypot(a_x - b_x, a_y - b_y)
        except Exception:
            return 0.0

    open_heap = [(euclidean_distance_heuristic(start, goal), start)]
    predecessor = {}    #maps node_id to parent node_id for path reconstruction step
    best_cost = {node_id: float('inf') for node_id in graph.nodes}
    best_cost[start] = 0.0

    #expands nodes
    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current == goal:
            # Exit when goal is popped
            break

        # Check each neighbor of current node
        for neighbor, edge in graph.adjacency.get(current, {}).items():
            weight = edge.get('weight', edge.get('distance', 1))
            temp = best_cost[current] + weight

            #if the path is better, push to heap
            if temp < best_cost.get(neighbor, float('inf')):
                predecessor[neighbor] = current
                best_cost[neighbor] = temp
                heapq.heappush(open_heap, (temp + euclidean_distance_heuristic(neighbor, goal), neighbor))

    #Reconstruct the path
    path = []
    current_node = goal

    if best_cost.get(goal, float('inf')) == float('inf'):
        return [goal], float('inf')
    
    while current_node is not None:
        path.append(current_node)
        current_node = predecessor.get(current_node)

    #swap from GOAL to START to START to GOAL
    path.reverse()
    return path, best_cost[goal]