from component import *
from fibre import Fibre
from detector import Detector
from network import Network

class Source(Component):
    can_input = False
    can_output = True

    def __init__(self,
                 repetition_rate = 0,
                 p_entangled = 0,
                 p_noisy = 0,
                 x = 0, y = 0,
                 name="Source",
                 network=None):
        super().__init__(name=name, x=x, y=y, network=network, link=False)
        self.repetition_rate = repetition_rate  # in Hz
        self.p_entangled = p_entangled
        self.p_noisy = p_noisy
        network.add_source(self)

    def __str__(self):
        return (
            f"{self.name} with RR: {self.repetition_rate} Hz, "
            f"x: {self.x:.3f}, "
            f"y: {self.y:.3f}, "
            f"inputs: {', '.join(input.name for input in self.inputs)}, "
            f"outputs: {', '.join(output.name for output in self.outputs)}"
        )
    
    def emit(self, time, outputs: list):
        """
        Simulate the emission of photons from the source.
        This method simulates a block of time where the source emits photons
        at the specified repetition rate.
        """

        # may change this to more outputs (for now only considering two entangled photons)
        if len(outputs) > 2:
            raise ValueError("Can only emit to two output fibres at once")

        print(f"{self.name} emitting photons at a rate of {self.repetition_rate} Hz for {time} seconds")

        # number of photons emitted on each link 
        n_photons = self.repetition_rate * time
        # number of entangled pairs emitted
        n_entangled = n_photons * self.p_entangled

        photons = [n_photons, n_entangled]

        for output in outputs:
            output.process_photons(photons)

