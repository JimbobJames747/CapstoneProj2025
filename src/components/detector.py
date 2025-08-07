from components.component import Component
import math

class Detector(Component):
    can_input = True
    can_output = True

    def __init__(self, name="Detector", x = 0, y = 0, 
                 det_efficiency = 0, p_dark_count = 0,
                 network=None, trusted_node=True):
        super().__init__(name=name, network=network, link=False)
        self.det_efficiency = det_efficiency
        self.p_dark_count = p_dark_count
        self.coincidence_window = 1.3e-10  # 130 ps
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
        #detected_photons = [math.floor(photons)]

        print(f"{self.name} detected {detected_photons[0]} photons, {detected_photons[1]} were entangled!")

        # prob of photon reaching detector is down to atenuation = Transmission coefficient, lets say 100 photons were
        # sent and 50 reached detector. If the distribution of photons lost from time bins (actually 2xtime bin time) is uniform then
        # overlap of photons must be 0.5x0.5=0.25 so 25 coincidences?