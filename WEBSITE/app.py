import sys
import os
import math
import time

# get filepath relative to the project so that it will run on any system
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
rsms_dir = os.path.join(base_dir, 'Road-Safety-Monitoring-System')
path_to_insert = rsms_dir if os.path.isdir(rsms_dir) else base_dir
sys.path.insert(0, path_to_insert)

from flask import Flask, render_template, request, jsonify
from create_nodes import open_images, parse_metadata
from create_graph import create_graph
from coordinate_conversion import dms_to_decimal
from dijkstra_search import Dijkstra
from a_star_search import A_star

app = Flask(__name__)

# load nodes and graph once on startup
images = open_images()
nodes = parse_metadata(images)
for n in nodes.values():
    n.coordinate = dms_to_decimal(n.coordinate)
graph = create_graph()
graph.build_graph(nodes)

def distance(a, b):
    R = 6371000.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat, dlon = lat2 - lat1, lon2 - lon1
    sa = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(sa))

def nearest_node(coord):
    try:
        return min(nodes.values(), key=lambda n: distance(coord, n.coordinate))
    except ValueError:
        return None

def resolve_node(value):
    if isinstance(value, (list, tuple)):
        return nearest_node(value)
    return nodes.get(value)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/route", methods=["POST"])
def route():
    data = request.json or {}
    start = data.get("start")
    end = data.get("end")
    algo = data.get("algo", "astar")

    try:
        start_node = resolve_node(start)
        end_node = resolve_node(end)

        if start_node is None or end_node is None:
            return jsonify({"error": "Invalid start or end"}), 400

        start_time = time.time()

        if algo == "dijkstra":
            node_path, total_dist = Dijkstra(graph, start_node_id=start_node.id, end_node_id=end_node.id)
        else:
            node_path, total_dist = A_star(graph, start_node.id, end_node.id)

        end_time = time.time()

        path_coords = [nodes[nid].coordinate for nid in node_path]

        if not math.isfinite(total_dist):
            distance_m = None
            unreachable = True
        else:
            distance_m = total_dist
            unreachable = False

        return jsonify({
            "path": path_coords,
            "node_path": node_path,
            "distance_m": distance_m,
            "time_s": end_time - start_time,
            "unreachable": unreachable
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)