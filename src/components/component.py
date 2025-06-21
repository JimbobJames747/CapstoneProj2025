
# base class for all components
# params are x and y coords in drawing area.
class Component():
    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.name = name
        self.outputs = []
        self.inputs = []


    def connectInput(self, component):
        if self.can_input:
            if component in self.inputs:
                raise ValueError(f"Component {self.name} already has input from {component.name}.")
            else:
                self.inputs.append(component)
                component.outputs.append(self)
        else:
            raise ValueError(f"Component {self.name} cannot take an input.")
        
        
    def connectOutput(self, component):
        if self.can_output:
            if component in self.outputs:
                raise ValueError(f"Component {self.name} already connected as output to {component.name}.")
            self.outputs.append(component)
            component.inputs.append(self)
        else:
            raise ValueError(f"Component {self.name} cannot output to another component.")
