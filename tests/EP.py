import numpy as np
import matplotlib.pyplot as plt

def roll(s, n):
    r_even = (1 + (1 - 2*s)**n) / 2
    r_odd = (1 - (1 - 2*s)**n) / 2
    return r_even, r_odd

def multi_copy_purify(F_in, N, noise = False, measurement_purification = False, p_m = 0.02, n = 1):
    L = 1/2
    if F_in < 0 or F_in > 1:
        raise ValueError("Input fidelity must be in the range [0, 1]")
    if N < 1:
        raise ValueError("Number of copies N must be at least 1")
    if p_m < 0 or p_m > 1:
        raise ValueError("Measurement error probability p_m must be in the range [0, 1]")
    if noise == False:
        F_out = F_in**N / (F_in**N + (1 - F_in)**N)
        P_succ = F_in**N + (1 - F_in)**N
        qubit_consumption = 2 * N
    else:
        s = p_m/2
        if measurement_purification == False:
            A = (F_in**N) * (1 - s) + ((1 - F_in)**N) * s
            B = ((1 - F_in)**N) * (1 - s) + (F_in**N) * s
            F_out = A / (A + B)
            P_succ = A + B
            qubit_consumption =2 * N
        else:
            if n > 1:
                r_e, r_o = roll(s,n)
                A = r_e * (F_in**N) + r_o * ((1 - F_in)**N)
                B = r_e * ((1 - F_in)**N) + r_o * (F_in**N)
                F_out = A / (A + B)
                P_succ = A + B
                qubit_consumption = 2 * (N + n)
            else:
                raise ValueError("Measurement purification requires n > 1")
    return F_out, P_succ, qubit_consumption, L

def nested_dejmps(F_in, rounds, reset_and_reuse = False, noise = False, measurement_purification = False, p_m = 0.02, n = 1): 
    if F_in < 0 or F_in > 1:
        raise ValueError("Input fidelity must be in the range [0, 1]")
    if rounds < 1:
        raise ValueError("Number of rounds must be at least 1")
    if p_m < 0 or p_m > 1:
        raise ValueError("Measurement error probability p_m must be in the range [0, 1]")
    F = F_in
    P_total = 1.0
    if noise == False:
        L = 1/2
        if reset_and_reuse == True:
            qubit_consumption = 4
        else:
            qubit_consumption = 2**(rounds + 1)
        for _ in range(rounds):
            P = 0.5 * (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2)
            P_total *= P
            F = (F**2 + (1/9)*(1 - F)**2) / (F**2 + (2/3)*F*(1 - F) + (5/9)*(1 - F)**2)
    else:
        s = p_m / 2
        r_e = (1 - s)**(2*n) + s**(2*n)
        r_o = 2 * (1 - s)**n * s**n
        g = (F * (1 - F)/3 + ((1 - F)/3)**2) * (r_o/r_e)
        if measurement_purification == False:
            if n == 1:
                for _ in range(rounds):
                    P = 0.5 * (r_e * (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2) + r_o * (4 * F * (1 - F)/3 + 4 * ((1 - F)/3)**2 ))
                    P_total *= P
                    F = (F**2 + (1/9)*(1 - F)**2 + g) / (F**2 + (2/3)*F*(1 - F) + (5/9)*(1 - F)**2 + 4 * g)
                L = (r_e + r_o) / 2 * (r_e - r_o)
                if reset_and_reuse == True:
                    qubit_consumption = 4
                else:
                    qubit_consumption = 2 * rounds + 2
            else:
                raise ValueError("Noisy measurement without purification requires n = 1")
        else:
            if n > 1:
                for _ in range(rounds):
                    P = 0.5 * (r_e * (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2) + r_o * (4 * F * (1 - F)/3 + 4 * ((1 - F)/3)**2 ))
                    P_total *= P
                    F = (F**2 + (1/9)*(1 - F)**2 + g) / (F**2 + (2/3)*F*(1 - F) + (5/9)*(1 - F)**2 + 4 * g)
                L = (r_e + r_o) / 2 * (r_e - r_o)
                if reset_and_reuse == True:
                    qubit_consumption = 2 * (1 + n) 
                else:
                    qubit_consumption = 2 * (1 + n) * rounds
            else:
                raise ValueError("Noisy measurement purification requires n > 1")
    return F, P_total, L, qubit_consumption

def hyperentangled_purify(F_p, F_f, scenario, eta=0.57, A=0.92, B=0.05, C=0.05, noise = False, measurement_purification = False, p_m = 0.02, n = 1):
    if F_p < 0 or F_p > 1 or F_f < 0 or F_f > 1:
        raise ValueError("Fidelities must be in the range [0, 1]")
    if eta < 0 or eta > 1:
        raise ValueError("Channel parameter eta must be in the range [0, 1]")
    if p_m < 0 or p_m > 1:
        raise ValueError("Measurement error probability p_m must be in the range [0, 1]")
    if A < 0 or A > 1 or B < 0 or B > 1 or C < 0 or C > 1:
        raise ValueError("Parameters A, B, C must be in the range [0, 1]")
    L = 1/2
    if noise == False:
        qubit_consumption = 4
        if scenario == 1:
            F_out = F_p * F_f/(F_p + (1 - eta)*(1 - F_p))
            P_succ = F_p + (1 - eta)*(1 - F_p)
        elif scenario == 2:
            F_out = F_p * F_f + (1 - F_p) * (1 - F_f)
            P_succ = 1
        elif scenario == 3:
            F_out = F_p*F_f + A*(1 - F_f)/(F_p + A + (1 - eta)*(B + C))
            P_succ = F_p + A + (1 - eta)*(B + C)
        else:
            raise ValueError("Scenario must be 1, 2, or 3!")
    else:
        s = p_m / 2
        if measurement_purification == False:
            qubit_consumption = 4
            a = (1 - s) * F_f + s * (1 - F_f)
            b = (1 - s) * (1 - F_f) + s * F_f
            if scenario == 1:
                F_out = F_p * a / (a * F_p + b * (1 - eta) * (1 - F_p))
                P_succ = a* F_p + b * (1 - eta) * (1 - F_p)
            elif scenario == 2:
                F_out = F_p * a + (1 - F_p) * b
                P_succ = 1
            elif scenario == 3:
                F_out = (F_p * a + A * b) / (a * F_p + b * A + (1 - eta) * (B + C) * b)
                P_succ = F_p * a + A * b + (1 - eta) * (B + C) * b
            else:
                raise ValueError("Scenario must be 1, 2, or 3!")
        else:
            qubit_consumption = 2 + 2 * n
            r_e, r_o = roll(s,n)
            a = r_e * F_f + r_o * (1 - F_f)
            b = r_e * (1 - F_f) + r_o * F_f
            if n >= 2:
                if scenario == 1:
                    F_out = F_p * a / (a * F_p + b * (1 - eta) * (1 - F_p))
                    P_succ = a* F_p + b * (1 - eta) * (1 - F_p)
                elif scenario == 2:
                    F_out = F_p * a + (1 - F_p) * b
                    P_succ = 1
                elif scenario == 3:
                    F_out = (F_p * a + A * b) / (a * F_p + b * A + (1 - eta) * (B + C) * b)
                    P_succ = F_p * a + A * b + (1 - eta) * (B + C) * b
                else:
                    raise ValueError("Scenario must be 1, 2, or 3!")
            else:
                raise ValueError("Measurement purification requires n >= 2")
    return F_out, P_succ, qubit_consumption, L

def hashing_bound(F_in):
    if F_in < 0.8107 or F_in > 1:
        raise ValueError("Input Error!")
    elif F_in == 0:
        raise ValueError("The fidelity is 0, and it cannot be calculated.")
    elif F_in == 1:
        return 1
    else:
        S = -F_in*np.log2(F_in) - (1 - F_in)*np.log2((1 - F_in)/3)
        E_hash = 1 - S
        return max(0.0, E_hash)
    
def figure(F_range=(0.5, 1), N=2, rounds=3):
    """
    绘制三个协议在 noise=False, measurement_purification=False 时的输出保真度随输入保真度变化的曲线。
    
    参数:
    - F_range: (min, max) 输入保真度范围
    - N: multi_copy_purify 中的副本数
    - rounds: nested_dejmps 中的迭代轮数
    - scenario: hyperentangled_purify 中的场景编号 (1, 2, 3)
    - eta, A, B, C: hyperentangled_purify 的参数
    """
    F_values = np.linspace(F_range[0], F_range[1], 200)

    # 三个协议的结果列表
    multi_out = []
    nested_out = []
    hyper_out_1 = []
    hyper_out_2 = []
    hyper_out_3 = []

    for F_in in F_values:
        Fm, _, _, _ = multi_copy_purify(F_in, N, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fn, _, _, _ = nested_dejmps(F_in, rounds, reset_and_reuse = False, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fh, _, _, _ = hyperentangled_purify(F_in, 1, scenario = 1, eta=0.57, A=0, B=0.3, C=0.2, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fo, _, _, _ = hyperentangled_purify(F_in, 1, scenario = 2, eta=0.57, A=0.5, B=0, C=0, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fp, _, _, _ = hyperentangled_purify(F_in, 1, scenario = 3, eta=0.57, A=0.2, B=0.15, C=0.15, noise = False, measurement_purification = False, p_m = 0.02, n = 1)

        multi_out.append(Fm)
        nested_out.append(Fn)
        hyper_out_1.append(Fh)
        hyper_out_2.append(Fo)
        hyper_out_3.append(Fp)
    
    scenario_1 = 1
    scenario_2 = 2
    scenario_3 = 3

    plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.size': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9})


    plt.figure(figsize=(8, 6),dpi=100)
    plt.plot(F_values, multi_out, linewidth=1, color='mediumaquamarine', label=f"Multi-copy (N={N})")
    plt.plot(F_values, nested_out, linewidth=1, color='lightcoral', label=f"Nested DEJMPS (rounds={rounds})")
    plt.plot(F_values, hyper_out_1, linewidth=1, linestyle='-', color='gold', label=f"Hyperentangled (scenario={scenario_1})")
    plt.plot(F_values, hyper_out_2, linewidth=1, linestyle='-', color='hotpink', label=f"Hyperentangled (scenario={scenario_2})")
    plt.plot(F_values, hyper_out_3, linewidth=1, linestyle='-.', dashes=[5, 3, 1, 3], color='royalblue', label=f"Hyperentangled (scenario={scenario_3})")
    plt.xlabel("Input Fidelity")
    plt.ylabel("Output Fidelity")
    plt.title("Entanglement Purification Protocols (Noise-Free)")
    plt.legend()
    plt.grid(False)
    plt.tick_params(direction='in')
    plt.tight_layout()
    plt.margins(x=0, y=0)
    plt.savefig('figure.png', dpi=300)
    plt.show()




    """if __name__ == "__main__":"""
figure(F_range=(0.5, 1), N=2, rounds=3)