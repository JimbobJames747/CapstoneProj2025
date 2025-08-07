from DLCZ import DLCZ
from parameters import *

# === Cavity-Enhanced Rb DLCZ Memory Class ===
class RbDLCZ(DLCZ):
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, verbose: bool = False):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Set internal memory parameters using the global constants
        self.set_memory_param("fidelity", Rb_DLCZ_MEMORY_FIDELITY)
        self.set_memory_param("efficiency", Rb_DLCZ_MEMORY_EFFICIENCY)
        self.set_memory_param("storage_time", Rb_DLCZ_MEMORY_STORAGE_TIME)
        self.set_memory_param("bandwidth", Rb_DLCZ_MEMORY_BANDWIDTH)
        self.set_memory_param("temperature", Rb_DLCZ_MEMORY_TEMPERATURE)
        self.set_memory_param("magnetic_field", Rb_DLCZ_MEMORY_MAGNETIC_FIELD)
        self.set_memory_param("wavelength", Rb_DLCZ_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", Rb_DLCZ_MEMORY_MULTIMODE_CAPACITY)

        # Check input validity against memory parameters
        self.check_input_validity()

    
