import numpy as np
from scipy.integrate import solve_ivp, cumulative_trapezoid
import matplotlib.pyplot as plt
from QuantumMemory import QuantumMemory
from parameters import *

# Assuming the cavity is resonant with the input pulse
class LambdaCavityModel(QuantumMemory):
    """
    Quantum memory cavity model for a Lambda-type system.
    Simulates storage and retrieval efficiencies, fidelity, and adiabatic control field Ω(t).
    """
    def __init__(self, period, cooperativity, storage_decay: float = 0.0, **kwargs):
        """
        Initialize the Lambda cavity model with:
        
        - period: pulse duration T (time)
        - cooperativity: cavity cooperativity C (dimensionless)
        - storage_decay: spin-wave decay rate γ_s (inverse time)

        Additional quantum memory parameters can be passed via kwargs.
        """
        super().__init__(**kwargs)
        self._T = period                     # Pulse duration [s]   
        self._C = cooperativity              # Cooperativity [dimensionless]
        
        # Memory internal parameters
        self._resonant_wavelength = 0.0     # Resonant wavelength [nm]
        self._Delta = 0.0                   # Detuning, Delta = w_input - w_eg [rad/s]
        self._gamma = 1.0                   # Polarisation decay rate [1/s]
        self._gamma_sw = storage_decay      # Spin-wave decay rate (storage decay rate) [1/s]
        self._storage_decay = storage_decay != 0.0       # Storage decay flag, used for on demand calculation of total efficiency
        self._total_efficiency_val = self._total_efficiency(self._T, self._C, self._Delta, storage_decay=self._storage_decay)       # Retrieval efficiency with storage decay
        self._retrieval_fidelity_val = self._retrieval_fidelity(self._fidelity, self._total_efficiency_val)                         # Retrieval fidelity

    # Setter functions
    def set_period(self, period: float):
        self._T = period
    def set_cooperativity(self, cooperativity: float):
        self._C = cooperativity
    def set_resonant_wavelength(self, resonant_wavelength: float):
        self._resonant_wavelength = resonant_wavelength
    def set_detuning(self, Delta: float):
        self._Delta = Delta
    def set_gamma(self, gamma: float):
        self._gamma = gamma
    def set_storage_decay(self, gamma_sw: float):
        self._gamma_sw = gamma_sw

    # Getter functions
    @property
    def period(self):
        return self._T
    @property
    def cooperativity(self):
        return self._C
    @property
    def resonant_wavelength(self):
        return self._resonant_wavelength
    @property
    def detuning(self):
        return self._Delta
    @property
    def gamma(self):
        return self._gamma
    @property
    def gamma_sw(self):
        return self._gamma_sw
    @property
    def total_efficiency(self):
        return self._total_efficiency_val
    @property
    def retrieval_fidelity(self):
        return self._retrieval_fidelity_val
    @property
    def assumptions(self):
        print("Assumptions & Conditions:")
        print("1. Store one quantum mode")
        print("2. Resonance limit, Lambda_input = Lambda_resonant")
        print("3. Cooperativity does not change with wavelength")
        print("4. Gaussian input mode")
        print("5. Adiabatic limit, TCgamma >> 1")

    # Calculate angular frequency of wavelength
    def _angular_frequency(self, wavelength: float):
        """Calculate angular frequency ω = 2πc/λ given a wavelength."""
        return 2 * np.pi * SPEED_OF_LIGHT / wavelength

    # Calculate input pulse for the cavity model (Eq. 34)
    def _input_pulse(self, t, T):
        """
        Calculate the Gaussian-like input pulse E_in(t) from Eq. (34).
        Returns amplitude normalized so ∫|E_in|^2 dt = 1.
        """
        # Calculate input pulse
        A = 2.09    # Normalisation constant
        input_pulse = A / np.sqrt(T) * (np.exp(-30 * (t / T - 0.5)**2) - np.exp(-7.5))

        return input_pulse

    # Internal calculation of adiabatic control field Ω(t) (Eq. 26)
    def _Omega(self, t, E_in, C, Delta):
        """
        Calculate the adiabatic optimal control field Ω(t) from Eq. (26),
        without the optional explicit phase factor.
        
        Ω(t) is shaped to match E_in(t) for efficient storage.
        """
        # Calculate control shape Omega(t)
        gamma_eff = self._gamma * (1 + C)
        denominator = np.sqrt(2 * self._gamma * (1 + C))
        integrand = cumulative_trapezoid(np.abs(E_in)**2, t, initial=0)
        Omega = - ((gamma_eff - 1j * Delta) / denominator) * (E_in / np.sqrt(integrand + 1e-12))

        return Omega
    
    # Internal calculation of total efficiency (Eq. 35) without storage decay
    def _total_efficiency(self, T, C, Delta, storage_decay=False):
        """
        Compute the total storage + retrieval efficiency η_total.
        
        - Integrates the coupled ODEs (Eqs. 10 & 11) for (P, S).
        - If storage_decay is True, applies exponential decay of spin-wave.
        """
        # Define time steps and calculate input pulse and control shape
        time_steps = np.linspace(0, T, TIME_STEPS)
        E_in_values = self._input_pulse(time_steps, T)
        Omega_values = self._Omega(time_steps, E_in_values, C, Delta)

        # Returns the derivatives of the system 
        def dynamics(t, y):
            # Define P and S as complex numbers
            P = y[0] + 1j * y[1]
            S = y[2] + 1j * y[3]

            # Interpolate Omega and E_in at current time t
            idx = np.searchsorted(time_steps, t) - 1
            if idx < 0 or idx >= len(time_steps):
                return [0, 0, 0, 0]
            Omega = Omega_values[idx]
            E_in = E_in_values[idx]

            # Calculate ODEs
            dP = - (self._gamma * (1 + C) + 1j * Delta) * P + 1j * Omega * S + 1j * np.sqrt(2 * self._gamma * C) * E_in
            dS = 1j * np.conj(Omega) * P
            return [dP.real, dP.imag, dS.real, dS.imag]

        # Solve the system differential equations
        sol = solve_ivp(dynamics, [0, T], [0, 0, 0, 0], t_eval=[T])
        S_final = sol.y[2][0] + 1j * sol.y[3][0]

        # Calculate efficiency
        eta_storage = np.abs(S_final)**2
        eta_total = eta_storage * (C / (1 + C))  # retrieval efficiency

        # Calculate total efficiency with storage decay
        if storage_decay:
            eta_total = eta_storage * (C / (1 + C)) * (np.exp(-2 * self._gamma_sw * self._storage_time))

        # Print efficiency if verbose is True
        if self._verbose:
            print(f"Total efficiency: {eta_total} %")
            print("Storage decay: ", self._storage_decay)

        return eta_total

    # Calculate retrieval fidelity
    def _retrieval_fidelity(self, fidelity: float, total_efficiency: float):
        """
        Compute the total retrieval fidelity combining:
        - intrinsic input state fidelity
        - memory process fidelity based on η_total
        """
        # Calculate memory fidelity
        memory_fidelity = (1 + total_efficiency) / 2

        # Print memory fidelity
        if self._verbose:
            print(f"Memory fidelity: {memory_fidelity}")

        return fidelity * memory_fidelity

    # Plot sweep of the total efficiency for varying C (Delta = 0)
    def plot_efficiency_sweep(self, title: str, save_filename: str = 'cavity_model_efficiency_sweep_figure.png', cooperativity_vals: list = []):
        """
        Plot η_total vs T*C*γ for a sweep of cooperativity values.
        Shows how efficiency grows and saturates for different C.
        """
        # Verbose is always False
        self._verbose = False

        # Set cooperativity values for sweep plot (default is 10^i * C for i = 0, 1, 2, 3)
        if not cooperativity_vals:
            cooperativity_vals = [10**i * self._C for i in range(4)]

        # x-axis: TCγ, 100 steps
        TCgamma_vals = np.linspace(1, 100, 100)  
        
        # Plot figure 
        plt.figure(figsize=(10, 6))

        # Calculate values
        for C in cooperativity_vals:
            eta_totals = []
            # Calculate efficiency for each TCγ value
            for TCgamma in TCgamma_vals:
                T = TCgamma / (C * self._gamma)
                eta = self._total_efficiency(T, C, Delta=self._Delta, storage_decay=self._storage_decay)
                eta_totals.append(eta)
            plt.plot(TCgamma_vals, eta_totals, label=f'C = {C}')
            eta_max = (C / (1 + C))**2
            if self._storage_decay:
                eta_max = eta_max * (np.exp(-2 * self._gamma_sw * self._storage_time))
            plt.hlines(eta_max, TCgamma_vals[0], TCgamma_vals[-1], linestyles='dashed', colors='gray')

        plt.xlabel(r'$T \cdot C \cdot \gamma$')
        plt.ylabel(r'Total Efficiency $\eta_{\mathrm{total}}$')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        plt.show()

    # Plot for input cooperativity only
    def plot_efficiency(self, title: str, save_filename: str = 'cavity_model_efficiency_figure.png'):
        """
        Plot η_total vs T*C*γ for the single cooperativity value.
        Also marks the input point as an 'x'.
        """
        # Verbose is always False
        self._verbose = False

        # x-axis: TCγ, 100 steps
        TCgamma_vals = np.linspace(1, 100, 100)  
        
        # Plot figure 
        plt.figure(figsize=(10, 6))

        # Calculate values
        eta_totals = []
        # Calculate efficiency for each TCγ value
        for TCgamma in TCgamma_vals:
            T = TCgamma / (self._C * self._gamma)
            eta = self._total_efficiency(T, self._C, Delta=self._Delta, storage_decay=self._storage_decay)
            eta_totals.append(eta)
        plt.plot(TCgamma_vals, eta_totals, color='r', label=f'C = {self._C}')

        # Scatter plot of total efficiency of input values 
        TCgamma_X = self._T * self._C * self._gamma
        plt.scatter(TCgamma_X, self._total_efficiency_val, color='b', marker='x', s=100, label='Input Values', zorder=5)

        # Plot maximum efficiency
        eta_max = (self._C / (1 + self._C))**2
        if self._storage_decay:
            eta_max = eta_max * (np.exp(-2 * self._gamma_sw * self._storage_time))
        plt.hlines(eta_max, TCgamma_vals[0], TCgamma_vals[-1], linestyles='dashed', colors='gray')

        plt.xlabel(r'$T \cdot C \cdot \gamma$')
        plt.ylabel(r'Total Efficiency $\eta_{\mathrm{total}}$')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        plt.show()

    # Plot for input cooperativity only
    def plot_fidelity(self, title: str, save_filename: str = 'cavity_model_fidelity_figure.png'):
        """
        Plot retrieval fidelity vs T*C*γ for the single cooperativity value.
        Also marks the input point as an 'x'.
        """
        # Verbose is always False
        self._verbose = False

        # x-axis: TCγ, 100 steps
        TCgamma_vals = np.linspace(1, 100, 100)  
        
        # Plot figure 
        plt.figure(figsize=(10, 6))

        # Calculate values
        fidelity_totals = []
        # Calculate fidelity for each TCγ value
        for TCgamma in TCgamma_vals:
            T = TCgamma / (self._C * self._gamma)
            eta = self._total_efficiency(T, self._C, Delta=self._Delta, storage_decay=self._storage_decay)
            fidelity_totals.append(self._retrieval_fidelity(self._fidelity, eta))
        plt.plot(TCgamma_vals, fidelity_totals, color='r', label=f'C = {self._C}')

        # Scatter plot of fidelity of input values 
        TCgamma_X = self._T * self._C * self._gamma
        plt.scatter(TCgamma_X, self._retrieval_fidelity_val, color='b', marker='x', s=100, label='Input Values', zorder=5)

        plt.xlabel(r'$T \cdot C \cdot \gamma$')
        plt.ylabel(r'Fidelity $F_{\mathrm{retrieval}}$')
        plt.title(title)
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(save_filename, dpi=300, bbox_inches='tight')
        plt.show()


    # WORK IN PROGRESS
    # def plot_efficiency_sweep_Delta(self, title: str, save_filename: str = 'cavity_model_efficiency_sweep_figure.png', Delta_vals: list = []):
    #     """
    #     Plot η_total vs T*C*γ for a sweep of cooperativity values.
    #     Shows how efficiency grows and saturates for different C.
    #     """
    #     # Verbose is always False
    #     self._verbose = False

    #     # Set cooperativity values for sweep plot (default is 10^i * C for i = 0, 1, 2)
    #     if not Delta_vals:
    #         Delta_vals = [10**i for i in range(3)]

    #     # x-axis: TCγ, 100 steps
    #     TCgamma_vals = np.linspace(1, 100, 100)  

    #     C = 10
        
    #     # Plot figure 
    #     plt.figure(figsize=(10, 6))

    #     # Calculate values
    #     for Delta in Delta_vals:
    #         eta_totals = []
    #         # Calculate efficiency for each TCγ value
    #         for TCgamma in TCgamma_vals:
    #             T = TCgamma / (C * self._gamma)
    #             eta = self._total_efficiency(T, C, Delta=Delta, storage_decay=False)
    #             eta_totals.append(eta)
    #         plt.plot(TCgamma_vals, eta_totals, label=f'Delta = {Delta}')
    #         eta_max = (C / (1 + C))**2
    #         plt.hlines(eta_max, TCgamma_vals[0], TCgamma_vals[-1], linestyles='dashed', colors='gray')

    #     plt.xlabel(r'$T \cdot C \cdot \gamma$')
    #     plt.ylabel(r'Total Efficiency $\eta_{\mathrm{total}}$')
    #     plt.title(title)
    #     plt.legend()
    #     plt.grid(True)
    #     plt.tight_layout()
    #     plt.savefig(save_filename, dpi=300, bbox_inches='tight')
    #     plt.show()