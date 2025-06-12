import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

def calc_elementary_link_success(l, N, m, alpha, eta_e, P_e, P_emission):
    # l # distance A-B, divided into N = 2^n EL
    # N num EL links
    # m # number of ortho frequencies
    # P_e = 0 # prob of detecting dark count per freq Mode per time bin
    # P_emission # prob of generating pair every T_q seconds over M modes
    # alpha  # [db/Km]
    # free running detectors
    # eta_e # effeciency of detector


    transm_eta = 10**((-alpha * l) / (2 * N))

    ### EL BSM
    single_pair_det_prob = P_emission * eta_e * transm_eta
    # prob that det clicks, either photon or dc
    A_e = (single_pair_det_prob) + P_e * (1 - (single_pair_det_prob)) # extension of Eq 6
    # prob at least 1 photon is detected
    B_e = 1 - (1 - P_e) * (1 - (single_pair_det_prob))**2 # extension of Eq 7

    # symmetric detection event (both click) - either both true or both dark
    a_e = (1/8) * ((P_e**2 * (1 - A_e)**2) + (A_e**2 * (1 - P_e)**2)) # eq 11
    # 1 true detection, 1 dark count
    b_e = (1/8) * (2* A_e * P_e * (1 - A_e) * (1 - P_e)) # eq 12
    # classically correlated but not true BS projections 
    c_e = (1/8) * P_e * (1 - P_e) * ((P_e * (1 - B_e)) + (B_e * (1 - P_e))) # eq 13

    s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
    # probability of BSM success for a single frequency 
    P_s0 = 4 * s1 # pg 7 
    # prob of success BSM of at least 1 of M freqs for 1 EL
    P_s1 = 1 - (1 - P_s0)**m # pg 3

    # fidelity calc
    fidelity = math.sqrt(a_e / s1)

    return P_s1, fidelity

if __name__ == '__main__':
    perfect_link_P_s1 = calc_elementary_link_success(l=10, N=1, m=1, alpha=0, eta_e=1, P_e=0, P_emission=1)

    print("Perfect link success probability:", perfect_link_P_s1)

    # iterate over length
    lengths = np.linspace(0, 15, 15) # km 
    single_link_success_ps = []
    single_link_success_ps_nondet = []

    single_link_fid = []
    single_link_fid_nondet = []
    dark_counts = np.linspace(0, 0.1, 15) # km 
    for dc in dark_counts:
        success_p, fid = calc_elementary_link_success(l=10, N=1, m=1, alpha=0.18, eta_e=1, P_e=dc, P_emission=1)
        single_link_fid.append(fid)

        single_link_success_ps_non_det, fid = calc_elementary_link_success(l=10, N=1, m=1, alpha=0.18, eta_e=1, P_e=dc, P_emission=.8)
        single_link_fid_nondet.append(fid)
    
    plt.title("Fidelity")
    plt.xlabel("DC")
    plt.ylabel("Fidelity")
    plt.plot(dark_counts, single_link_fid, label='det')
    plt.plot(dark_counts, single_link_fid_nondet, label='nondet')

    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
    exit(1)

    single_link_fid = []
    single_link_fid_nondet = []
    for length in lengths:
        success_p, fid = calc_elementary_link_success(l=length, N=1, m=1, alpha=0.18, eta_e=1, P_e=0, P_emission=1)
        single_link_success_ps.append(success_p)

        single_link_success_ps_non_det, fid = calc_elementary_link_success(l=length, N=1, m=1, alpha=0.18, eta_e=1, P_e=0, P_emission=.8)
        single_link_success_ps_nondet.append(single_link_success_ps_non_det)

    single_link_nondet_1 = []
    single_link_nondet_5 = []
    single_link_nondet_10 = []
    for length in lengths:
        p, fid = calc_elementary_link_success(l=length, N=1, m=1, alpha=0.18, eta_e=1, P_e=0, P_emission=.8)
        single_link_nondet_1.append(p)

        p, fid = calc_elementary_link_success(l=length, N=1, m=5, alpha=0.18, eta_e=1, P_e=0, P_emission=.8)
        single_link_nondet_5.append(p)

        p, fid = calc_elementary_link_success(l=length, N=1, m=10, alpha=0.18, eta_e=1, P_e=0, P_emission=.8)
        single_link_nondet_10.append(p)
    
    #plt.title("P Success")
    #plt.xlabel("Length")
    #plt.ylabel("P Success")
    #plt.plot(lengths, single_link_nondet_1, label='m=1')
    #plt.plot(lengths, single_link_nondet_5, label='5')
    #plt.plot(lengths, single_link_nondet_10, label='10')


    #plt.grid(True)
    #plt.tight_layout()
    #plt.legend()
    #plt.show()

   

    plt.title("BSM Success, Deterministic source, No Dark Counts")
    plt.xlabel("Link length L [km]")
    plt.ylabel("Probability of EL BSM success")
    plt.plot(lengths, single_link_success_ps, label='det')
    plt.plot(lengths, single_link_success_ps_nondet, label='nondet')

    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
