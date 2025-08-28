class QuantumMemory:
    def __init__(self, name: str, in_wavelength: float, in_storage_time: float, in_fidelity: float, verbose: bool = False):
        # Validate input parameters
        self.validate_inputs(in_wavelength, in_storage_time, in_fidelity)
        
        # Initialize input parameters
        self._name = name                     
        self._in_wavelength = in_wavelength         # Input Wavelength [m]
        self._in_storage_time = in_storage_time     # Input Storage time [s]
        self._in_fidelity = in_fidelity             # Input Fidelity [dimensionless]
        self._verbose = verbose

        # Internal memory parameters stored in a dictionary
        self._memory_params = {
            "scheme": None,                     # Memory scheme (e.g., EIT, AFC)
            "heralded": None,                   # Heralded [bool]
            "fidelity": None,                   # Memory fidelity [dimensionless]
            "efficiency": None,                 # Memory efficiency [dimensionless]
            "storage_time": None,               # Memory storage time [s]
            "bandwidth": None,                  # Memory bandwidth [MHz]
            "temperature": None,                # Memory temperature [K]
            "magnetic_field": None,             # Memory magnetic field [T]
            "wavelength": None,                 # Memory wavelength [m]
            "multimode_capacity": None          # Memory multimode capacity [dimensionless]
        }


    # Setter functions for input parameters
    def set_name(self, name):
        self._name = name
    def set_in_wavelength(self, wavelength):
        self._wavelength = wavelength if isinstance(wavelength, list) else [wavelength]
    def set_in_storage_time(self, storage_time):
        self._storage_time = storage_time
    def set_in_fidelity(self, fidelity):
        self._fidelity = fidelity

    # Getter functions for input parameters
    @property
    def name(self):
        return self._name
    @property
    def wavelength(self):
        return self._wavelength
    @property
    def storage_time(self):
        return self._storage_time
    @property
    def fidelity(self):
        return self._fidelity
    @property
    def summary(self):
        print("=== Internal Memory Parameters ===")
        print(f"Name: {self._name}")
        for k, v in self._memory_params.items():
            unit = {
                "storage_time": "s",
                "bandwidth": "MHz",
                "temperature": "K",
                "magnetic_field": "T",
                "wavelength": "m"
            }.get(k, "")
            print(f"{k.capitalize().replace('_', ' ')}: {v} {unit}".strip())

    # Set and get memory parameters
    def set_memory_param(self, key, value):
        if key in self._memory_params:
            self._memory_params[key] = value
        else:
            raise KeyError(f"Invalid memory parameter: '{key}'")
    def get_memory_param(self, key):
        return self._memory_params.get(key, None)
    
    # Validate input parameters 
    def validate_inputs(self, in_wavelength, in_storage_time, in_fidelity):
        if in_wavelength <= 0:
            raise ValueError(f"Invalid: Input wavelength must be positive.")
        if in_storage_time <= 0:
            raise ValueError(f"Invalid: Storage time must be positive.")
        if not (0 <= in_fidelity <= 1):
            raise ValueError(f"Invalid: Fidelity must be between 0 and 1 (inclusive).")

    # Check input validity against memory parameters
    def check_input_validity(self):
        mem_wavelength = self.get_memory_param("wavelength")
        mem_storage_time = self.get_memory_param("storage_time")

        if mem_wavelength is not None and abs(self._in_wavelength - mem_wavelength) > 1e-12:
            print(f"Warning: Input wavelength ({self._in_wavelength} m) does not match expected memory wavelength ({mem_wavelength} m).")

        if mem_storage_time is not None and self._in_storage_time > mem_storage_time:
            print(f"Warning: Input storage time ({self._in_storage_time} s) exceeds memory storage time ({mem_storage_time} s).")

    # Retrieved fidelity and efficiency methods
    def retrieved_fidelity(self):
        return self.get_memory_param("fidelity") * self._in_fidelity

    def retrieved_efficiency(self):
        return self.get_memory_param("efficiency")
    
