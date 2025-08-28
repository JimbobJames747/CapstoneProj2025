import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.special import comb

def run_guha(l, alpha, det_eff, prob_dc_per_freq_per_bin, verbose=False):
    transm_eta = 10**((-alpha * l) / (2 * 1) / 10)
    ### Elementary link
    total_eff = transm_eta * det_eff
    P_click = total_eff + ((1-total_eff) * prob_dc_per_freq_per_bin)

    P_true_click = total_eff

    true_a = P_true_click**2 * (1 - prob_dc_per_freq_per_bin)**2

    a = P_click**2 * (1 - prob_dc_per_freq_per_bin)**2

    b = 2 * P_click * prob_dc_per_freq_per_bin * (1 - P_click) * (1 - prob_dc_per_freq_per_bin)
    b += prob_dc_per_freq_per_bin**2 * (1 - P_click)**2

    #P_true_1 = P_click**2 * (1 - prob_dc_per_freq_per_bin)**2

    fid = true_a / (a + b)
    return true_a, (a + b), fid


def run_pnr(l, mu, alpha, det_eff, prob_dc_per_freq_per_bin, verbose=False):
    transm_eta = 10**((-alpha * l) / (2 * 1) / 10)


    ### Elementary link
    total_eff = transm_eta * det_eff

    P_true_detection_2_pair = 0
    P_false_detection_2_pair = 0
    p_e_sum = 0
    for x in range(101):
        p_e = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))
        if x == 1:
        p_e_sum += p_e

    if x == 0:
        P_true_detection_2_pair += 0
        else:
        P_true_detection_2_pair += p_e * comb(x, 1) * total_eff * (1 - total_eff)**(x-1) * total_eff * (1 - total_eff)**(x-1) * (1 - (prob_dc_per_freq_per_bin))**2

    if x > 1:
        P_false_detection_2_pair += p_e * comb(x, 2) * total_eff * (1 - total_eff)**(x-1) * total_eff * (1 - total_eff)**(x-1) * (1 - (prob_dc_per_freq_per_bin))**2

        P_false_detection_2_pair += (p_e * comb(x,1) * total_eff * (1 - total_eff)**((2 * x) - 1) * prob_dc_per_freq_per_bin * (1-prob_dc_per_freq_per_bin)**2)

        P_false_detection_2_pair += (p_e * (1 - total_eff)**((2 * x)) * prob_dc_per_freq_per_bin**2 * (1-prob_dc_per_freq_per_bin)**2)


    P_all_counts_2_pair = P_true_detection_2_pair + P_false_detection_2_pair # prereq for Eq 3


    #print("P_all_counts_2_pair:", P_all_counts_2_pair)

    fidelity = (P_true_detection_2_pair) / (P_all_counts_2_pair)


    lower_bound_rate = prob_dc_per_freq_per_bin**2 * (1 - prob_dc_per_freq_per_bin)**2

    #return P_all_counts_2_pair, fidelity, lower_bound_rate
    return P_true_detection_2_pair, fidelity, P_all_counts_2_pair, p_e_sum

def run_non_pnr(l, mu, alpha, det_eff, prob_dc_per_freq_per_bin, verbose=False):
    # l # distance A-B, divided into N = 2^n EL
    # N num EL links
    # prob_dc_per_freq_per_bin = 0 # prob of detecting dark count per freq Mode per time bin
    # P_emit_1 # prob of generating only 1 pair every T_q seconds
    # P_emit_2 # prob of generating 2 pairs every T_q seconds
    # alpha # [db/Km]
    # free running detectors - NO PHOTON NUMBER RESOLUTION
    # det_eff - effeciency of detector

    x = 1
    P_emit_1 = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))
    x = 2
    P_emit_2 = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))

    #print("Pe", P_emit_1, P_emit_2)

    if P_emit_1 + P_emit_2 > 1:
        print("ERROR - P(1) + P(2) + P(0) must be <= 1")
        exit(1)
        transm_eta = 10**((-alpha * l) / (2 * 1) / 10)


    ### Elementary link
    transm_eta = 10**((-alpha * l) / (2 * 1) / 10)


    ### Elementary link
    total_eff = transm_eta * det_eff

    #P_false_detection_2_pair = P_emit_2 * paired_detection_p**2
    P_false_detection_2_pair = P_emit_2 * (2**2 - 2) * total_eff * (1 - total_eff)**(2-1) * total_eff * (1 - total_eff)**(2-1)


    P_true_detection_2_pair = 0
    P_all_dets = 0
    p_e_sum = 0
    for x in range(101):
    p_e = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))
    if x > 0:
    p_e_sum += p_e

    if x == 0:
    P_true_detection_2_pair_curr = 0
    else:
    P_true_detection_2_pair_curr = p_e * comb(x, 1) * total_eff * (1 - total_eff)**(x-1) * total_eff * (1 - total_eff)**(x-1) * (1 - (prob_dc_per_freq_per_bin))**2

    P_true_detection_2_pair += P_true_detection_2_pair_curr

    prob_detect_at_least_one = (1 - (1 - total_eff)**x) + (prob_dc_per_freq_per_bin * (1 - total_eff)**x)

    #prob_one_detection = x * total_eff * (1 - total_eff)**(x - 1)

    P_all_dets_curr = prob_detect_at_least_one**2 * (1 - prob_dc_per_freq_per_bin)**2
    P_all_dets += p_e * P_all_dets_curr
    #P_false_detection_2_pair -= P_true_detection_2_pair_curr
    print(P_true_detection_2_pair, P_all_dets)
    #P_false_detection_2_pair += (prob_dc_per_freq_per_bin)**2 * (1 - (prob_dc_per_freq_per_bin))**2

    #P_false_detection_2_pair += (prob_dc_per_freq_per_bin)**2 * (1 - (prob_dc_per_freq_per_bin))**2

    #P_all_counts_2_pair = P_true_detection_2_pair + P_false_detection_2_pair # prereq for Eq 3

    #print("P_all_counts_2_pair:", P_all_counts_2_pair)

    fidelity = (P_true_detection_2_pair) / (P_all_dets)


    lower_bound_rate = prob_dc_per_freq_per_bin**2 * (1 - prob_dc_per_freq_per_bin)**2

    #return P_all_counts_2_pair, fidelity, lower_bound_rate
    return P_true_detection_2_pair, fidelity, P_all_dets, p_e_sum


if __name__ == '__main__':

# iterate over length
lengths = np.linspace(0, 650, 650) # km

a = []
a2 = []
b = []
b2 = []
c = []
c2 = []

a_fid = []
b_fid = []
c_fid = []

mu = .2

prob_dc_per_freq_per_bin = 3e-5
alpha = .2
det_eff = .9
for length in lengths:

p_succ_ent_distr, fidelity, all_p, p_e_sum = run_non_pnr(mu=mu, l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
a.append(p_succ_ent_distr)
a2.append(all_p)
a_fid.append(fidelity)

p_succ_ent_distr, fidelity, all_p, p_e_sum = run_pnr(mu=mu, l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
b.append(p_succ_ent_distr)
b2.append(all_p)
b_fid.append(fidelity)

P_true, P_ent, fidelity = run_guha(l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
c.append(P_true)
c2.append(P_ent)
c_fid.append(fidelity)

v_est = (mu + 2) / (3 * mu + 2)
#v_est = 1 / (1 + mu)

f_est = (1 + 3 * v_est) / 4
#print(f_est)
fig, axs = plt.subplots(2, 2, layout='constrained')

# --- First subplot: Fidelity curves ---
fig.suptitle("Performance Analysis of Source-in-Midpoint Link")
fig.supxlabel(r"$L$ [km]")

axs[0,0].set_title("$\mu = 0.2$")
axs[0,1].set_title("$\mu = 0.1$")

axs[1, 0].plot(lengths, c_fid, color='red', linestyle='-')
axs[1, 0].plot(lengths, b_fid, color='green', linestyle='-')
axs[1, 0].plot(lengths, a_fid, color='blue', linestyle='-')
#axs[1].axhline(y=0.9325, color='black', linestyle='--', label='Est. Min. Fid. with no DC')
axs[1, 0].axhline(y=0.878, color='black', linestyle='--')

#axs[1, 0].set_ylim(.5, 1.02)
axs[1, 0].grid(True)
axs[1, 0].set_ylabel(r"$F_{ent} = P_{T} / P_{ent}$")
#axs[1, 0].set_xticks(np.arange(0, 151, 25)) # Fixed arange to arange
#axs[1, 0].set_yticks(np.arange(.5, 1.02, .1)) # Fixed arange to arange



# --- Second subplot: Additional curves ---
axs[0, 0].plot(lengths, c2, color='red', linestyle='-')
axs[0, 0].plot(lengths, b2, color='green', linestyle='-')
axs[0, 0].plot(lengths, a2, color='blue', linestyle='-')

#axs[0, 0].set_ylim(0, 1.04)
axs[0,0].set_yscale('log')

axs[0, 0].set_ylabel(r"$P_{ent} = P_{T} + P_{F}$")
axs[0, 0].grid(True)
#axs[0, 0].set_xticks(np.arange(0, 151, 25)) # Fixed arange to arange

axs[0, 0].tick_params(labelbottom=False)
axs[1, 0].tick_params(labelbottom=True) # Explicitly show bottom-row ticks
axs[0, 1].tick_params(labelbottom=False) # Explicitly show bottom-row ticks
axs[1, 1].tick_params(labelbottom=True) # Explicitly show bottom-row ticks




a = []
a2 = []
b = []
b2 = []
c = []
c2 = []

a_fid = []
b_fid = []
c_fid = []

mu = .1

prob_dc_per_freq_per_bin = 3e-5
alpha = .2

for length in lengths:

p_succ_ent_distr, fidelity, all_p, p_e_sum = run_non_pnr(mu=mu, l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
a.append(p_succ_ent_distr)
a2.append(all_p)
a_fid.append(fidelity)

p_succ_ent_distr, fidelity, all_p, p_e_sum = run_pnr(mu=mu, l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
b.append(p_succ_ent_distr)
b2.append(all_p)
b_fid.append(fidelity)

P_true, P_ent, fidelity = run_guha(l=length, alpha=alpha, det_eff=det_eff, prob_dc_per_freq_per_bin=prob_dc_per_freq_per_bin)
c.append(P_true)
c2.append(P_ent)
c_fid.append(fidelity)


# --- First subplot: Fidelity curves ---
axs[1, 1].plot(lengths, c_fid, color='red', linestyle='-')
axs[1, 1].plot(lengths, b_fid, color='green', linestyle='-')
axs[1,1 ].plot(lengths, a_fid, color='blue', linestyle='-')
axs[1, 1].axhline(y=0.9325, color='black', linestyle='--', label="Takasue's $F'_{ent}$")

#axs[1,1].set_ylim(.5, 1.02)
axs[1, 1].grid(True)
axs[1, 1].legend()
#axs[1, 1].set_xticks(np.arange(0, 151, 25)) # Fixed arange to arange
#axs[1, 1].set_yticks(np.arange(.5, 1.02, .1)) # Fixed arange to arange



# --- Second subplot: Additional curves ---
axs[0, 1].plot(lengths, c2, color='red', linestyle='-', label=r"$Guha$")
axs[0, 1].plot(lengths, b2, color='green', linestyle='-', label=r"$PNR$")
axs[0, 1].plot(lengths, a2, color='blue', linestyle='-', label=r"$Non-PNR$")

#axs[0, 1].set_ylim(0, 1.04)
axs[0,1].set_yscale('log')

axs[0, 1].grid(True)
axs[0, 1].legend()
#axs[0, 1].set_xticks(np.arange(0, 151, 25)) # Fixed arange to arange

plt.show()