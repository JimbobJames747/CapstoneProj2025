import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 参数设置
# -----------------------------
eta_m = 0.8  # Memory efficiency (can be changed)
pb0 = 0.5    # BSM success probability without memory
pb_mem = pb0 * eta_m**4  # Effective BSM probability with memory

# -----------------------------
# Guha 优于 Full-Memory 的条件变形：
# 1 / (1 - (1 - p)^M)^2 <= 3 / (2 * p * eta_m^2)
# 即：eta_w >= sqrt((2/3) * p * eta_m^2)
# -----------------------------

def threshold_eta_w(p):
    return np.sqrt((2 / 3) * p * eta_m**2)

# -----------------------------
# 给定 p 求最小 M 使得 eta_w 满足条件
# -----------------------------

def find_min_M(p, threshold_func):
    target = threshold_func(p)
    for M in range(1, 1000):
        eta_w = 1 - (1 - p) ** M
        if eta_w >= target:
            return M
    return np.nan

# -----------------------------
# 主仿真
# -----------------------------

p_vals = np.linspace(0.01, 0.9, 50)
M_vals = [find_min_M(p, threshold_eta_w) for p in p_vals]

# -----------------------------
# 标记 M 从 1 到 2 的临界点
# -----------------------------

transition_idx = next(i for i, m in enumerate(M_vals) if m > 1)
transition_p = p_vals[transition_idx]
transition_M = M_vals[transition_idx]

# -----------------------------
# 自定义坐标轴刻度
# -----------------------------

xticks = [0.01] + list(np.arange(0.1, 1.0, 0.1))
xtick_labels = [f"{x:.2f}" if x == 0.01 else f"{x:.1f}" for x in xticks]

# -----------------------------
# 绘图
# -----------------------------

plt.figure(figsize=(10, 6))
plt.plot(p_vals, M_vals, 'o-', color='darkgreen', linewidth=2, markersize=4, label='Minimum M*')
plt.axvline(transition_p, color='red', linestyle='--', linewidth=1.5)
plt.plot(transition_p, transition_M, 'ro', markersize=8, label=f'M* jumps to 7 at p ≈ {transition_p:.3f}=100dB')

plt.xticks(xticks, labels=xtick_labels)
plt.xlabel(r"Link success probability $\eta_{\mathrm{tr}} = 10^{-\alpha L / 10},\ \alpha = 0.2\,\mathrm{dB/km}$", fontsize=16)

plt.ylabel("Minimum WDM Channels M*", fontsize=16)
plt.title("Required WDM Channels M* vs Link Success Probability ηtr", fontsize=20)
plt.grid(True, linestyle='--', alpha=0.6)
plt.tick_params(axis='both', which='major', labelsize=16)
plt.legend(fontsize=16)
plt.tight_layout()
plt.show()
