import numpy as np
import matplotlib.pyplot as plt
import math
 
class RepeaterChain:
    def __init__(self, source_rep_rate, detector_type, l, m, alpha, eff_el_bsm_detector_1, eff_el_bsm_detector_2, P_el_dc_per_bin_per_freq, eff_rep_bsm_detector_1,
                 eff_rep_bsm_detector_2, P_rep_dc_per_bin_per_freq, eff_loading_qm, eff_emitting_qm, mu=.1, num_elem_links = 1):
        # l # distance A-B, divided into N = 2^n EL
        # N num EL links
        # m # number of ortho frequencies
        # P_el_dc_per_bin_per_freq  # prob of detecting dark count per freq Mode per time bin at EL BSM
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

        self.detector_type = detector_type

        if detector_type not in ['guha', 'PNR', 'non_PNR']:
            raise ValueError("Invalid detector_type specified. Use 'guha', 'PNR', or 'non_PNR'.")
        self.mu = mu
        self.source_rep_rate = source_rep_rate

        self.num_elem_links = num_elem_links # N
        self.n = int(math.log2(self.num_elem_links))
        
        self.l = l
        self.m = m
        self.alpha = alpha

        self.eff_el_bsm_detector_1 = eff_el_bsm_detector_1
        self.eff_el_bsm_detector_2 = eff_el_bsm_detector_2

        # Note: these must be equal for math to work out
        self.P_el_dc_per_bin_per_freq = P_el_dc_per_bin_per_freq

        
        self.eff_rep_bsm_detector_1 = eff_rep_bsm_detector_1
        self.eff_rep_bsm_detector_2 = eff_rep_bsm_detector_2

        # Note: these must be equal for math to work out
        self.P_rep_dc_per_bin_per_freq = P_rep_dc_per_bin_per_freq

        self.eff_loading_qm = eff_loading_qm
        self.eff_emitting_qm = eff_emitting_qm

        self.transm_eta = 10**((-self.alpha * self.l) / (2 * self.num_elem_links) / 10)
        self.total_eff_1 = self.eff_el_bsm_detector_1 * self.transm_eta
        self.total_eff_2 = self.eff_el_bsm_detector_2 * self.transm_eta
 
        self.s = None
        self.P_succ = None
 
        self.fidelity = None
 
        ############# Repeater BSM calculations
        # prob that det clicks, either photon or dc
        self.single_pair_det_prob_r_1 = self.eff_rep_bsm_detector_1 * self.eff_emitting_qm
        self.single_pair_det_prob_r_2 = self.eff_rep_bsm_detector_2 * self.eff_emitting_qm
 
        self.A_r_true_1 = self.single_pair_det_prob_r_1
        self.A_r_true_2 = self.single_pair_det_prob_r_2
 
        self.A_r_1 = self.single_pair_det_prob_r_1 + self.P_rep_dc_per_bin_per_freq * (1 - (self.P_rep_dc_per_bin_per_freq)) # extension of Eq 6
        self.A_r_2 = self.single_pair_det_prob_r_2 + self.P_rep_dc_per_bin_per_freq * (1 - (self.P_rep_dc_per_bin_per_freq)) # extension of Eq 6
        
        # prob at least 1 photon is detected
        self.B_r = 1 - (1 - self.P_rep_dc_per_bin_per_freq) * ((1 - (self.eff_emitting_qm * self.eff_rep_bsm_detector_1)) * (1 - (self.eff_emitting_qm * self.eff_rep_bsm_detector_2))) # extension of Eq 7
 
        # eq 11 - symmetric detection event (both click) - either both true or both dark
        self.a = (1/8) * (self.A_r_true_1 * self.A_r_true_2 * (1 - self.P_rep_dc_per_bin_per_freq) * (1 - self.P_rep_dc_per_bin_per_freq))
        
        # eq 12 - 1 true detection, 1 dark count
        self.b = (1/8) * self.A_r_1 * self.P_rep_dc_per_bin_per_freq * (1 - self.A_r_2) * (1 - self.P_rep_dc_per_bin_per_freq)
        self.b += (1/8) *self.A_r_2 * self.P_rep_dc_per_bin_per_freq * (1 - self.A_r_1) * (1 - self.P_rep_dc_per_bin_per_freq)

        self.b += (1/8) * self.P_rep_dc_per_bin_per_freq * self.P_rep_dc_per_bin_per_freq * (1 - self.A_r_1) * (1 - self.A_r_2)

        # eq 13 - classically correlated but not true BS projections
        self.c = (1/8) * self.P_rep_dc_per_bin_per_freq * (1 - self.P_rep_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - self.B_r)) + (self.B_r * (1 - self.P_rep_dc_per_bin_per_freq)))
 
        self.s = self.a + self.b + 2 * self.c

    def run(self):
        # RETURNS P_ent, ent_distr_rate, fidelity
        if self.detector_type == 'guha':
            return self.run_guha()
        elif self.detector_type == 'PNR':
            return self.run_pnr()
        elif self.detector_type == 'non_PNR':
            return self.run_non_pnr()
        
    def run_pnr(self):
        true_2_pair_1 = 0
        true_2_pair_2 = 0
        false_2_pair_1 = 0
        false_2_pair_2 = 0
        for x in range(101):
            p_e = (1 + x) * (((self.mu / 2)**x) / (1 + self.mu / 2)**(x + 2))
            if x > 0:
                true_2_pair_1 += p_e * math.comb(x, 1) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * self.eff_loading_qm * (1 - self.eff_loading_qm)**(x-1)
                true_2_pair_2 += p_e * math.comb(x, 1) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) * self.eff_loading_qm * (1 - self.eff_loading_qm)**(x-1)
 
                prob_at_least_one_storage = (1 - (1 - self.eff_loading_qm)**(x))
 
                false_2_pair_1 += p_e * math.comb(x, 2) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * prob_at_least_one_storage
                false_2_pair_2 += p_e * math.comb(x, 2) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) * prob_at_least_one_storage

                false_2_pair_1 += (p_e * (1 - self.total_eff_1)**(x) * self.P_el_dc_per_bin_per_freq * prob_at_least_one_storage)

                false_2_pair_2 += (p_e * (1 - self.total_eff_2)**(x) * self.P_el_dc_per_bin_per_freq * prob_at_least_one_storage)
             
        
 
        A_e_true_1 = true_2_pair_1 
        A_e_true_2 = true_2_pair_2

        p_click_1 = A_e_true_1 + false_2_pair_1 
        p_click_2 = A_e_true_2 + false_2_pair_2

        A_e_1 = p_click_1 
        A_e_2 = p_click_2 

        A_e_false_1 = A_e_1 - A_e_true_1
        A_e_false_2 = A_e_2 - A_e_true_2

        B_e = 1 - (1 - self.P_el_dc_per_bin_per_freq) * ((1 - p_click_1) * (1 - p_click_2))
 
        # symmetric detection event (both click) - either both true or both dark
        a_e = (1/8) * (A_e_true_1 * A_e_true_2 * (1 - self.P_el_dc_per_bin_per_freq)**2) # eq 11
 
        # 1 true detection, 1 dark count
        b_e = (1/8) * (A_e_1 * self.P_el_dc_per_bin_per_freq * (1 - A_e_2) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12
        b_e += (1/8) * (A_e_2 * self.P_el_dc_per_bin_per_freq * (1 - A_e_1) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12

        b_e += (1/8) * (self.P_el_dc_per_bin_per_freq**2 * (1 - A_e_1) * (1 - A_e_2)) # eq 12
        b_e += (1/8) * (A_e_false_1 * A_e_false_2 * (1 - self.P_el_dc_per_bin_per_freq)**2) # eq 11
 
 
        # classically correlated but not true BS projections
        c_e = (1/8) * self.P_el_dc_per_bin_per_freq * (1 - self.P_el_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - B_e)) + (B_e * (1 - self.P_el_dc_per_bin_per_freq))) # eq 13
 
 
        s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
        # probability of BSM success for a single frequency
         
        if self.num_elem_links == 1:
            P_s0 = 4 * s1 # pg 7
            # prob of success BSM of at least 1 of M freqs for 1 EL
            self.P_succ = 1 - (1 - P_s0)**self.m # pg 3
        else:
            Ps_i = 4 * self.s # repeater
            Ps1 = 1 - (1 - 4 * s1)**self.m # EL
            self.P_succ = (Ps_i ** (self.num_elem_links - 1)) * (Ps1 ** self.num_elem_links)
 
        w1 = c_e / (a_e + b_e)
        w_r = self.c / (self.a + self.b)
 
        i = self.n +1
 
        if i == 1:
            z_i = a_e + b_e
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
        elif i > 1:
            z_i = (self.s**2 / (self.a + self.b)) * (1 / ((1 + 2 * w1) * (1 + 2 * w_r)))**(2**(i-1))
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
 
        if i == 1:
            self.fidelity = a_i / s1
        else:
            self.fidelity = a_i / self.s

        return self.P_succ, self.source_rep_rate * self.P_succ, self.fidelity

        

    def run_non_pnr(self):
        true_2_pair_1 = 0
        true_2_pair_2 = 0
        p_all_detections_1 = 0
        p_all_detections_2 = 0
        for x in range(101):
            p_e = (1 + x) * (((self.mu / 2)**x) / (1 + self.mu / 2)**(x + 2))
            if x > 0:
                true_2_pair_1 += p_e * math.comb(x, 1) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * self.eff_loading_qm * (1 - self.eff_loading_qm)**(x-1)
                true_2_pair_2 += p_e * math.comb(x, 1) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) * self.eff_loading_qm * (1 - self.eff_loading_qm)**(x-1)
 
                prob_at_least_one_storage = (1 - (1 - self.eff_loading_qm)**(x))
                prob_at_least_one_detection_1 = (1 - (1 - self.total_eff_1)**(x)) + ((1 - self.total_eff_1)**x * self.P_el_dc_per_bin_per_freq)
                prob_at_least_one_detection_2 = (1 - (1 - self.total_eff_2)**(x)) + ((1 - self.total_eff_2)**x * self.P_el_dc_per_bin_per_freq)
 
                p_all_detections_1 += p_e * prob_at_least_one_detection_1 * prob_at_least_one_storage
                p_all_detections_2 += p_e * prob_at_least_one_detection_2 * prob_at_least_one_storage
        
 
        A_e_true_1 = true_2_pair_1 
        A_e_true_2 = true_2_pair_2

        p_click_1 = p_all_detections_1 
        p_click_2 = p_all_detections_2

        A_e_1 = p_click_1 
        A_e_2 = p_click_2

        A_e_false_1 = A_e_1 - A_e_true_1
        A_e_false_2 = A_e_2 - A_e_true_2

        B_e = 1 - (1 - self.P_el_dc_per_bin_per_freq) * ((1 - p_click_1) * (1 - p_click_2))
 
        # symmetric detection event (both click) - either both true or both dark
        a_e = (1/8) * (A_e_true_1 * A_e_true_2 * (1 - self.P_el_dc_per_bin_per_freq)**2) # eq 11
 
        # 1 true detection, 1 dark count
        b_e = (1/8) * (A_e_1 * self.P_el_dc_per_bin_per_freq * (1 - A_e_2) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12
        b_e += (1/8) * (A_e_2 * self.P_el_dc_per_bin_per_freq * (1 - A_e_1) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12

        b_e += (1/8) * (self.P_el_dc_per_bin_per_freq**2 * (1 - A_e_1) * (1 - A_e_2)) # eq 12
        b_e += (1/8) * (A_e_false_1 * A_e_false_2 * (1 - self.P_el_dc_per_bin_per_freq)**2) # eq 11
 
 
        # classically correlated but not true BS projections
        c_e = (1/8) * self.P_el_dc_per_bin_per_freq * (1 - self.P_el_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - B_e)) + (B_e * (1 - self.P_el_dc_per_bin_per_freq))) # eq 13
 
 
        s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
        # probability of BSM success for a single frequency
         
        if self.num_elem_links == 1:
            P_s0 = 4 * s1 # pg 7
            # prob of success BSM of at least 1 of M freqs for 1 EL
            self.P_succ = 1 - (1 - P_s0)**self.m # pg 3
        else:
            Ps_i = 4 * self.s # repeater
            Ps1 = 1 - (1 - 4 * s1)**self.m # EL
            self.P_succ = (Ps_i ** (self.num_elem_links - 1)) * (Ps1 ** self.num_elem_links)
 
        w1 = c_e / (a_e + b_e)
        w_r = self.c / (self.a + self.b)
 
        i = self.n +1
 
        if i == 1:
            z_i = a_e + b_e
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
        elif i > 1:
            z_i = (self.s**2 / (self.a + self.b)) * (1 / ((1 + 2 * w1) * (1 + 2 * w_r)))**(2**(i-1))
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
 
        if i == 1:
            self.fidelity = a_i / s1
        else:
            self.fidelity = a_i / self.s

        return self.P_succ, self.source_rep_rate * self.P_succ, self.fidelity
    
    def run_guha(self):
        
        P_click_1 = self.total_eff_1 + ((1-self.total_eff_1) * self.P_el_dc_per_bin_per_freq)
        P_click_2 = self.total_eff_2 + ((1-self.total_eff_2) * self.P_el_dc_per_bin_per_freq)

    
        P_true_click_1 = self.total_eff_1
        P_true_click_2 = self.total_eff_2

        A_e_true_1 = P_true_click_1
        A_e_true_2 = P_true_click_2

        A_e_1 = P_click_1 + (self.P_el_dc_per_bin_per_freq * (1 - P_click_1))
        A_e_2 = P_click_2 + (self.P_el_dc_per_bin_per_freq * (1 - P_click_2))

        B_e = 1 - (1 - self.P_el_dc_per_bin_per_freq) * ((1 - P_true_click_1) * (1 - P_true_click_2))

        
        # symmetric detection event (both click) - either both true or both dark
        a_e = (1/8) * (A_e_true_1 * A_e_true_2 * (1 - self.P_el_dc_per_bin_per_freq)**2) # eq 11
 
        # 1 true detection, 1 dark count
        b_e = (1/8) * (A_e_1 * self.P_el_dc_per_bin_per_freq * (1 - A_e_2) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12
        b_e += (1/8) * (A_e_2 * self.P_el_dc_per_bin_per_freq * (1 - A_e_1) * (1 - self.P_el_dc_per_bin_per_freq)) # eq 12

        b_e += (1/8) * (self.P_el_dc_per_bin_per_freq**2 * (1 - A_e_1) * (1 - A_e_2)) # eq 12
 
 
        # classically correlated but not true BS projections
        c_e = (1/8) * self.P_el_dc_per_bin_per_freq * (1 - self.P_el_dc_per_bin_per_freq) * ((self.P_el_dc_per_bin_per_freq * (1 - B_e)) + (B_e * (1 - self.P_el_dc_per_bin_per_freq))) # eq 13
 
 
        s1 = a_e + b_e + 2 * c_e # prereq for Eq 3
        # probability of BSM success for a single frequency
         
        if self.num_elem_links == 1:
            P_s0 = 4 * s1 # pg 7
            # prob of success BSM of at least 1 of M freqs for 1 EL
            self.P_succ = 1 - (1 - P_s0)**self.m # pg 3
        else:
            Ps_i = 4 * self.s # repeater
            Ps1 = 1 - (1 - 4 * s1)**self.m # EL
            self.P_succ = (Ps_i ** (self.num_elem_links - 1)) * (Ps1 ** self.num_elem_links)
 
        w1 = c_e / (a_e + b_e)
        w_r = self.c / (self.a + self.b)
 
        i = self.n +1
 
        if i == 1:
            z_i = a_e + b_e
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
        elif i > 1:
            z_i = (self.s**2 / (self.a + self.b)) * (1 / ((1 + 2 * w1) * (1 + 2 * w_r)))**(2**(i-1))
            a_i = 0.5 * (1 + ((self.a - self.b) / (self.a + self.b))**(i-1) * ((a_e - b_e) / (a_e + b_e))) * z_i
 
        if i == 1:
            self.fidelity = a_i / s1
        else:
            self.fidelity = a_i / self.s

        return self.P_succ, self.source_rep_rate * self.P_succ, self.fidelity
 


if __name__ == "__main__":
    # repeater tests with Perfect memory. only efficiency loading and emitting qubits is simulated

    a_succ = []
    b_succ = []
    c_succ = []

    a_fid = []
    b_fid = []
    c_fid = []

    source_rep_rate = 50 # MHz
    
    # mess with m to show its necessary, m =1 is bad
    m = 1000 # number of ortho frequencies
    alpha = .2
    eff_el_bsm_detector_1 = 1
    eff_el_bsm_detector_2 = 1
    P_el_dc_per_bin_per_freq = 0

    eff_rep_bsm_detector_1 = 1
    eff_rep_bsm_detector_2 = 1
    P_rep_dc_per_bin_per_freq = 0
    
    # maybe look at? but not too interesting
    eff_loading_qm = 1
    eff_emitting_qm = 1
    
    # probably don't look at, cause jake does in his section
    mu= .1
    
    lengths = np.linspace(0, 2000, 1000)  # km

    for l in lengths:
        rep_a = RepeaterChain(
            source_rep_rate=source_rep_rate,
            detector_type='PNR', # look at these
            l=l,
            m=m,
            alpha=alpha,
            eff_el_bsm_detector_1=eff_el_bsm_detector_1,
            eff_el_bsm_detector_2=eff_el_bsm_detector_2,
            P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
            eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
            eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
            P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
            eff_loading_qm=eff_loading_qm,
            eff_emitting_qm=eff_emitting_qm,
            mu=mu,
            num_elem_links=1 # and this
            )
        a_succ.append(rep_a.run()[1])
        a_fid.append(rep_a.run()[2])

        rep_a = RepeaterChain(
            source_rep_rate=source_rep_rate,
            detector_type='non_PNR',
            l=l,
            m=m,
            alpha=alpha,
            eff_el_bsm_detector_1=eff_el_bsm_detector_1,
            eff_el_bsm_detector_2=eff_el_bsm_detector_2,
            P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
            eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
            eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
            P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
            eff_loading_qm=eff_loading_qm,
            eff_emitting_qm=eff_emitting_qm,
            mu=mu,
            num_elem_links=2
            )
        b_succ.append(rep_a.run()[1])
        b_fid.append(rep_a.run()[2])

        rep_a = RepeaterChain(
            source_rep_rate=source_rep_rate,
            detector_type='guha',
            l=l,
            m=m,
            alpha=alpha,
            eff_el_bsm_detector_1=eff_el_bsm_detector_1,
            eff_el_bsm_detector_2=eff_el_bsm_detector_2,
            P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
            eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
            eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
            P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
            eff_loading_qm=eff_loading_qm,
            eff_emitting_qm=eff_emitting_qm,
            mu=mu,
            num_elem_links=4
            )
        c_succ.append(rep_a.run()[1])
        c_fid.append(rep_a.run()[2])

    plt.figure(figsize=(10, 5))
    plt.plot(lengths, a_succ, label='1', color='blue')
    plt.plot(lengths, b_succ, label='2', color='orange')
    plt.plot(lengths, c_succ, label='3', color='green')
    plt.xlabel('Distance (km)')

    plt.ylabel('Success Rate (MHz)') 
    plt.yscale('log')
    plt.legend()
    plt.grid()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(lengths, a_fid, label='1', color='blue')
    plt.plot(lengths, b_fid, label='2', color='orange')
    plt.plot(lengths, c_fid, label='3', color='green')
    plt.xlabel('Distance (km)')     
    plt.ylabel('Fidelity')
    plt.legend()
    plt.grid()
    plt.show()
