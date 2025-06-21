from component import Component
from fibre import Fibre
from detector import Detector

class Source(Component):
    can_input = False
    can_output = True

    def __init__(self, repetition_rate = 0, x = 0, y = 0, name="Source"):
        super().__init__(name=name, x=x, y=y)
        self.repetition_rate = repetition_rate  # in Hz

    def __str__(self):
        return (
            f"{self.name} with RR: {self.repetition_rate} Hz, "
            f"x: {self.x:.3f}, "
            f"y: {self.y:.3f}, "
            f"inputs: {', '.join(input.name for input in self.inputs)}, "
            f"outputs: {', '.join(output.name for output in self.outputs)}"
        )


source = Source(repetition_rate=1000, x=10, y=20, name="Test Source")
fibre = Fibre(x=5, y=15, fibre_length=10.0, attenuation=0.2, name="Test Fibre")
detector = Detector(name="Test Detector", x=30, y=40, det_efficiency=0.9, p_dark_count=0.01)

source.connectOutput(fibre)
fibre.connectOutput(detector)




print(source)
print(fibre)
print(detector)

