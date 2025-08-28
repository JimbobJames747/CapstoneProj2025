# Plot η_max(T) and η_QEC(T) on the same axes with fixed C, τ, γ, γs.
# Assumptions:
# - For baseline memory (no QEC), storage time equals total time: τs = T,
#   so η_max(T) = (C/(1+C))^2 * exp(-2 * γs * T).
# - For QEC, use ρ_logic(T) from the given P(x) and cycle time τ.
#
# Fixed defaults (editable):
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
'''from caas_jupyter_tools import display_dataframe_to_user'''

C = 3.0            # cooperativity (dimensionless)
tau = 10.0         # μs, QEC cycle time
gamma = 1/100.0    # μs^-1, used in P(x)
gamma_s = 1/50.0   # μs^-1, spin-wave decay rate (non-zero)
T_max = 1000.0     # μs
num_points = 1000

def P_of_x(x, gamma):
    return np.exp(-8.0 * gamma * x) * (5.0 - 4.0 * np.exp(-2.0 * gamma * x))

def rho_logic_array(T_array, tau, gamma):
    T_array = np.asarray(T_array)
    out = np.empty_like(T_array, dtype=float)
    P_tau = P_of_x(tau, gamma)
    for i, T in enumerate(T_array):
        N = int(np.floor(T / tau))
        Delta = T - N * tau
        out[i] = (P_tau ** N) * P_of_x(Delta, gamma)
    return out

def eta_max_T(T, C, gamma_s):
    return (C/(1.0 + C))**2 * np.exp(-2.0 * gamma_s * T)

T_vals = np.linspace(0.0, T_max, num_points)
eta_max_vals = eta_max_T(T_vals, C, gamma_s)
rho_vals = rho_logic_array(T_vals, tau, gamma)
eta_qec_vals = (C/(1.0 + C))**2 * rho_vals

# Display parameter table
param_df = pd.DataFrame({
    "Parameter": ["C", "τ (μs)", "γ (μs^-1)", "γs (μs^-1)", "T range (μs)"],
    "Value": [C, tau, gamma, gamma_s, f"0–{T_max}"],
})
'''display_dataframe_to_user("固定参数（可调整）", param_df)'''

# Single plot with both curves
plt.figure(figsize=(6, 4.8))
plt.plot(T_vals, eta_max_vals, label="η_max(T) baseline (no QEC)")
plt.plot(T_vals, eta_qec_vals, label="η_QEC(T) with cycles")
plt.xlabel("T (μs)")
plt.ylabel("η")
plt.title("Performance Analysis of QEC in Quantum Memory")
plt.grid(False)
plt.tick_params(direction='in')
plt.legend()
plt.savefig('QEC_M', dpi=300)
plt.show()

# Save combined data
'''combined = pd.DataFrame({
    "T_us": T_vals,
    "eta_max_baseline": eta_max_vals,
    "eta_QEC": eta_qec_vals,
    "rho_logic": rho_vals,
})
combined.to_csv("/mnt/data/eta_vs_T_combined.csv", index=False)
"/mnt/data/eta_vs_T_combined.csv"'''
