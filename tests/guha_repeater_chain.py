import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

class RepeaterChain:
    def __init__(self, l, m, alpha, eff_el_bsm_detector, P_el_dc_per_bin_per_freq, P_emission, eff_rep_bsm_detector, P_rep_dc_per_bin_per_freq, eff_loading_emitting_qm, num_elem_links = 1):
        # l # distance A-B, divided into N = 2^n EL
        # N num EL links
        # m # number of ortho frequencies
        # P_el_dc_per_bin_per_freq  # prob of detecting dark count per freq Mode per time bin at EL BSM
        # P_emission # prob of generating pair every T_q seconds over M modes
        # alpha  # [db/Km]
        # free running detectors
        # eff_el_bsm_detector # effeciency of EL BSM detector 
        # eff_rep_bsm_detector - effieciency of repeater BSM detector
        # P_rep_dc_per_bin_per_freq  - prob of detecting dark count per freq Mode per time bin at Repeater BSM
        # eff_loading_emitting_qm: denote the sub-unity efficiency in loading (and re- trieving) the photonic qubit into (and from) the memor- ies, and that of frequency shifting and filtering
        if num_elem_links <= 0:
            print("ERROR: Number of elementary links must be positive.")
            print("Quitting...")
            exit(1)
        if num_elem_links > 1 and num_elem_links % 2 != 0:
            print("ERROR: Number of elementary links must be divisible by 2.")
            print("Quitting...")
            exit(1)

        self.num_elem_links = num_elem_links # N 
        self.n = int(math.log2(self.num_elem_links))
        
        self.l = l 
        self.m = m 
        self.alpha = alpha 
        self.eff_el_bsm_detector = eff_el_bsm_detector 
        self.P_el_dc_per_bin_per_freq = P_el_dc_per_bin_per_freq 
        self.P_emission = P_emission 

        self.eff_loading_emitting_qm = eff_loading_emitting_qm
        self.eff_rep_bsm_detector = eff_rep_bsm_detector
        self.P_rep_dc_per_bin_per_freq = P_rep_dc_per_bin_per_freq

        self.transm_eta = None

        self.s = None
        self.P_succ = None

        # prob that det clicks, either photon or dc
        A_r = (self.eff_loading_emitting_qm * self.eff_rep_bsm_detector) + self.P_rep_dc_per_bin_per_freq * (1 - (self.eff_loading_emitting_qm * self.eff_rep_bsm_detector)) # extension of Eq 6
        
        # prob at least 1 photon is detected
        B_r = 1 - (1 - self.P_rep_dc_per_bin_per_freq) * (1 - (self.eff_loading_emitting_qm * self.eff_rep_bsm_detector))**2 # extension of Eq 7 

        # eq 11 - symmetric detection event (both click) - either both true or both dark
        self.a = (1/8) * ((self.P_rep_dc_per_bin_per_freq**2 * (1 - A_r)**2) + (A_r**2 * (1 - self.P_rep_dc_per_bin_per_freq)**2))
        
        # eq 12 - 1 true detection, 1 dark count
        self.b = (1/8) * (2* A_r * self.P_rep_dc_per_bin_per_freq * (1 - A_r) * (1 - self.P_rep_dc_per_bin_per_freq)) # eq 12

        # eq 13 - classically correlated but not true BS projections 
        self.c = (1/8) * self.P_rep_dc_per_bin_per_freq * (1 - self.P_rep_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - B_r)) + (B_r * (1 - self.P_rep_dc_per_bin_per_freq))) 

        self.s = self.a + self.b + 2 * self.c


    def calc_ent_distr_succ(self):
        # calc probability of success (P_succ eq 3) that entanglement is successfull distributed and swapped across the whole chain 
     
        ### calculate first elementary link
        self.transm_eta = 10**((-self.alpha * self.l) / (2 * self.num_elem_links))

        ### EL BSM
        single_pair_det_prob = self.P_emission * self.eff_el_bsm_detector * self.transm_eta
        # prob that det clicks, either photon or dc
        A_e = (single_pair_det_prob) + self.P_el_dc_per_bin_per_freq * (1 - (single_pair_det_prob)) # extension of Eq 6

        # prob at least 1 photon is detected
        B_e = 1 - (1 - self.P_el_dc_per_bin_per_freq) * (1 - (single_pair_det_prob))**2 # extension of Eq 7

        # symmetric detection event (both click) - either both true or both dark
        a_e = (1/8) * ((self.P_el_dc_per_bin_per_freq**2 * (1 - A_e)**2) + (A_e**2 * (1 - self.P_el_dc_per_bin_per_freq)**2)) # eq 11
        # 1 true detection, 1 dark count
        b_e = (1/8) * (2* A_e * self.P_el_dc_per_bin_per_freq * (1 - A_e) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12
        # classically correlated but not true BS projections 
        c_e = (1/8) * self.P_el_dc_per_bin_per_freq * (1 - self.P_el_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - B_e)) + (B_e * (1 - self.P_el_dc_per_bin_per_freq))) # eq 13

        s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
        # probability of BSM success for a single frequency 
        P_s0 = 4 * s1 # pg 7 
         
        if self.num_elem_links == 1:
            # prob of success BSM of at least 1 of M freqs for 1 EL
            self.P_succ = 1 - (1 - P_s0)**self.m # pg 3
        else:
            Ps = 4 * self.s
            Ps1 = 1 - (1 - 4 * s1)**self.m
            self.P_succ = (Ps ** (self.num_elem_links - 1)) * (Ps1 ** self.num_elem_links)

        print("P_succ with ", self.num_elem_links, " EL:", self.P_succ)


if __name__ == '__main__':
    # perfect scales as
    # p_succ where s and s1 = .125
    rc_perfect = RepeaterChain(l=10, m=4, alpha=0, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links = 4)

    rc_perfect.calc_ent_distr_succ()

    rc_succs = []
    rc_succs_2 = []
    rc_succs_4 = []
    rc_succs_8 = []
    rc_succs_16 = []


    lengths = np.linspace(0, 1000, 1000) # km 
    alpha = .15
    m = 1000
    P_el_dc_per_bin_per_freq = 3e-5
    for length in lengths:
        rc = RepeaterChain(l=length, m=m, alpha=alpha, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links =1)
        rc.calc_ent_distr_succ()

        rc_succs.append(rc.P_succ)

        rc = RepeaterChain(l=length, m=m, alpha=alpha, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links =2)
        rc.calc_ent_distr_succ()

        rc_succs_2.append(rc.P_succ)

        rc = RepeaterChain(l=length, m=m, alpha=alpha, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links =4)
        rc.calc_ent_distr_succ()

        rc_succs_4.append(rc.P_succ)

        rc = RepeaterChain(l=length, m=m, alpha=.18, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links =8)
        rc.calc_ent_distr_succ()

        rc_succs_8.append(rc.P_succ)

        rc = RepeaterChain(l=length, m=m, alpha=.18, eff_el_bsm_detector=1, P_el_dc_per_bin_per_freq=0, P_emission=1, eff_rep_bsm_detector=1, P_rep_dc_per_bin_per_freq=0, eff_loading_emitting_qm=1, num_elem_links =16)
        rc.calc_ent_distr_succ()

        rc_succs_16.append(rc.P_succ)
    
    plt.xlabel("Length")
    plt.ylabel("Log(P Succ)")
    plt.yscale('log')  # Set y-axis to log base 10

    plt.plot(lengths, rc_succs, label='1')
    plt.plot(lengths, rc_succs_2, label='2')
    plt.plot(lengths, rc_succs_4, label='4')
    plt.plot(lengths, rc_succs_8, label='8')
    plt.plot(lengths, rc_succs_16, label='16')




    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()


