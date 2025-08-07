from EIT import EIT
from parameters import *

# Laser-cooled Atom EIT Memory Class 
class LaserCooledAtom(EIT):
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, verbose: bool = False):
        super().__init__(name, in_wavelength, in_storage_time, in_fidelity, verbose)

        # Set internal memory parameters using the dictionary
        self.set_memory_param("fidelity", LC_MEMORY_FIDELITY)
        self.set_memory_param("efficiency", LC_MEMORY_EFFICIENCY)
        self.set_memory_param("storage_time", LC_MEMORY_STORAGE_TIME)
        self.set_memory_param("bandwidth", LC_MEMORY_BANDWIDTH)
        self.set_memory_param("temperature", LC_MEMORY_TEMPERATURE)
        self.set_memory_param("magnetic_field", LC_MEMORY_MAGNETIC_FIELD)
        self.set_memory_param("wavelength", LC_MEMORY_WAVELENGTH)
        self.set_memory_param("multimode_capacity", LC_MEMORY_MULTIMODE_CAPACITY)

        # Check input validity against memory parameters
        self.check_input_validity()

