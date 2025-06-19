from component import Component

class Source(Component):
    can_input = False
    can_output = True

    def __init__(self, repetition_rate = 0, x = 0, y = 0):
        super().__init__(x=x, y=y)
        self.repetition_rate = repetition_rate

    def __str__(self):
        return str("Source with RR: {} Hz, ".format(self.repetition_rate) +
                f"x: {self.x:.3f}, "+
                f"y: {self.y:.3f}, "+
                f"inputs: {self.inputs}, "+
                f"outputs: {self.outputs}")




