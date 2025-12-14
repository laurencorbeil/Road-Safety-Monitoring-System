# This file is used to turn nodes into a graphical format

class create_graph:

    # INITIALIZE EMPTY GRAPH
    def __init__(self):
        self.nodes = {}
        self.adjacency = {}

    def build_graph(self, all_nodes):
        # STORE ALL NODES IN THE GRAPH
        self.nodes = all_nodes

        # CHECK CONNECTIONS
        for node_id, node in self.nodes.items():
            self.adjacency[node_id] = {}

            for connection in node.connections:
                neighbor_id = connection['neighbor']

                if neighbor_id in self.nodes:
                    self.adjacency[node_id][neighbor_id] = {
                        'distance': connection['distance'],
                        'direction': connection['direction'],
                    }
        return self
