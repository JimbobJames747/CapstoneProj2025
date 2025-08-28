import numpy as np
import matplotlib.pyplot as plt

# Parameter settings
t0 = 1e-6   # Time unit for each attempt by light source to send EP = should theoretically be >= detector dead time (s)
eta_tr_values = [0.9, 0.6, 0.3, 0.01]  # Different eta_tr values to compare
pb = 0.4       # BSM success probability
eta_m = 0.7
pb_1 = 0.5 * eta_m**4
tb = 1e-6   # BSM operation time = detector dead time (s)
tc = 2e-5     # Classical communication delay (s)

def harmonic_number(m):
    """Calculate the m-th harmonic number H_m = sum(1/k) for k=1 to m"""
    return sum(1/k for k in range(1, m+1))

def sequential_time(N, eta_tr):
    """
    Corrected Sequential formula:
    T_seq(N) = (1/pb) * [(3/2 * t0/p + tb + tc) + (N-2) * (t0/p + tb + tc)]
    """
    delta = (tb + tc) / pb
    first_segment = 3/2 * t0/(pb_1*eta_tr) + (tb + tc)/pb
    remaining_segments = (N - 2) * (t0/(pb_1*eta_tr) + (tb + tc)/pb)
    return first_segment + remaining_segments

def tree_time(N, eta_tr):
    """
    Updated Binary Tree Structure using harmonic number theory:
    For N links, we have N/2 independent events at the first layer
    Expected time for maximum of N/2 independent exponential events = μ * H_{N/2}
    where μ = t0/p and H_m is the m-th harmonic number
    Plus BSM delays for all layers
    """
    delta = (tb + tc) / pb
    n = int(np.log2(N))  # number of layers
    m = N // 2  # number of independent events at first layer
    
    # Base time using harmonic number theory
    mu = 3*t0 / (2 *pb_1*eta_tr)  # mean of exponential distribution
    H_m = harmonic_number(m)
    base_time = mu * H_m
    # Add BSM delays for all layers
    bsm_delays_total = 0
    while m >= 1:
        H_m = harmonic_number(m)
        bsm_delays = H_m * delta
        bsm_delays_total += bsm_delays
        m //= 2  # Move to the next layer (half the nodes in the next layer)
    return base_time + bsm_delays_total

def waitless_time(N, eta_tr):
    """
    Waitless Protocol - Calculate expected time based on N=2^n
    """
    delta = (tb + tc) / pb
    n = int(np.log2(N))
    result = t0 / (eta_tr**(2**n) * pb**(2**n - 1)) + delta
    return result 

# Display up to N=64, but waitless protocol can only show smaller N values due to extremely large numbers
N_values = [2**i for i in range(1, 7)]  # N = 2, 4, 8, 16, 32, 64

# Create 2x2 subplot layout
fig, axes = plt.subplots(2, 2, figsize=(16, 16))
#fig.suptitle('Comparison of Raw Key Rates: Sequential vs. Binary Tree(Full-memory) vs. Parallel Protocol', fontsize=20, y=1)  # 16 -> 32

# Colors and markers for different protocols
colors = ['blue', 'green', 'red']
markers = ['o', 's', '^']
protocol_names = ['Sequential Structure', 'Binary Tree Structure (Full-memory)', 'Parallel Protocol']

# Plot for each eta_tr value in separate subplots
for idx, eta_tr in enumerate(eta_tr_values):
    # Determine subplot position
    row = idx // 2
    col = idx % 2
    ax = axes[row, col]
    
    # Calculate time for each protocol
    sequential_times = [sequential_time(N, eta_tr) for N in N_values]
    tree_times = [tree_time(N, eta_tr) for N in N_values]
    waitless_times = []

    for N in N_values:
        wt = waitless_time(N, eta_tr)
        # For waitless protocol, set to NaN when N>=32 due to extremely large values to avoid display issues in log plot
        if N >= 32 or np.isnan(wt) or wt > 1e6:
            waitless_times.append(np.nan)
        else:
            waitless_times.append(wt)

    # Calculate generation rates (bits/s) - each successful entanglement generation produces 1 bit of shared secret
    sequential_rates = [1 / t for t in sequential_times]
    tree_rates = [1 / t for t in tree_times]
    waitless_rates = []

    for wt in waitless_times:
        if not np.isnan(wt) and wt > 0:
            waitless_rates.append(1 / wt)
        else:
            waitless_rates.append(np.nan)

    # Plot lines for each protocol
    ax.plot(N_values, sequential_rates, marker=markers[0], linestyle='-', 
            label='Sequential Structure', linewidth=2, markersize=8, color=colors[0])
    ax.plot(N_values, tree_rates, marker=markers[1], linestyle='-', 
            label='Binary Tree Structure(Full-memory)', linewidth=2, markersize=8, color=colors[1])
    ax.plot(N_values, waitless_rates, marker=markers[2], linestyle='-', 
            label='Parallel Protocol', linewidth=2, markersize=8, color=colors[2])

    # Set logarithmic y-axis for rates
    ax.set_yscale('log')
    
    # Set labels and title for each subplot
    if row == 1:  # Only show x-label for bottom row
        ax.set_xlabel('Number of Single Links (N)', fontsize=24)  # 12 -> 24
    ax.set_ylabel('R_raw (bits/s)', fontsize=24)  # 12 -> 24
    ax.set_title(f'ηtr = {eta_tr}', fontsize=18, fontweight='bold')  # 14 -> 28
    
    # 放大刻度标签字体
    ax.tick_params(axis='both', which='major', labelsize=20)  # 增加这行，原来没有设置
    ax.tick_params(axis='both', which='minor', labelsize=18)  # 增加这行，原来没有设置
    
    # Grid and legend
    ax.grid(True, which='both', linestyle='--', alpha=0.3)
    ax.set_xticks(N_values)
    ax.set_xticklabels([str(N) for N in N_values])
    
    # Add legend only to the first subplot to avoid repetition
    if idx == 0:
        ax.legend(fontsize=12, loc='upper right')  # 10 -> 20

# Adjust layout to prevent overlap
# Adjust layout to prevent overlap and add more space between rows
plt.tight_layout()
plt.subplots_adjust(top=0.93, bottom=0.08, hspace=0.15) 

# Add parameter information at the bottom
# param_text = f'Parameters: Tq={t0*1e6:.0f}μs, ηd={0.8}, ηm={eta_m}, tb={tb*1e6:.0f}μs, tc={tc*1e6:.0f}μs'
# fig.text(0.5, 0.02, param_text, ha='center', fontsize=28, style='italic')  # 14 -> 28

plt.show()

# Print numerical results for all eta_tr values
print("\n" + "="*100)
print("Generation Rate Comparison (bits/s) for Different ηtr Values:")
print("="*100)

for eta_tr in eta_tr_values:
    print(f"\nηtr = {eta_tr}:")
    print("Links (N)\tSequential Rate\tTree Rate\tParallel Rate")
    print("-" * 65)
    
    # Recalculate for this eta_tr value
    sequential_times = [sequential_time(N, eta_tr) for N in N_values]
    tree_times = [tree_time(N, eta_tr) for N in N_values]
    waitless_times = []

    for N in N_values:
        wt = waitless_time(N, eta_tr)
        if N >= 32 or np.isnan(wt) or wt > 1e6:
            waitless_times.append(np.nan)
        else:
            waitless_times.append(wt)

    sequential_times = [sequential_time(N, eta_tr) for N in N_values]
    tree_times = [tree_time(N, eta_tr) for N in N_values]
    waitless_times = []

    for N in N_values:
        wt = waitless_time(N, eta_tr)
        if N >= 32 or np.isnan(wt) or wt > 1e6:
            waitless_times.append(np.nan)
        else:
            waitless_times.append(wt)

    sequential_rates = [1 / t for t in sequential_times]
    tree_rates = [1 / t for t in tree_times]
    waitless_rates = []

    for wt in waitless_times:
        if not np.isnan(wt) and wt > 0:
            waitless_rates.append(1 / wt)
        else:
            waitless_rates.append(np.nan)
    
    for i, N in enumerate(N_values):
        seq_rate = sequential_rates[i]
        tree_rate = tree_rates[i]
        if not np.isnan(waitless_rates[i]):
            wait_rate_str = f"{waitless_rates[i]:.2e}"
        else:
            wait_rate_str = "~0"
        
        print(f"{N}\t\t{seq_rate:.2e}\t\t{tree_rate:.2e}\t\t{wait_rate_str}")