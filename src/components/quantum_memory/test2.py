#
# Full Python code to reproduce Figure 2b from Gorshkov et al.,
# "Photon storage in Lambda-type optically dense atomic media. I. Cavity model"
# arXiv:quant-ph/0612082v2
#

import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
from tqdm import tqdm

# --- 1. Define Constants and Simulation Parameters ---

# Physical parameters from Figure 2b
C = 10.0      # Cooperativity parameter
GAMMA = 1.0   # Polarization decay rate (can be set to 1 as a reference)

# Simulation parameters to match the figure
# These are the detuning values for the different curves in Fig 2b.
DELTA_OVER_GAMMA_VALUES = [0, 10, 100, 1000]
TC_GAMMA_VALUES = np.linspace(1, 50, 50) # Range for the x-axis

# --- 2. Define Helper Functions ---

# 2a. Calculate the normalization constant 'A' for the input pulse
# The input pulse must be normalized such that integral(|E_in(t)|^2, t=0..T) = 1.
# The paper provides E_in(t) = A * (unnormalized_shape) / sqrt(T).
# This requires A = 1 / sqrt(integral(|unnormalized_shape(u)|^2, u=0..1)), where u=t/T.
def e_in_unnormalized_sq(u):
    """The squared shape of the unnormalized input pulse."""
    return (np.exp(-30 * (u - 0.5)**2) - np.exp(-7.5))**2

integral_K, _ = quad(e_in_unnormalized_sq, 0, 1)
A_NORM = 1.0 / np.sqrt(integral_K)
# The paper states A is approx 2.09, which this calculation confirms.
print(f"Calculated normalization constant A: {A_NORM:.4f}")


# 2b. Define the input pulse function E_in(t)
def E_in(t, T):
    """
    Calculates the amplitude of the Gaussian-like input pulse E_in at time t
    for a total pulse duration T, as given by Eq. (34).
    """
    if t < 0 or t > T:
        return 0.0
    u = t / T
    return A_NORM * (np.exp(-30 * (u - 0.5)**2) - np.exp(-7.5)) / np.sqrt(T)


# 2c. Define the system of ordinary differential equations (ODEs)
def ode_system(t, y, T, C, gamma, delta, omega_interp_func, e_in_interp_func):
    """
    Defines the exact equations of motion (Eqs. 10, 11) for the system.
    This function is passed to the ODE solver.
    y is a real vector [P_real, P_imag, S_real, S_imag].
    """
    # Reconstruct complex variables from the real vector y
    P = y[0] + 1j * y[1]
    S = y[2] + 1j * y[3]

    # Get time-dependent field values from interpolated functions
    omega_t = omega_interp_func(t)
    e_in_t = e_in_interp_func(t)

    # Eq. (10): dP/dt = -(gamma(1+C) + i*delta)P + i*omega*S + i*sqrt(2*gamma*C)*E_in
    dP_dt = -(gamma * (1 + C) + 1j * delta) * P + 1j * omega_t * S + 1j * np.sqrt(2 * gamma * C) * e_in_t
    # Eq. (11): dS/dt = i*omega_conj*P
    dS_dt = 1j * np.conj(omega_t) * P

    # Return derivatives as a flattened real vector for the solver
    return [dP_dt.real, dP_dt.imag, dS_dt.real, dS_dt.imag]


# --- 3. Main Simulation Loop ---

all_results = {}

# Loop over each detuning value to generate each curve in the plot
for delta_over_gamma in DELTA_OVER_GAMMA_VALUES:
    delta = delta_over_gamma * GAMMA
    print(f"\nCalculating for Delta/gamma = {delta_over_gamma}...")
    results_for_delta = []

    # Loop over each point on the x-axis (TCgamma)
    # A progress bar is used here for better user experience.
    for tc_gamma in tqdm(TC_GAMMA_VALUES, desc=f"Simulating Delta/gamma={delta_over_gamma}"):
        # Calculate pulse duration T for the current x-axis point
        T = tc_gamma / (C * GAMMA)
        
        # Create a fine time grid for calculating the control pulse
        t_grid = np.linspace(0, T, 2000)
        dt = t_grid[1] - t_grid[0]

        # --- Step A: Calculate the optimal control pulse Omega(t) using Eq. (26) ---
        
        # Vectorize E_in calculation for speed
        e_in_vals = np.array([E_in(t, T) for t in t_grid])
        e_in_sq_vals = np.abs(e_in_vals)**2

        # Calculate the integral I(t) = integral from t to T of |E_in|^2
        # This is done efficiently using a reverse cumulative sum.
        integral_I_t = np.cumsum((e_in_sq_vals * dt)[::-1])[::-1]
        # Avoid division by zero at the last point where the integral is zero
        integral_I_t[integral_I_t < 1e-20] = 1e-20

        # Calculate the magnitude squared of Omega
        omega_mag_sq_numerator = (GAMMA*(1+C))**2 + delta**2
        omega_mag_sq_denominator = 2 * GAMMA * (1+C)
        omega_mag_sq = (omega_mag_sq_numerator / omega_mag_sq_denominator) * (e_in_sq_vals / integral_I_t)

        # Apply the truncation as described in the paper for t < T/100
        trunc_time = T / 100.0
        # Find the index corresponding to the truncation time
        trunc_idx = np.searchsorted(t_grid, trunc_time)
        if trunc_idx > 0 and trunc_idx < len(omega_mag_sq):
             omega_mag_sq[:trunc_idx] = omega_mag_sq[trunc_idx]

        # Calculate h(t,T) = integral from t to T of |Omega|^2
        integral_h_t_T = np.cumsum((omega_mag_sq * dt)[::-1])[::-1]

        # Calculate the phase factor for Omega from the Stark shift term
        phase_exponent = 1j * delta * integral_h_t_T / ((GAMMA*(1+C))**2 + delta**2)
        phase_factor = np.exp(phase_exponent)

        # Assemble the full complex Omega(t) using Eq. (26)
        prefactor = (GAMMA*(1+C) + 1j*delta) / np.sqrt(2*GAMMA*(1+C))
        omega_vals = prefactor * (e_in_vals / np.sqrt(integral_I_t)) * phase_factor

        # Create interpolation functions for Omega and E_in to pass to the ODE solver.
        # This is much more efficient than recalculating at every solver step.
        omega_interp = interp1d(t_grid, omega_vals, bounds_error=False, fill_value=0)
        e_in_interp = interp1d(t_grid, e_in_vals, bounds_error=False, fill_value=0)

        # --- Step B: Solve the exact ODEs numerically ---
        y0 = [0.0, 0.0, 0.0, 0.0]  # Initial conditions: P(0)=0, S(0)=0
        t_span = [0, T]
        
        sol = solve_ivp(
            ode_system,
            t_span,
            y0,
            method='RK45',
            args=(T, C, GAMMA, delta, omega_interp, e_in_interp),
            dense_output=True
        )

        # --- Step C: Calculate the total efficiency ---
        # Extract the final value of the spin-wave S(T)
        S_T_complex = sol.y[2, -1] + 1j * sol.y[3, -1]
        
        # Storage efficiency eta_s = |S(T)|^2
        eta_s = np.abs(S_T_complex)**2
        
        # Total efficiency = eta_s * eta_r, where eta_r = C/(1+C)
        eta_tot = eta_s * (C / (1 + C))
        results_for_delta.append(eta_tot)

    all_results[delta_over_gamma] = np.array(results_for_delta)

# --- 4. Plot the Final Figure ---

plt.style.use('seaborn-v0_8-whitegrid')
plt.figure(figsize=(12, 7))

# Plot the theoretical maximum efficiency line
eta_max = (C / (1 + C))**2
plt.axhline(y=eta_max, color='k', linestyle='--', label=f'Theoretical Max ($(C/(1+C))^2$) = {eta_max:.3f}')

# Plot the results for each detuning
for delta_over_gamma, efficiencies in all_results.items():
    plt.plot(TC_GAMMA_VALUES, efficiencies, marker='o', markersize=4, linestyle='-', label=f'$\\Delta/\\gamma = {int(delta_over_gamma)}$')

# Formatting the plot to match Figure 2b
plt.xlabel('$TC\\gamma$', fontsize=14)
plt.ylabel('Total Efficiency $\\eta_{tot}$', fontsize=14)
plt.title(f'Breakdown of Optimal Adiabatic Storage in a Cavity (Fig. 2b Recreation)\n$C={int(C)}$', fontsize=16)
plt.legend(title='Detuning', fontsize=12)
plt.ylim(0, 1.05 * eta_max)
plt.xlim(0, 50)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()
