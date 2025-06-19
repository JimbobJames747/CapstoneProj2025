
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
        self.inputs.append(component)

    def connectOutput(self, component):
        self.outputs.append(component)
