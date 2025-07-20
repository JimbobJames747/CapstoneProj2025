import numpy as np
import matplotlib.pyplot as plt
import math


class SingleLink(l, mu, alpha, det_1_eff, det_2_eff, prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0, verbose=False):
    def __init__(self, l, mu, alpha, det_1_eff, det_2_eff, prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0, verbose=False):
        self.mu = mu
        self.l = l
        self.alpha = alpha
        self.det_1_eff = det_1_eff
        self.prob_dc_per_freq_per_bin_det_1 = prob_dc_per_freq_per_bin_det_1
        self.det_2_eff = det_2_eff
        self.prob_dc_per_freq_per_bin_det_2 = prob_dc_per_freq_per_bin_det_2
        self.verbose = verbose

    def run_single_link(l, mu, alpha, det_1_eff, det_2_eff, prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0, verbose=False):
        # l # distance A-B, divided into N = 2^n EL
        # N num EL links
        # prob_dc_per_freq_per_bin = 0 # prob of detecting dark count per freq Mode per time bin
        # P_emit_1 # prob of generating only 1 pair every T_q seconds 
        # P_emit_2 # prob of generating 2 pairs every T_q seconds
        # alpha  # [db/Km]
        # free running detectors - NO PHOTON NUMBER RESOLUTION
        # det_eff - effeciency of detector

        x = 1
        P_emit_1 = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))
        x = 2
        P_emit_2 = (1 + x) * (((mu / 2)**x) / (1 + mu / 2)**(x + 2))

        if P_emit_1 + P_emit_2 > 1: 
            print("ERROR - P(1) + P(2) + P(0) must be <= 1")
            exit(1)
        
        transm_eta = 10**((-alpha * l) / 2 / 10)


        ### Elementary link 
        total_eff_1 = transm_eta * det_1_eff
        total_eff_2 = transm_eta * det_2_eff


        # P(detector clicks per time bin)
        P_det_clicks_1_pair_det_1 =  (P_emit_1 * total_eff_1) + (prob_dc_per_freq_per_bin_det_1 * (1 - (P_emit_1 * total_eff_1))) # extension of Eq 6

        P_det_clicks_1_pair_det_2 =  (P_emit_1 * total_eff_2) + (prob_dc_per_freq_per_bin_det_1 * (1 - (P_emit_1 * total_eff_1))) # extension of Eq 6

        a = P_emit_1
        b = P_emit_2
        j = prob_dc_per_freq_per_bin_det_1
        k = prob_dc_per_freq_per_bin_det_2
        x = total_eff_1
        y = total_eff_2

        P_both_click_1_pair = (
            a * j * k * x * y
            + a * (-j) * x * y
            - a * k * x * y
            + a * x * y
            - a * j * k * x
            - a * j * k * y
            + a * j * y
            + a * k * x
            + j * k
        )

        
        P_det_clicks_2_pair_det_1 = (
            (P_emit_1 * total_eff_1) + 
            ((1 - P_emit_1 * total_eff_1) * P_emit_2 * total_eff_1) + 
            ((1 - P_emit_1 * total_eff_1) * (1 - P_emit_2 * total_eff_1) * prob_dc_per_freq_per_bin_det_1)
        )

        P_det_clicks_2_pair_det_2 = (
            (P_emit_1 * total_eff_2) + 
            ((1 - P_emit_1 * total_eff_2) * P_emit_2 * total_eff_2) + 
            ((1 - P_emit_1 * total_eff_2) * (1 - P_emit_2 * total_eff_2) * prob_dc_per_freq_per_bin_det_2)
        )
        

        P_both_click_2_pair = (
        a * b * j * k * x**2 * y**2
        - a * b * j * x**2 * y**2
        - a * b * k * x**2 * y**2
        + a * b * x**2 * y**2
        - a * b * j * k * x**2 * y
        - a * b * j * k * x * y**2
        + a * b * j * x**2 * y
        + a * b * j * x * y**2
        + a * b * k * x**2 * y
        + a * b * k * x * y**2
        - a * b * x**2 * y
        - a * b * x * y**2
        + a * j * k * x * y
        - a * j * x * y
        - a * k * x * y
        + a * x * y
        - a * b * j * k * x**2 * y
        - a * b * j * k * x * y**2
        + a * b * j * x**2 * y
        + a * b * j * x * y**2
        + a * b * k * x**2 * y
        + a * b * k * x * y**2
        - a * b * x**2 * y
        - a * b * x * y**2
        + a * b * j * k * x**2
        + 2 * a * b * j * k * x * y
        + a * b * j * k * y**2
        - 2 * a * b * j * x * y
        - a * b * j * y**2
        - a * b * k * x**2
        - 2 * a * b * k * x * y
        + 2 * a * b * x * y
        - a * j * k * x
        - a * j * k * y
        + a * j * y
        + a * k * x
        + b * j * k * x * y
        - b * j * x * y
        - b * k * x * y
        + b * x * y
        - b * j * k * x
        - b * j * k * y
        + b * j * y
        + b * k * x
        + j * k
    )
        


        # P of correct detection sequence from true detections
        # sent and received 2 True AND no DC
        P_true_detection_1_pair = (P_both_click_1_pair * (1 - prob_dc_per_freq_per_bin_det_1) * (1 - prob_dc_per_freq_per_bin_det_2))  # eq 11

        P_true_detection_2_pair = (P_both_click_2_pair * (1 - prob_dc_per_freq_per_bin_det_1) * (1 - prob_dc_per_freq_per_bin_det_2))  # eq 11


        one_minus_both_click_2_pair_squared = (
            -a * b * j * k * x**2 * y**2
            + a * b * j * x**2 * y**2
            + a * b * k * x**2 * y**2
            + a * (-b) * x**2 * y**2
            + a * b * j * k * x**2 * y
            + a * b * j * k * x * y**2
            - a * b * j * x**2 * y
            - a * b * j * x * y**2
            - a * b * k * x**2 * y
            - a * b * k * x * y**2
            + a * b * x**2 * y
            + a * b * x * y**2
            - a * j * k * x * y
            + a * j * x * y
            + a * k * x * y
            - a * x * y
            + a * b * j * k * x**2 * y
            + a * b * j * k * x * y**2
            - a * b * j * x**2 * y
            - a * b * j * x * y**2
            - a * b * k * x**2 * y
            - a * b * k * x * y**2
            + a * b * x**2 * y
            + a * b * x * y**2
            - a * b * j * k * x**2
            - 2 * a * b * j * k * x * y
            - a * b * j * k * y**2
            + 2 * a * b * j * x * y
            + a * b * j * y**2
            + a * b * k * x**2
            + 2 * a * b * k * x * y
            - 2 * a * b * x * y
            + a * j * k * x
            + a * j * k * y
            - a * j * y
            - a * k * x
            - b * j * k * x * y
            + b * j * x * y
            + b * k * x * y
            - b * x * y
            + b * j * k * x
            + b * j * k * y
            - b * j * y
            - b * k * x
            - j * k
            + 1
        )

        one_minus_both_click_1_pair_squared = (
            -a * j * k * x * y
            + a * j * x * y
            + a * k * x * y
            - a * x * y
            + a * j * k * x
            + a * j * k * y
            - a * j * y
            - a * k * x
            - j * k
            + 1
        )
        
        # P of correct detection sequence from false detections
        # lost 1 and detected 1 dark OR lost 2 and detected 2 dark


        P_false_detection_1_pair = (P_det_clicks_1_pair_det_1 * prob_dc_per_freq_per_bin_det_2 * (1 -  P_det_clicks_1_pair_det_1) * (1 - prob_dc_per_freq_per_bin_det_2)) + (P_det_clicks_1_pair_det_2 * prob_dc_per_freq_per_bin_det_1 * (1 -  P_det_clicks_1_pair_det_2) * (1 - prob_dc_per_freq_per_bin_det_1)) + ((prob_dc_per_freq_per_bin_det_1 * prob_dc_per_freq_per_bin_det_2 * one_minus_both_click_1_pair_squared)) # eq 12

        P_false_detection_2_pair = (P_det_clicks_2_pair_det_1 * prob_dc_per_freq_per_bin_det_2 * (1 -  P_det_clicks_2_pair_det_1) * (1 - prob_dc_per_freq_per_bin_det_2)) + (P_det_clicks_2_pair_det_2 * prob_dc_per_freq_per_bin_det_1 * (1 -  P_det_clicks_2_pair_det_2) * (1 - prob_dc_per_freq_per_bin_det_1)) + ((prob_dc_per_freq_per_bin_det_1 * prob_dc_per_freq_per_bin_det_2 * one_minus_both_click_2_pair_squared)) # eq 12 # eq 12

    

        P_all_counts_2_pair = P_true_detection_2_pair + P_false_detection_2_pair # prereq for Eq 3    
        P_all_counts_1_pair = P_true_detection_1_pair + P_false_detection_1_pair

        fidelity = (P_true_detection_1_pair)  / (P_all_counts_2_pair)

        lower_bound_rate = prob_dc_per_freq_per_bin_det_1* prob_dc_per_freq_per_bin_det_2 * (1 - prob_dc_per_freq_per_bin_det_1) * (1 - prob_dc_per_freq_per_bin_det_2)

        #return P_all_counts_2_pair, fidelity
        return P_true_detection_1_pair, fidelity
