from component import Component
import math

class Detector(Component):
    can_input = True
    can_output = True

    def __init__(self, name="Detector", x = 0, y = 0, 
                 det_efficiency = 0, p_dark_count = 0,
                 network=None):
        super().__init__(name=name, x=x, y=y, network=network, link=False)
        self.det_efficiency = det_efficiency
        self.p_dark_count = p_dark_count
        network.add_detector(self)

    def __str__(self):
        return str(
                "{}: {}, ".format(self.name, self.det_efficiency) +
                f"dark count probability: {self.p_dark_count:.3f}" +
                f"x: {self.x:.3f}, "+
                f"y: {self.y:.3f}, "+
                f"inputs: {', '.join(input.name for input in self.inputs)}, "
                f"outputs: {', '.join(output.name for output in self.outputs)}"
            )
    
    def process_photons(self, photons):
        detected_photons = [math.floor(photons * self.det_efficiency) for photons in photons]

        print(f"{self.name} detected {detected_photons[0]} photons, {detected_photons[1]} were entangled!")