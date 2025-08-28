from AFC import AFC
from parameters import *

# === Er:YSO Crystal AFC Memory Class ===
class ErCrystalAFC(AFC):
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, verbose: bool = False):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Set internal memory parameters using the global constants
        self.set_memory_param("fidelity", ER_AFC_MEMORY_FIDELITY)
        self.set_memory_param("efficiency", ER_AFC_MEMORY_EFFICIENCY)
        self.set_memory_param("storage_time", ER_AFC_MEMORY_STORAGE_TIME)
        self.set_memory_param("bandwidth", ER_AFC_MEMORY_BANDWIDTH)
        self.set_memory_param("temperature", ER_AFC_MEMORY_TEMPERATURE)
        self.set_memory_param("magnetic_field", ER_AFC_MEMORY_MAGNETIC_FIELD)
        self.set_memory_param("wavelength", ER_AFC_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", ER_AFC_MEMORY_MULTIMODE_CAPACITY)

        # Check input validity against memory parameters
        self.check_input_validity()


