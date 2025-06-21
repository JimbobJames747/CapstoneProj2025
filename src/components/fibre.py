from component import Component

class Fibre(Component):
    can_input = True
    can_output = True

    def __init__(self, x=0, y=0, fibre_length=0.0, attenuation=0.0, name="Fibre"):
        super().__init__(name=name, x=x, y=y)
        self.fibre_length = fibre_length  # in kilometers
        self.attenuation = attenuation  # in dB/km

    def __str__(self):
        return (
            f"{self.name} with length: {self.fibre_length:.2f} km, "
            f"attenuation: {self.attenuation:.2f} dB/km, "
            f"x: {self.x:.3f}, "
            f"y: {self.y:.3f}, "
            f"inputs: {', '.join(input.name for input in self.inputs)}, "
            f"outputs: {', '.join(output.name for output in self.outputs)}"
        )
    


    

