
class Network:
    def __init__(self, name: str):
        self.components = []
        self.links = []
        self.name = name

    def __str__(self):
        return f"Network: {self.name}"
    
    def add_component(self, component):
        if component not in self.components:
            self.components.append(component)
            component.network = self
        else:
            raise ValueError(f"Component {component.name} is already in the network {self.name}.")
        
    def remove_component(self, component):
        if component in self.components:
            self.components.remove(component)
            component.network = None
        else:
            raise ValueError(f"Component {component.name} is not in the network {self.name}.")
        
    def add_link(self, link):
        if link not in self.links:
            self.links.append(link)
            link.network = self
        else:
            raise ValueError(f"Link {link} is already in the network {self.name}.")
        
    def remove_link(self, link):
        if link in self.links:
            self.links.remove(link)
            link.network = None
        else:
            raise ValueError(f"Link {link} is not in the network {self.name}.")