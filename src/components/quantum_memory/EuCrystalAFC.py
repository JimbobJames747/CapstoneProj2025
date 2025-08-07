from AFC import AFC
from parameters import *

# === Eu:YSO AFC Memory Class ===
class EuCrystalAFC(AFC):
    def __init__(
        self, 
        name: str, 
        in_wavelength: float, 
        in_storage_time: float, 
        in_fidelity: float, 
        long_storage: bool = False, 
        verbose: bool = False
    ):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Choose parameter set based on long_storage flag
        self.set_memory_param("fidelity", EU_AFC_MEMORY_FIDELITY)
        self.set_memory_param("efficiency", EU_AFC_MEMORY_EFFICIENCY)
        self.set_memory_param("wavelength", EU_AFC_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", EU_AFC_MEMORY_MULTIMODE_CAPACITY)

        # If long storage 
        if long_storage:
            self.set_memory_param("storage_time", EU_LONG_AFC_MEMORY_STORAGE_TIME)
            self.set_memory_param("bandwidth", EU_LONG_AFC_MEMORY_BANDWIDTH)
            self.set_memory_param("temperature", EU_LONG_AFC_MEMORY_TEMPERATURE)
            self.set_memory_param("magnetic_field", EU_LONG_AFC_MEMORY_MAGNETIC_FIELD)

        # If short storage 
        else:
            self.set_memory_param("storage_time", EU_SHORT_AFC_MEMORY_STORAGE_TIME)
            self.set_memory_param("bandwidth", EU_SHORT_AFC_MEMORY_BANDWIDTH)
            self.set_memory_param("temperature", EU_SHORT_AFC_MEMORY_TEMPERATURE)
            self.set_memory_param("magnetic_field", EU_SHORT_AFC_MEMORY_MAGNETIC_FIELD)

        # Check input validity against memory parameters
        self.check_input_validity()
