from create_nodes import open_images
from create_nodes import parse_metadata
from create_graph import create_graph
from dijkstra_search import Dijkstra
from a_star_search import A_star
from coordinate_conversion import dms_to_decimal
import cv2
import math, time, argparse


def distance(a, b):
    R = 6371000.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    sa = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(sa))


def find_nearest_node(coord, nodes):
    best = None
    best_d = float('inf')
    for n in nodes.values():
        d = distance(coord, n.coordinate)
        if d < best_d:
            best_d = d
            best = n
    return best


def build_graph_and_nodes():
    images = open_images()
    nodes = parse_metadata(images)
    for node in nodes.values():
        node.coordinate = dms_to_decimal(node.coordinate)
    graph = create_graph()
    graph.build_graph(nodes)
    return graph, nodes


def parse_coord_or_id(value):
    if isinstance(value, str) and ',' in value:
        try:
            lat, lon = value.split(',')
            return (float(lat.strip()), float(lon.strip()))
        except Exception:
            return value
    return value

def main():
    parser = argparse.ArgumentParser(description="Run pathfinding between two nodes or coords")
    parser.add_argument('--start', '-s', help="Start node id or 'lat,lon'", default='h1')
    parser.add_argument('--end', '-e', help="End node id or 'lat,lon'", default='s25')
    parser.add_argument('--algo', choices=['astar', 'dijkstra'], default='astar')
    args = parser.parse_args()

    graph, nodes = build_graph_and_nodes()

    start_val = parse_coord_or_id(args.start)
    end_val = parse_coord_or_id(args.end)

    if isinstance(start_val, (list, tuple)):
        start_node = find_nearest_node(start_val, nodes)
    else:
        start_node = nodes.get(start_val)

    if isinstance(end_val, (list, tuple)):
        end_node = find_nearest_node(end_val, nodes)
    else:
        end_node = nodes.get(end_val)

    if start_node is None or end_node is None:
        print('Invalid start or end; check node IDs or coordinate format lat,lon')
        return

    print(f"Start: {start_node.id} @ {start_node.coordinate}")
    print(f"End:   {end_node.id} @ {end_node.coordinate}")

    t0 = time.time()
    if args.algo == 'dijkstra':
        node_path, total_distance = Dijkstra(graph, start_node_id=start_node.id, end_node_id=end_node.id)
    else:
        node_path, total_distance = A_star(graph, start_node.id, end_node.id)
    t1 = time.time()

    print('Path:', node_path)
    print(f'Total distance: {total_distance:.2f} (units as in metadata)')
    print(f'Time: {t1 - t0:.6f}s')

if __name__ == "__main__":
    main()