import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def calc_elementary_link_success(l, N, m, alpha, det_eff, prob_dc_per_freq_per_bin, P_emission, verbose=False):
    # l # distance A-B, divided into N = 2^n EL
    # N num EL links
    # m # number of ortho frequencies
    # prob_dc_per_freq_per_bin = 0 # prob of detecting dark count per freq Mode per time bin
    # P_emission # prob of generating pair every T_q seconds over M modes
    # alpha  # [db/Km]
    # free running detectors
    # det_eff # effeciency of detector
    
    transm_eta = 10**((-alpha * l) / (2 * N) / 10)

    ### Elementary link 
    total_eff = transm_eta * det_eff

    # prob that det clicks, either photon or dc
    A_e = (total_eff) + (prob_dc_per_freq_per_bin * (1 - (total_eff))) # extension of Eq 6
    
    # prob at least 1 photon is detected
    B_e = 1 - ((1 - prob_dc_per_freq_per_bin) * (1 - (P_emission * total_eff))) # extension of Eq 7

    # symmetric detection event (both click) - either both true or both dark
    a_e = ((prob_dc_per_freq_per_bin**2 * P_emission * (1 - A_e)**2) + (P_emission * A_e**2 * (1 - prob_dc_per_freq_per_bin)**2)) # eq 11

    # 1 true detection, 1 dark count
    b_e = (2* A_e * prob_dc_per_freq_per_bin * (1 - (P_emission * A_e)) * (1 - prob_dc_per_freq_per_bin)) # eq 12

    # classically correlated but not true BS projections 
    c_e = prob_dc_per_freq_per_bin * (1 - prob_dc_per_freq_per_bin) * ((prob_dc_per_freq_per_bin * (1 - B_e)) + (B_e * (1 - prob_dc_per_freq_per_bin))) # eq 13

    s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
    

    # we derive accidental probability per time bin
    rep_rate = 5e7 # Hz, 50 MHz
    coinc_window = 1.3e-10 # 130 ps
    coinc_window_factor = coinc_window / (1 / rep_rate)

    # Joshi entanglement lecture: rate of detector clicks at A and B, times coincidence window normalized by time bin
    p_acc = (A_e * A_e * coinc_window_factor) 

    # Guha fidelity equations
    w1 = c_e / (a_e + b_e)

    z = (s1**2 / (a_e + b_e)) * ((1 + 2 * w1) * (1 + 2 * w1))**(-1)

    a1 = 0.5 * (1 + ((a_e - b_e) / (a_e + b_e))) * z
    d1 = (s1 / 4) - (z / 2) * (1 - (1 / 2 * (1 - 2 * w1)) * ((1 - 2 * w1) * (1 - 2 * w1)))

    # account for accidentals
    p_succ_ent_distr = s1 
    p_succ_ent_distr_minus_acc = s1 * (1 - p_acc)


    # we derive fidelity calc from Guha to include/exclude accidental probability
    fidelity = (a1 + d1)  / (s1 + p_acc)
    fidelity_acc_sub = (a1 + d1)  / (s1)

    return p_succ_ent_distr, p_succ_ent_distr_minus_acc, fidelity_acc_sub, fidelity
