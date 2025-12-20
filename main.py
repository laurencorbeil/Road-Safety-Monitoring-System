from create_nodes import open_images
from create_nodes import parse_metadata
from create_graph import create_graph
import cv2

def main():
    images = open_images
    nodes = parse_metadata(images)
    graph = create_graph()
    graph.build_graph(nodes)