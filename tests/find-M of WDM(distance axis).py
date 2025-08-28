import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 参数设置
# -----------------------------
eta_m = 0.8       # Memory efficiency
pb0 = 0.5         # BSM success probability without memory
pb_mem = pb0 * eta_m**2  # BSM success probability with memory
alpha = 0.20      # Fibre loss in dB/km

# -----------------------------
# 计算阈值函数：eta_w >= sqrt((2/3) * p * eta_m^2)
# -----------------------------
def threshold_eta_w(p):
    return np.sqrt((2 / 3) * p * eta_m**2)

# -----------------------------
# 给定 p 求最小 M
# -----------------------------
def find_min_M(p, threshold_func):
    target = threshold_func(p)
    for M in range(1, 1000):
        eta_w = 1 - (1 - p) ** M
        if eta_w >= target:
            return M
    return np.nan

# -----------------------------
# 主仿真过程
# -----------------------------
p_vals = np.linspace(0.01, 0.9, 500)
M_vals = [find_min_M(p, threshold_eta_w) for p in p_vals]

# 把 p 映射到距离 D
D_vals = -(10 / alpha) * np.log10(p_vals)


# -----------------------------
# 找转折点 M=2 的位置
# -----------------------------
transition_idx = next(i for i, m in enumerate(M_vals) if m > 1)
transition_D = D_vals[transition_idx]
transition_M = M_vals[transition_idx]

# -----------------------------
# 绘图
# -----------------------------
plt.figure(figsize=(10, 6))
plt.plot(D_vals, M_vals, 'o-', color='darkblue', linewidth=2, markersize=4, label='Minimum M*')

plt.axvline(transition_D, color='red', linestyle='--', linewidth=1.5)
plt.plot(transition_D, transition_M, 'ro', markersize=8, label=f'M* jumps to 7 at D ≈ {transition_D:.1f} km')

plt.xlabel("Distance per Link (km)", fontsize=18)
plt.ylabel("Minimum WDM Channels M*", fontsize=18)
plt.title("Required WDM Channels M* vs Link Distance", fontsize=20)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()
