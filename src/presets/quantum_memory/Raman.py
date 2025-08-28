from QuantumMemory import QuantumMemory

class Raman(QuantumMemory):
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, verbose: bool = False):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)
        self.set_memory_param("scheme", "Off-resonant Raman")
        self.set_memory_param("heralded", False)