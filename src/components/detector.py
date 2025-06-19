from component import Component

class Detector(Component):
    can_input = True
    can_output = False

    def __init__(self, name=None, x = 0, y = 0, 
                 det_efficiency = 0, p_dark_count = 0):
        super().__init__(name=name, x=x, y=y)
        self.det_efficiency = det_efficiency
        self.p_dark_count = p_dark_count

    def __str__(self):
        return str("Detector with Efficiency: {}, ".format(self.det_efficiency) +
                f"dark count probability: {self.p_dark_count:.3f}" +
                f"x: {self.x:.3f}, "+
                f"y: {self.y:.3f}, "+
                f"inputs: {self.inputs}, "+
                f"outputs: {self.outputs}, ")