import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp, cumulative_trapezoid 

# Constants
TIME_STEPS = 1000

def input_pulse(t, T):
    """Gaussian-like input pulse from Eq. (34), normalized."""
    A = 2.09
    return A / np.sqrt(T) * (np.exp(-30 * (t / T - 0.5)**2) - np.exp(-7.5))

def Omega(t, E_in, C, Delta, gamma):
    """Adiabatic control field Ω(t) without the phase term (efficiency-only)."""
    gamma_eff = gamma * (1 + C)
    denominator = np.sqrt(2 * gamma * (1 + C))
    integrand = cumulative_trapezoid(np.abs(E_in)**2, t, initial=0)
    Omega = - ((gamma_eff - 1j * Delta) / denominator) * (E_in / np.sqrt(integrand + 1e-12))
    #Omega = ((1j * Delta) / denominator) * (E_in / np.sqrt(integrand + 1e-12))
    return Omega

def total_efficiency(T, C, Delta, gamma, gamma_sw=0.0, storage_time=0.0, storage_decay=False, verbose=False):
    """Compute η_total by solving the system of ODEs for (P, S)."""
    t_vals = np.linspace(0, T, TIME_STEPS)
    E_in_vals = input_pulse(t_vals, T)
    
    #scaling_factor = (gamma * C * np.sqrt(T) / Delta) if Delta > gamma*C else 1.0
    Omega_vals = Omega(t_vals, E_in_vals, C, Delta, gamma) #* scaling_factor

    def dynamics(t, y):
        P = y[0] + 1j * y[1]
        S = y[2] + 1j * y[3]
        idx = np.searchsorted(t_vals, t, side='right') - 1
        if idx < 0 or idx >= len(t_vals):
            return [0, 0, 0, 0]
        Omega_t = Omega_vals[idx]
        E_in_t = E_in_vals[idx]
        dP = - (gamma * (1 + C) + 1j * Delta) * P + 1j * Omega_t * S + 1j * np.sqrt(2 * gamma * C) * E_in_t
        dS = 1j * np.conj(Omega_t) * P
        return [dP.real, dP.imag, dS.real, dS.imag]

    sol = solve_ivp(dynamics, [0, T], [0, 0, 0, 0], t_eval=[T])
    S_final = sol.y[2][0] + 1j * sol.y[3][0]

    eta_storage = np.abs(S_final)**2
    eta_total = eta_storage * (C / (1 + C)) if C > 0 else 0.0

    if storage_decay:
        eta_total *= np.exp(-2 * gamma_sw * storage_time)

    if verbose:
        print(f"Total η = {eta_total:.4f}")

    return eta_total

def main():
    # Simulation config
    C = 10                      # cooperativity
    Delta_vals = [100, 1000]  # can be customized
    gamma = 1.0
    storage_decay = False
    gamma_sw = 0.0
    storage_time = 0.0

    TCgamma_vals = np.linspace(1, 100, 100)

    # Plot
    plt.figure(figsize=(10, 6))
    for Delta in Delta_vals:
        eta_totals = []
        delta_label = Delta
        for TCgamma in TCgamma_vals:
            # Example adjustment (you can tweak the scaling):
            T = TCgamma * (Delta / (gamma * C))**2 / (C * gamma)

            #T = TCgamma / (C * gamma) if C > 0 else TCgamma  # fallback for C=0
            #Delta /= np.sqrt(TCgamma)
            eta = total_efficiency(
                T=T, C=C, Delta=Delta, gamma=gamma,
                gamma_sw=gamma_sw, storage_time=storage_time,
                storage_decay=storage_decay
            )
            eta_totals.append(eta)

        plt.plot(TCgamma_vals, eta_totals, label=f'Δ = {delta_label}')

    eta_max = (C / (1 + C))**2 

    plt.hlines(eta_max, TCgamma_vals[0], TCgamma_vals[-1], linestyles='dashed', colors='gray')

    # Final plot settings
    plt.xlabel(r'$T \cdot C \cdot \gamma$')
    plt.ylabel(r'Total Efficiency $\eta_{\mathrm{total}}$')
    plt.title("Adiabatic Memory Efficiency for C = 10")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    # plt.savefig("cavity_model_efficiency_C0.png", dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    main()
