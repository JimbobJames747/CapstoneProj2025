import sys
from components import network as nw
from components.component import Component
from components.fibre import Fibre
from components.detector import Detector 
from components.source import Source
from presets.single_link import SingleLink
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

# this file is the brain of the program, it connects all the backend logic to the GUI and calls backend classes like components and networks

class SlotHandler:
    def __init__(self, window):
        self.window = window
        self.network_file_open = False
        self.network = None

    #To do: make it for general label
    # def change_label(self, text):
    #     self.ui.label.setText(text)

    ### MENU BAR BTNS ###

    def exit_app(self):
        sys.exit(0)

    ### TOOLBAR BTNS ###   

    def new_button_clicked(self):
        if self.network_file_open:
            print("Network file is already open. Please close it before creating a new one.")
        else:
            print("New button clicked")
            self.network = nw.Network(name="Untitled Network")
            self.network_file_open = True
            self.tree_network = QTreeWidgetItem()
            self.tree_network.setText(0, "Untitled Network")
            self.window.componentTree.addTopLevelItem(self.tree_network)

    def run_button_clicked(self):
        print("Run button clicked")
        print(self.network)

    def stop_button_clicked(self):
        print("Stop button clicked")

    def save_button_clicked(self, text):
        print(text)

    ### COMPONENTS BTNS ###

    def add_source_button_clicked(self):
        print("Add Source button clicked")
        if self.network is not None:
            Source(network=self.network, name="Source {}".format(len(self.network.sources)))
            self.tree_source = QTreeWidgetItem()
            self.tree_source.setText(0, "Source {}".format(len(self.network.sources)))
            self.tree_network.addChild(self.tree_source)
            self.tree_network.setExpanded(True)
        else:
            print("No network is open. Please create or open a network first.")

    def add_detector_button_clicked(self):
        print("Add Detector button clicked")
        if self.network is not None:
            Detector(network=self.network, name="Detector {}".format(len(self.network.detectors)))
            self.tree_detector = QTreeWidgetItem()
            self.tree_detector.setText(0, "Detector {}".format(len(self.network.detectors)))
            self.tree_network.addChild(self.tree_detector)
            self.tree_network.setExpanded(True)
        else:
            print("No network is open. Please create or open a network first.")

    def add_fibre_button_clicked(self):
        print("Add Fibre button clicked")

    # presets

    def add_single_link_button_clicked(self):
        print("Add Single Link button clicked")
        if self.network is not None:
            print("Can't add a single link to a network. Close current network and click add single link again.")
        else:
            SingleLink(l=1, mu=1, alpha=1, det_1_eff=1, det_2_eff=1, prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0, verbose=False)
            self.tree_single_link = QTreeWidgetItem()
            self.tree_single_link.setText(0, "Single Link")
            self.window.componentTree.addTopLevelItem(self.tree_single_link)
            self.tree_single_link_source = QTreeWidgetItem()
            self.tree_single_link_source.setText(0, "Source")
            self.tree_single_link.addChild(self.tree_single_link_source)
            for i in range(2):
                self.tree_single_link_detector = QTreeWidgetItem()
                self.tree_single_link_detector.setText(0, "Detector {}".format(i + 1))
                self.tree_single_link.addChild(self.tree_single_link_detector)
            self.tree_single_link.setExpanded(True)

    ### SELECTING COMPONENTS IN TREE ###

    ### TESTING BTNS ###

    def print_network_button_clicked(self):
        print(self.network)

    def show_button_clicked(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        print("Show Network button clicked")
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

        draw_network(self.network)
        