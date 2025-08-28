import numpy as np
import matplotlib.pyplot as plt
import math

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
    N_avg = qubit_consumption / P_succ
    if 0.8107 <= F_out <= 1:
        R = 2 * hashing_bound(F_out) / N_avg
    else:
        R = 0.0
    return F_out, P_succ, qubit_consumption, L, N_avg, R

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
            qubit_consumption = 2*(rounds + 1)
        for _ in range(rounds):
            P = F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2
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
                    P = r_e * (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2) + r_o * (4 * F * (1 - F)/3 + 4 * ((1 - F)/3)**2 )
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
                    P = r_e * (F**2 + (2/3)*F*(1-F) + (5/9)*(1-F)**2) + r_o * (4 * F * (1 - F)/3 + 4 * ((1 - F)/3)**2 )
                    P_total *= P
                    F = (F**2 + (1/9)*(1 - F)**2 + g) / (F**2 + (2/3)*F*(1 - F) + (5/9)*(1 - F)**2 + 4 * g)
                L = (r_e + r_o) / 2 * (r_e - r_o)
                if reset_and_reuse == True:
                    qubit_consumption = 2 * (1 + n) 
                else:
                    qubit_consumption = 2 * (1 + n) * rounds
            else:
                raise ValueError("Noisy measurement purification requires n > 1")
    N_avg = qubit_consumption / P_total
    if 0.8107 <= F <= 1:
        R = 2 * hashing_bound(F) / N_avg
    else:
        R = 0.0
    return F, P_total, qubit_consumption, L, N_avg, R

def hyperentangled_purify(F_p, F_f, scenario, eta=0.57, A=0, B=0.2, C=0.3, noise = False, measurement_purification = False, p_m = 0.02, n = 1):
    total = F_p + A + B + C
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError(f"Parameters F_p, A, B, C must sum to 1 (got {total:.12g})")
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
    N_avg = qubit_consumption / P_succ
    if 0.8107 <= F_out <= 1:
        R = 2 * hashing_bound(F_out) / N_avg
    else:
        R = 0.0
    return F_out, P_succ, qubit_consumption, L, N_avg, R

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
    
def safe_hashing(F):
    try:
        return hashing_bound(F)
    except ValueError:
        return 0.0

def protocol_ebits_per_input(protocol_fn, protocol_args):
    if isinstance(protocol_args, dict):
        F_out, P_succ, qubit_consumption, _, _ = protocol_fn(**protocol_args)
    else:
        F_out, P_succ, qubit_consumption, _, _ = protocol_fn(*protocol_args)
    n_in = qubit_consumption / 2.0
    E_out = safe_hashing(F_out)
    R = 0.0
    if n_in > 0:
        R = P_succ * E_out / n_in
    return R


def figure(F_range=(0.5, 1), N=2, rounds=2,F_values_1=(0.8107, 1)):

    F_values = np.linspace(F_range[0], F_range[1], 200)

    # 三个协议的结果列表
    multi_out = []
    nested_out = []
    hyper_out_1 = []
    hyper_out_2 = []
    hyper_out_3 = []
    multi_out_p = []
    nested_out_p = []
    hyper_out_1_p = []
    hyper_out_2_p = []
    hyper_out_3_p = []
    multi_out_n = []
    nested_out_n = []
    hyper_out_1_n = []
    hyper_out_2_n = []
    hyper_out_3_n = []
    multi_out_h = []
    nested_out_h = []
    hyper_out_1_h = []
    hyper_out_2_h = []
    hyper_out_3_h = []

    for F_in in F_values:
        Fm, Pm, _, _, Nm, _ = multi_copy_purify(F_in, N, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fn, Pn, _, _, Nn, _ = nested_dejmps(F_in, rounds, reset_and_reuse = False, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fh, Ph, _, _, Nh, _ = hyperentangled_purify(F_in, 1, scenario = 1, eta=0.57, A=0, B=0.6*(1-F_in), C=0.4*(1-F_in), noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fo, Po, _, _, No, _ = hyperentangled_purify(F_in, 1, scenario = 2, eta=0.57, A=1-F_in, B=0, C=0, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        Fp, Pp, _, _, Np, _ = hyperentangled_purify(F_in, 1, scenario = 3, eta=0.57, A=0.4*(1-F_in), B=0.3*(1-F_in), C=0.3*(1-F_in), noise = False, measurement_purification = False, p_m = 0.02, n = 1)

        multi_out.append(Fm)
        nested_out.append(Fn)
        hyper_out_1.append(Fh)
        hyper_out_2.append(Fo)
        hyper_out_3.append(Fp)
        multi_out_p.append(Pm)
        nested_out_p.append(Pn)
        hyper_out_1_p.append(Ph)
        hyper_out_2_p.append(Po)
        hyper_out_3_p.append(Pp)
        multi_out_n.append(Nm)
        nested_out_n.append(Nn)
        hyper_out_1_n.append(Nh)
        hyper_out_2_n.append(No)
        hyper_out_3_n.append(Np)


        


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


    plt.figure(figsize=(8, 6),dpi=100)
    plt.plot(F_values, multi_out_p, linewidth=1, color='mediumaquamarine', label=f"Multi-copy (N={N})")
    plt.plot(F_values, nested_out_p, linewidth=1, color='lightcoral', label=f"Nested DEJMPS (rounds={rounds})")
    plt.plot(F_values, hyper_out_1_p, linewidth=1, linestyle='-', color='gold', label=f"Hyperentangled (scenario={scenario_1})")
    plt.plot(F_values, hyper_out_2_p, linewidth=1, linestyle='-', color='hotpink', label=f"Hyperentangled (scenario={scenario_2})")
    plt.plot(F_values, hyper_out_3_p, linewidth=1, linestyle='-', color='royalblue', label=f"Hyperentangled (scenario={scenario_3})")
    plt.xlabel("Input Fidelity")
    plt.ylabel("Probability of success")
    plt.title("Entanglement Purification Protocols (Noise-Free)")
    plt.legend()
    plt.grid(False)
    plt.tick_params(direction='in')
    plt.tight_layout()
    plt.margins(x=0, y=0)
    plt.savefig('figure_p.png', dpi=300)
    plt.show()


    plt.figure(figsize=(8, 6),dpi=100)
    plt.plot(F_values, multi_out_n, linewidth=1, color='mediumaquamarine', label=f"Multi-copy (N={N})")
    plt.plot(F_values, nested_out_n, linewidth=1, color='lightcoral', label=f"Nested DEJMPS (rounds={rounds})")
    plt.plot(F_values, hyper_out_1_n, linewidth=1, linestyle='-', color='gold', label=f"Hyperentangled (scenario={scenario_1})")
    plt.plot(F_values, hyper_out_2_n, linewidth=1, linestyle='-', color='hotpink', label=f"Hyperentangled (scenario={scenario_2})")
    plt.plot(F_values, hyper_out_3_n, linewidth=1, linestyle='-', color='royalblue', label=f"Hyperentangled (scenario={scenario_3})")
    plt.xlabel("Input Fidelity")
    plt.ylabel("Resource consumption")
    plt.title("Entanglement Purification Protocols (Noise-Free)")
    plt.legend()
    plt.grid(False)
    plt.tick_params(direction='in')
    plt.tight_layout()
    plt.margins(x=0, y=0)
    plt.savefig('figure_R.png', dpi=300)
    plt.show()


    F_values_1 = np.linspace(0.8107, 1, 200)

    E_values = []
    for F in F_values_1:
        try:
            E_values.append(hashing_bound(F))
        except ValueError:
            E_values.append(np.nan)

    plt.figure(figsize=(8, 6), dpi=100)
    plt.plot(F_values_1, E_values, color='royalblue', lw=1.2, label='Hashing bound')
    plt.xlabel("Input Fidelity $F_{in}$")
    plt.ylabel("Hashing Bound")
    plt.title("Hashing Bound vs. Input Fidelity")
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.margins(x=0, y=0)
    plt.tick_params(direction='in')
    plt.savefig('hashing_bound.png', dpi=300)
    plt.show()

    F_values_1 = np.linspace(0.8107, 1, 200)

    E_values_1 = []

    for F_in in F_values_1:
        _, _, _, _, _, Rm = multi_copy_purify(F_in, N, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        _, _, _, _, _, Rn = nested_dejmps(F_in, rounds, reset_and_reuse = False, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        _, _, _, _, _, Rh = hyperentangled_purify(F_in, 1, scenario = 1, eta=0.57, A=0, B=0.6*(1-F_in), C=0.4*(1-F_in), noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        _, _, _, _, _, Ro = hyperentangled_purify(F_in, 1, scenario = 2, eta=0.57, A=1-F_in, B=0, C=0, noise = False, measurement_purification = False, p_m = 0.02, n = 1)
        _, _, _, _, _, Rp = hyperentangled_purify(F_in, 1, scenario = 3, eta=0.57, A=0.4*(1-F_in), B=0.3*(1-F_in), C=0.3*(1-F_in), noise = False, measurement_purification = False, p_m = 0.02, n = 1)

        multi_out_h.append(Rm)
        nested_out_h.append(Rn)
        hyper_out_1_h.append(Rh)
        hyper_out_2_h.append(Ro)
        hyper_out_3_h.append(Rp)

        E_values_1.append(hashing_bound(F_in))

    plt.figure(figsize=(8, 6), dpi=100)
    '''plt.plot(F_values_1, E_values_1, color='black', linewidth=1.5, label='Hashing bound')'''
    plt.plot(F_values_1, multi_out_h, linewidth=1, color='mediumaquamarine', label="Multi-copy")
    plt.plot(F_values_1, nested_out_h, linewidth=1, color='lightcoral', label="Nested DEJMPS")
    plt.plot(F_values_1, hyper_out_1_h, linewidth=1, color='gold', label="Hyper (scenario=1)")
    plt.plot(F_values_1, hyper_out_2_h, linewidth=1, color='hotpink', label="Hyper (scenario=2)")
    plt.plot(F_values_1, hyper_out_3_h, linewidth=1, color='royalblue', label="Hyper (scenario=3)")
    plt.xlabel("Input Fidelity")
    plt.ylabel("ebits per input pair")
    plt.title("Protocols vs Hashing Bound")
    plt.legend()
    plt.tick_params(direction='in')
    plt.tight_layout()
    plt.margins(x=0, y=0)
    plt.grid(False)
    plt.savefig('protocols_vs_hashing_bound.png', dpi=300)
    plt.show()


    """if __name__ == "__main__":"""
figure(F_range=(0.5, 1),N=2, rounds=2, F_values_1=(0.8107, 1))
