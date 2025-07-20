
# base class for all components
# params are x and y coords in drawing area.

class Component():
    def __init__(self, name, network, link=False):
        self.name = name
        self.outputs = []
        self.inputs = []
        self.network = network
        network.add_component(self)

    def connectInput(self, link):
        if self.can_input:
            if link.end in self.inputs:
                raise ValueError(f"Component {self.name} already has input from {link.end.name}.")
            elif link.end not in self.network.components :
                raise ValueError(f"Components not in the same network: {self.name} and {link.end.name}.")
            else:
                self.inputs.append(link)
                link.connection_out = (self)
        else:
            raise ValueError(f"Component {self.name} cannot take an input.")

    def connectOutput(self, link):
        if self.can_output:
            if link.start in self.outputs:
                raise ValueError(f"Component {self.name} already connected as output to {link.start.name}.")
            elif link.start not in self.network.components :
                raise ValueError(f"Components not in the same network: {self.name} and {link.start.name}.")
            else:
                self.outputs.append(link)
                link.connection_in = (self)
        else:
            raise ValueError(f"Component {self.name} cannot output to another component.")
        
    
