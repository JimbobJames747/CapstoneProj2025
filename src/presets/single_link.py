import numpy as np
import matplotlib.pyplot as plt
import math


class SingleLink:
    def __init__(self, source_rep_rate, l, alpha, det_1_eff, det_2_eff, arch, detector_type, mu=.1, prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0, verbose=False):
        self.source_rep_rate = source_rep_rate
        self.mu = mu
        self.l = l
        self.alpha = alpha
        self.det_1_eff = det_1_eff
        self.prob_dc_per_freq_per_bin_det_1 = prob_dc_per_freq_per_bin_det_1
        self.det_2_eff = det_2_eff
        self.detector_type = detector_type
        self.prob_dc_per_freq_per_bin_det_2 = prob_dc_per_freq_per_bin_det_2

        self.arch = arch
        if arch not in ['midpoint', 'source_at_sender']:
            raise ValueError("Invalid architecture specified. Use 'midpoint', 'source_at_sender'.")
        if detector_type not in ['guha', 'PNR', 'non_PNR']:
            raise ValueError("Invalid detector_type specified. Use 'guha', 'PNR', or 'non_PNR'.")
        
        if arch == 'midpoint':
            self.trans_eta = 10**((-alpha * l) / (2 * 1) / 10)
            self.total_eff_1 = self.trans_eta * det_1_eff
            self.total_eff_2 = self.trans_eta * det_2_eff
        elif arch == 'source_at_sender':
            # NOTE: assume source is at Node 1
            self.trans_eta = 10**((-alpha * l) / (1) / 10)
            self.total_eff_1 = det_1_eff
            self.total_eff_2 = self.trans_eta * det_2_eff

        self.total_eff_1 = self.trans_eta * det_1_eff
        self.total_eff_2 = self.trans_eta * det_2_eff
        
        self.verbose = verbose

    def run(self):
        # RETURNS P_ent, ent_distr_rate, fidelity
        if self.detector_type == 'guha':
            return self.run_guha()
        elif self.detector_type == 'PNR':
            return self.run_pnr()
        elif self.detector_type == 'non_PNR':
            return self.run_non_pnr()

    def run_guha(self):
        
        P_click_1 = self.total_eff_1 + ((1-self.total_eff_1) * self.prob_dc_per_freq_per_bin_det_1)
        P_click_2 = self.total_eff_2 + ((1-self.total_eff_2) * self.prob_dc_per_freq_per_bin_det_2)

    
        P_true_click_1 = self.total_eff_1
        P_true_click_2 = self.total_eff_2

    
        true_a = P_true_click_1 * P_true_click_2* (1 - self.prob_dc_per_freq_per_bin_det_1) * (1 - self.prob_dc_per_freq_per_bin_det_2)
    
        a_e = P_click_1 * P_click_2 * (1 - self.prob_dc_per_freq_per_bin_det_1) * (1 - self.prob_dc_per_freq_per_bin_det_2)
    
        b_e = P_click_1 * self.prob_dc_per_freq_per_bin_det_2 * (1 - P_click_2) * (1 - self.prob_dc_per_freq_per_bin_det_1)
        b_e += P_click_2 * self.prob_dc_per_freq_per_bin_det_1 * (1 - P_click_1) * (1 - self.prob_dc_per_freq_per_bin_det_2)

        b_e += self.prob_dc_per_freq_per_bin_det_1 * self.prob_dc_per_freq_per_bin_det_2 * (1 - P_true_click_1) * (1 - P_true_click_2)
        
        fid = true_a / (a_e + b_e)
        return a_e + b_e, self.source_rep_rate * (a_e + b_e), fid
    
    def run_pnr(self):
        P_true_detection_2_pair = 0
        P_false_detection_2_pair = 0
        for x in range(101):
            p_e = (1 + x) * (((self.mu / 2)**x) / (1 + self.mu / 2)**(x + 2))
    
            if x == 0:
                P_true_detection_2_pair += 0
            else:
                P_true_detection_2_pair += p_e * math.comb(x, 1) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) * (1 - (self.prob_dc_per_freq_per_bin_det_1)) * (1 - (self.prob_dc_per_freq_per_bin_det_2))
    
            if x > 1:
                P_false_detection_2_pair += p_e * math.comb(x, 2) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) *  (1 - (self.prob_dc_per_freq_per_bin_det_1)) * (1 - (self.prob_dc_per_freq_per_bin_det_2))
 
                #
                P_false_detection_2_pair_curr = math.comb(x,1) * self.total_eff_1 * (1 - self.total_eff_2)**(x) * (1 - self.prob_dc_per_freq_per_bin_det_1) * (self.prob_dc_per_freq_per_bin_det_2) * (1 - self.prob_dc_per_freq_per_bin_det_2)
                P_false_detection_2_pair_curr += self.total_eff_2 * (1 - self.total_eff_1)**(x) * (1 - self.prob_dc_per_freq_per_bin_det_2) * (self.prob_dc_per_freq_per_bin_det_1) * (1 - self.prob_dc_per_freq_per_bin_det_1) 
                P_false_detection_2_pair += p_e * P_false_detection_2_pair_curr

                #
                P_false_detection_2_pair += (p_e * (1 - self.total_eff_1)**(x) * (1 - self.total_eff_2)**(x) * self.prob_dc_per_freq_per_bin_det_1 * self.prob_dc_per_freq_per_bin_det_2 * (1-self.prob_dc_per_freq_per_bin_det_1) * (1-self.prob_dc_per_freq_per_bin_det_2))
    
    
        P_all_counts_2_pair = P_true_detection_2_pair + P_false_detection_2_pair # prereq for Eq 3    
        
        fidelity = (P_true_detection_2_pair)  / (P_all_counts_2_pair)
        
        return P_all_counts_2_pair, self.source_rep_rate * P_all_counts_2_pair, fidelity
    
    def run_non_pnr(self):
        P_true_detection_2_pair = 0
        P_all_dets = 0
        for x in range(101):
            p_e = (1 + x) * (((self.mu / 2)**x) / (1 + self.mu / 2)**(x + 2))
    
            if x == 0:
                P_true_detection_2_pair_curr = 0
            else:
                P_true_detection_2_pair += p_e * math.comb(x, 1) * self.total_eff_1 * (1 - self.total_eff_1)**(x-1) * self.total_eff_2 * (1 - self.total_eff_2)**(x-1) * (1 - (self.prob_dc_per_freq_per_bin_det_1)) * (1 - (self.prob_dc_per_freq_per_bin_det_2))
    
            P_true_detection_2_pair += P_true_detection_2_pair_curr
    
            prob_detect_at_least_one_1 = (1 - (1 - self.total_eff_1)**x) + (self.prob_dc_per_freq_per_bin_det_1 * (1 - self.total_eff_1)**x)
            prob_detect_at_least_one_2 = (1 - (1 - self.total_eff_2)**x) + (self.prob_dc_per_freq_per_bin_det_2 * (1 - self.total_eff_2)**x)
    
            #prob_one_detection = x * total_eff * (1 - total_eff)**(x - 1)
    
            P_all_dets_curr = prob_detect_at_least_one_1 * prob_detect_at_least_one_2 * (1 - self.prob_dc_per_freq_per_bin_det_1) * (1 - self.prob_dc_per_freq_per_bin_det_2)
            
            P_all_dets += p_e * P_all_dets_curr
    
        fidelity = (P_true_detection_2_pair)  / (P_all_dets)


        return P_all_dets, self.source_rep_rate * P_all_dets, fidelity
