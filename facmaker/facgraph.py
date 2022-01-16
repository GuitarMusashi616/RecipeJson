import matplotlib.pyplot as plt
import networkx as nx


class FacGraph:
    def __init__(self, pos_func=nx.spectral_layout):
        self.G = nx.DiGraph()
        self.edge_labels = {}
        self.pos_func = pos_func

    def add(self, building, mult=1):
        for req, numreq in building.req.items():
            for prod, numprod in building.prod.items():
                self.G.add_edge(req, prod)
                self.edge_labels[req, prod] = round(numreq * mult) if numreq // 1 == numreq else numreq * mult

    def show(self):
        plt.rcParams["figure.figsize"] = (12, 8)
        pos = self.pos_func(self.G)
        nx.draw(self.G, pos, with_labels=True, edge_color='black', width=1, linewidth=1, node_size=500,
                node_color='pink', alpha=0.9)
        nx.draw_networkx_edge_labels(self.G, pos, self.edge_labels)
        plt.show()