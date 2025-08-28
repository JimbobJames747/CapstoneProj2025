from GEM import GEM
from parameters import *

# === Pr GEM Memory Class ===
class PrGEM(GEM):
    def __init__(
        self,
        name: str,
        in_wavelength: float,
        in_storage_time: float,
        in_fidelity: float,
        verbose: bool = False,
        qfcd: bool = True  
    ):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Set internal memory parameters using the global constants
        self.set_memory_param("fidelity", PR_GEM_MEMORY_FIDELITY)
        self.set_memory_param("storage_time", PR_GEM_MEMORY_STORAGE_TIME)
        self.set_memory_param("bandwidth", PR_GEM_MEMORY_BANDWIDTH)
        self.set_memory_param("temperature", PR_GEM_MEMORY_TEMPERATURE)
        self.set_memory_param("magnetic_field", PR_GEM_MEMORY_MAGNETIC_FIELD)
        self.set_memory_param("wavelength", PR_GEM_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", PR_GEM_MEMORY_MULTIMODE_CAPACITY)

        # Set QFCD parameters only if enabled
        if qfcd:
            self.set_memory_param("fidelity", QFCD_FIDELITY)
            self.set_memory_param(
                "efficiency",
                PR_GEM_MEMORY_EFFICIENCY * TRANSMISSION_EFFICIENCY * PR_QFCD_EFFICIENCY
            )

        # Check input validity against memory parameters
        self.check_input_validity()


    
