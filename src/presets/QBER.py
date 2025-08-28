import numpy as np
import matplotlib.pyplot as plt

# --------------------
# 参数（与你给的一致的符号与数值）
# --------------------
Pe = Pr = Pd = 3e-5            # 每次窗/每频模暗计数概率（EL 与 repeater）
eta_e = eta_r = eta_d = 0.9    # 器件效率（发/收/探测）
M = 1000                       # 频复用数（此处仅进入注释展示）
alpha = 0.15                   # 光纤衰减 dB/km
T_q = 50e-9                    # 时隙
t_d = 1.0                      # 端节点探测相关系数前因子（与你式子一致地写成常数）

# --------------------
# 工具函数：平滑 + 保证单调（不引 SciPy，只用滑动平均+前缀极大）
# --------------------
def smooth_monotone(y, k=21):
    """ 简单滑动平均（窗口 k，奇数）后用前缀极大保证单调非降 """
    k = max(3, int(k) | 1)
    pad = k // 2
    ypad = np.r_[np.full(pad, y[0]), y, np.full(pad, y[-1])]
    ker = np.ones(k) / k
    ys = np.convolve(ypad, ker, mode='valid')
    # 单调非降
    return np.maximum.accumulate(ys)

# --------------------
# 物理量：t_e(L), t_r（重复使用你此前的 A/B/C 结构，保持记号一致）
# --------------------
def t_values(L, N):
    """返回 (t_e(L), t_r)。t_e 随距离单调下降；t_r 为复位/BSM 噪声因子（常数）"""
    # 半链路信道透过率（每个 EL 的半段）
    eta_chan = 10 ** (-(alpha * L) / (2 * N) / 10.0)

    # ---- Repeater BSM（与 L 几乎无关，这里按你的表达式保留常数项）----
    # 记：A/B/C 里，a、b 给“真+假”的对称事件，c 给“偶然/暗计数相关”的偏置
    A_r_true_1 = eta_e
    A_r_true_2 = eta_e
    A_r_1 = A_r_true_1 + Pr * (1 - Pr)
    A_r_2 = A_r_true_2 + Pr * (1 - Pr)
    B_r = 1 - (1 - Pr) * ((1 - eta_e) * (1 - eta_e))
    a_r = (1/8) * (A_r_true_1 * A_r_true_2) * (1 - Pr) ** 2
    b_r = (1/8) * A_r_1 * Pr * (1 - A_r_2) * (1 - Pr) \
        + (1/8) * A_r_2 * Pr * (1 - A_r_1) * (1 - Pr) \
        + (1/8) * (Pr ** 2) * (1 - A_r_1) * (1 - A_r_2)
    c_r = (1/8) * Pr * (1 - Pr) * (Pe * (1 - B_r) + B_r * (1 - Pr))
    wr = c_r / max(a_r + b_r, 1e-300)
    t_r = max(1.0 - 2.0 * wr, 1e-6)      # 保证 0<t_r<=1

    # ---- Elementary-link BSM（随 L 变化）----
    tot1 = eta_r * eta_chan
    tot2 = eta_r * eta_chan
    P_click_1 = tot1 + (1 - tot1) * Pe
    P_click_2 = tot2 + (1 - tot2) * Pe
    P_true_1, P_true_2 = tot1, tot2

    A_e_true_1, A_e_true_2 = P_true_1, P_true_2
    A_e_1 = P_click_1 + Pe * (1 - P_click_1)
    A_e_2 = P_click_2 + Pe * (1 - P_click_2)
    B_e = 1 - (1 - Pe) * ((1 - P_true_1) * (1 - P_true_2))

    a_e = (1/8) * A_e_true_1 * A_e_true_2 * (1 - Pe) ** 2
    b_e = (1/8) * A_e_1 * Pe * (1 - A_e_2) * (1 - Pe) \
        + (1/8) * A_e_2 * Pe * (1 - A_e_1) * (1 - Pe) \
        + (1/8) * (Pe ** 2) * (1 - A_e_1) * (1 - A_e_2)
    c_e = (1/8) * Pe * (1 - Pe) * (Pe * (1 - B_e) + B_e * (1 - Pe))
    we = c_e / np.maximum(a_e + b_e, 1e-300)
    t_e = np.clip(1.0 - 2.0 * we, 1e-6, 1.0)  # 保证 0<t_e<=1

    return t_e, t_r

def add_qber_threshold(ax, q=0.11):
    # 黑色、稍粗的虚线；标签也用黑色
    ax.axhline(q, linestyle="--", linewidth=2.5, color="k", alpha=0.9)
    ax.text(0.01, q, f"QBER = {q:.2f}",
            transform=ax.get_yaxis_transform(),
            va="bottom", ha="left", color="k")


# --------------------
# 生成曲线并绘图
# --------------------
L1 = np.linspace(0, 3000, 2000)   # single link
L2 = np.linspace(0, 6000, 3000)   # repeater chain

# --- Single link: Q1(L) = 1/2 [1 - t_d * t_e(L)] ---
t_e_single, _ = t_values(L1, N=1)
Q1 = 0.5 * (1.0 - np.clip(t_d * t_e_single, 0.0, 1.0))
Q1 = smooth_monotone(Q1, k=17)  # 平滑且单调

fig1, ax1 = plt.subplots(figsize=(8.4, 5.2), dpi=140)
ax1.plot(L1, Q1, label="Single link", lw=2.2)
ax1.set_xlabel("L (km)"); ax1.set_ylabel("QBER")
ax1.set_xlim(0, 3000); ax1.set_ylim(0, 0.6)
ax1.grid(True, alpha=0.5)
leg1 = ax1.legend(loc="upper right", frameon=True)

# 右下角参数框（图内）
param_text = (
    r"$P_e=P_r=P_d=3\times10^{-5}$" "\n"
    r"$\eta_e=\eta_r=\eta_d=0.9$" "\n"
    rf"$M={M}$, $\alpha={alpha}\,\mathrm{{dB/km}}$, $T_q={int(T_q*1e9)}\,\mathrm{{ns}}$"
)
ax1.text(0.98, 0.02, param_text, transform=ax1.transAxes,
         va="bottom", ha="right",
         bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.4", alpha=0.95))
plt.tight_layout()
plt.savefig("QBER_single_smooth.png", bbox_inches="tight")

# --- Repeater chain: Q_{n+1}(L) = 1/2 [1 - (t_d/t_r) (t_r t_e)^N ] ---
# ================= 图 2：Repeater chain (N=1,2,4,8) =================
fig2, ax2 = plt.subplots(figsize=(8.4, 5.2), dpi=140)

curves = []
for N in [1, 2, 4, 8]:
    t_e_rep, t_r = t_values(L2, N=N)
    core = (t_d / max(t_r, 1e-12)) * (np.clip(t_r * t_e_rep, 0.0, 1.0) ** N)
    QN = 0.5 * (1.0 - np.clip(core, 0.0, 1.0))
    QN = smooth_monotone(QN, k=17)
    curves.append((N, QN))
    ax2.plot(L2, QN, lw=2.2, label=f"N={N}")

ax2.set_xlabel("L (km)"); ax2.set_ylabel("Quantum Bit Error Rate")
ax2.set_xlim(0, 5000); ax2.set_ylim(0, 0.6)
ax2.grid(True, alpha=0.5)
add_qber_threshold(ax2, q=0.11)
# ---- 参数框固定在右下角 ----
param_text = (
    r"$P_e=P_r=P_d=3\times10^{-5}$" "\n"
    r"$\eta_e=\eta_r=\eta_d=0.9$" "\n"
    rf"$M={M}$, $\alpha={alpha}\,\mathrm{{dB/km}}$, $T_q={int(T_q*1e9)}\,\mathrm{{ns}}$"
)
param_artist = ax2.text(0.98, 0.02, param_text, transform=ax2.transAxes,
                        va="bottom", ha="right",
                        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="0.4", alpha=0.95))

# 先临时放一个图例拿到它的高度
tmp_leg = ax2.legend(loc="lower right", frameon=True)
fig2.canvas.draw()

# 计算参数框的“顶部”位置（轴坐标）
renderer = fig2.canvas.get_renderer()
pb = param_artist.get_window_extent(renderer)
(px0, py0) = ax2.transAxes.inverted().transform((pb.x0, pb.y0))
(px1, py1) = ax2.transAxes.inverted().transform((pb.x1, pb.y1))
param_top_y = py1  # 参数框的上边界（轴坐标）

# 计算图例高度，并把图例“下边界”放到参数框上方留一点空隙
lb = tmp_leg.get_window_extent(renderer)
(lx0, ly0) = ax2.transAxes.inverted().transform((lb.x0, lb.y0))
(lx1, ly1) = ax2.transAxes.inverted().transform((lb.x1, lb.y1))
legend_h = ly1 - ly0

gap = 0.02  # 参数框与图例之间的竖向间距（轴坐标）
anchor_y = param_top_y + gap
# 如果放上去会超出顶端，就往下夹到图内
anchor_y = min(anchor_y, 1.0 - legend_h - 0.02)

# 删除临时图例，按新的位置重建（右下角对齐）
tmp_leg.remove()
leg2 = ax2.legend(loc="lower right", bbox_to_anchor=(0.98, anchor_y), frameon=True)

plt.tight_layout()
plt.savefig("QBER_repeater_smooth_no_overlap.png", bbox_inches="tight")
plt.show()

