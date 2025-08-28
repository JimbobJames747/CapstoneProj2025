class QuantumMemory:
    def __init__(self, name: str, wavelength: float, storage_time: float, fidelity: float, heralded: bool = False, verbose: bool = False):
        self._name = name                     
        self._wavelength = wavelength if isinstance(wavelength, list) else [wavelength] # Wavelength [nm]
        self._storage_time = storage_time     # Storage time [s]
        self._fidelity = fidelity             # Fidelity [dimensionless]
        self._heralded = heralded             # Heralded [bool]
        self._verbose = verbose

    # Setter functions
    def set_name(self, name):
        self._name = name
    def set_wavelength(self, wavelength):
        self._wavelength = wavelength if isinstance(wavelength, list) else [wavelength]
    def set_storage_time(self, storage_time):
        self._storage_time = storage_time
    def set_fidelity(self, fidelity):
        self._fidelity = fidelity
    def set_heralded(self, heralded):
        self._heralded = heralded

    # Getter functions
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
    def heralded(self):
        return print('Heralded:', self._heralded)
    
    
    