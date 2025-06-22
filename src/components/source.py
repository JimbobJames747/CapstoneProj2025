from component import *
from fibre import Fibre
from detector import Detector
from network import Network

class Source(Component):
    can_input = False
    can_output = True

    def __init__(self, repetition_rate = 0, x = 0, y = 0, name="Source", network=None):
        super().__init__(name=name, x=x, y=y, network=network, link=False)
        self.repetition_rate = repetition_rate  # in Hz

    def __str__(self):
        return (
            f"{self.name} with RR: {self.repetition_rate} Hz, "
            f"x: {self.x:.3f}, "
            f"y: {self.y:.3f}, "
            f"inputs: {', '.join(input.name for input in self.inputs)}, "
            f"outputs: {', '.join(output.name for output in self.outputs)}"
        )






network = Network(name="Test Network")

detector_1 = Detector(name="Detector_1", x=30, y=50, det_efficiency=0.9, p_dark_count=0.01, network=network)
source = Source(repetition_rate=1000, x=10, y=20, name="Test Source", network=network)
detector_2 = Detector(name="Detector_2", x=30, y=40, det_efficiency=0.9, p_dark_count=0.01, network=network)

fibre = Fibre(fibre_length=10.0, attenuation=0.2, name="Fibre_1", network=network, start=source, end=detector_1)
fibre = Fibre(fibre_length=10.0, attenuation=0.2, name="Fibre_2", network=network, start=source, end=detector_2)



print(network.components)
print(network.links)
print(fibre.connections)


import networkx as nx
import matplotlib.pyplot as plt

def draw_network(network):
    G = nx.DiGraph()

    # Add nodes
    for component in network.components:
        G.add_node(component.name)

    # Add edges based on links
    for link in network.links:
        G.add_edge(link.start.name, link.end.name)

    # Draw
    nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, arrowsize=20)
    plt.show()

draw_network(network)




