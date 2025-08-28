from EIT import EIT
from parameters import *

# Rb Vapour EIT Memory Class 
class RbVapourEIT(EIT):
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, qfcd: bool = True, verbose: bool = False):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Set internal memory parameters using the updated global constants
        self.set_memory_param("fidelity", VAPOUR_EIT_MEMORY_FIDELITY)
        self.set_memory_param("efficiency", VAPOUR_EIT_MEMORY_EFFICIENCY)
        self.set_memory_param("storage_time", VAPOUR_EIT_MEMORY_STORAGE_TIME)
        self.set_memory_param("bandwidth", VAPOUR_EIT_MEMORY_BANDWIDTH)
        self.set_memory_param("temperature", VAPOUR_EIT_MEMORY_TEMPERATURE)
        self.set_memory_param("magnetic_field", VAPOUR_EIT_MEMORY_MAGNETIC_FIELD)
        self.set_memory_param("wavelength", VAPOUR_EIT_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", VAPOUR_EIT_MEMORY_MULTIMODE_CAPACITY)

        # Set QFCD parameters only if enabled
        if qfcd:
            self.set_memory_param("fidelity", QFCD_FIDELITY)
            self.set_memory_param(
                "efficiency",
                VAPOUR_EIT_MEMORY_EFFICIENCY * TRANSMISSION_EFFICIENCY * RB_QFCD_EFFICIENCY
            )

        # Check input validity against memory parameters
        self.check_input_validity()


