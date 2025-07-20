from component import *
from fibre import Fibre
from detector import Detector
from source import Source
from network import Network


network = Network(name="Test Network")

detector_1 = Detector(name="Detector_1", x=30, y=50, det_efficiency=0.9, p_dark_count=0.01, network=network)
detector_2 = Detector(name="Detector_2", x=30, y=40, det_efficiency=0.9, p_dark_count=0.01, network=network)
detector_3 = Detector(name="Detector_3", x=30, y=30, det_efficiency=0.9, p_dark_count=0.01, network=network)

source = Source(repetition_rate=1E6, x=10, y=20, name="Test Source", network=network, p_entangled=0.7, p_noisy=0.1)


fibre_1 = Fibre(fibre_length=10.0, attenuation=0.02, name="Fibre_1", network=network, start=source, end=detector_1)
fibre_2 = Fibre(fibre_length=10.0, attenuation=0.02, name="Fibre_2", network=network, start=source, end=detector_2)
fibre_3 = Fibre(fibre_length=10.0, attenuation=0.02, name="Fibre_3", network=network, start=source, end=detector_3)

network.simulate(time=100.0)



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