from create_nodes import parse_metadata
from create_graph import create_graph

def main():
    nodes = parse_metadata()
    graph = create_graph()
    graph.build_graph(nodes)