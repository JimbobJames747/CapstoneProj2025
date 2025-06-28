from component import Component
from network import Network

class Fibre():
    can_input = True
    can_output = True

    def __init__(self, network: Network, start: Component, end: Component, fibre_length=0.0, attenuation=0.0, name="Fibre"):
        self.fibre_length = fibre_length  # in kilometers
        self.attenuation = attenuation  # in dB/km
        self.name = name
        self.network = network
        self.start = start
        self.end = end
        self.connection_in = start
        self.connection_out = end
        start.connectOutput(self)
        end.connectInput(self)
        network.add_link(self)

    def __str__(self):
        return (
            f"{self.name} with length: {self.fibre_length:.2f} km, "
            f"attenuation: {self.attenuation:.2f} dB/km, "
            f"start: ({self.start.name}), "
            f"end: ({self.end.name})"
        )
    
    def process_photons(self, photons):
        photons = [photons * (10 ** (-self.attenuation * self.fibre_length)) for photons in photons]
        self.connection_out.process_photons(photons)
        
         
    


    

