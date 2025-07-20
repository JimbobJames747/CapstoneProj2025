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
        total_eff = transm_eta * det_eff

        # P(detector clicks per time bin)
        P_det_clicks_1_pair =  (P_emit_1 * total_eff) + (prob_dc_per_freq_per_bin * (1 - (P_emit_1 * total_eff))) # extension of Eq 6

        P_det_clicks_1_pair_squared = (
            prob_dc_per_freq_per_bin**2 * P_emit_1 * total_eff**2
                - 2 * prob_dc_per_freq_per_bin**2 * P_emit_1 * total_eff
                + prob_dc_per_freq_per_bin**2
                - 2 * prob_dc_per_freq_per_bin * P_emit_1 * total_eff**2
                + 2 * prob_dc_per_freq_per_bin * P_emit_1 * total_eff
                + P_emit_1 * total_eff**2
        ) # extension of Eq 6

        
        P_det_clicks_2_pair = (
            (P_emit_1 * total_eff) + 
            ((1 - P_emit_1 * total_eff) * P_emit_2 * total_eff) + 
            ((1 - P_emit_1 * total_eff) * (1 - P_emit_2 * total_eff) * prob_dc_per_freq_per_bin)
        )
        
        a = P_emit_1
        b = P_emit_2
        c = prob_dc_per_freq_per_bin
        x = total_eff

        P_det_clicks_2_pair_squared = (
            a * b * c**2 * x**4
            - 2 * a * b * c * x**4
            + a * b * x**4
            - 2 * a * b * c**2 * x**3
            + 4 * a * b * c * x**3
            - 2 * a * b * x**3
            + a * c**2 * x**2
            - 2 * a * c * x**2
            + a * x**2
            - 2 * a * b * c**2 * x**3
            + 4 * a * b * c * x**3
            - 2 * a * b * x**3
            + 4 * a * b * c**2 * x**2
            - 6 * a * b * c * x**2
            + 2 * a * b * x**2
            - 2 * a * c**2 * x
            + 2 * a * c * x
            + b * c**2 * x**2
            - 2 * b * c * x**2
            + b * x**2
            - 2 * b * c**2 * x
            + 2 * b * c * x
            + c**2
        )
        


        # P of correct detection sequence from true detections
        # sent and received 2 True AND no DC
        P_true_detection_1_pair = ((P_det_clicks_1_pair_squared * (1 - prob_dc_per_freq_per_bin)**2))  # eq 11
        P_true_detection_2_pair = ((P_det_clicks_2_pair_squared * (1 - prob_dc_per_freq_per_bin)**2))  # eq 11


        one_minus_prob_detection_1_pair_sq = (P_emit_1 * total_eff**2 * prob_dc_per_freq_per_bin**2) - (2 * P_emit_1 * total_eff**2 * prob_dc_per_freq_per_bin) + (P_emit_1 * total_eff**2) - (2 * P_emit_1 * total_eff * prob_dc_per_freq_per_bin**2) + (4 * P_emit_1 * total_eff * prob_dc_per_freq_per_bin) - (2 * P_emit_1 * total_eff) + (prob_dc_per_freq_per_bin**2) - (2 * prob_dc_per_freq_per_bin) + 1

        one_minus_prob_detection_2_pair_sq = (
                a * b * c**2 * x**4
                - 2 * a * b * c * x**4
                + a * b * x**4
                - 2 * a * b * c**2 * x**3
                + 4 * a * b * c * x**3
                - 2 * a * b * x**3
                + a * c**2 * x**2
                - 2 * a * c * x**2
                + a * x**2
                - 2 * a * b * c**2 * x**3
                + 4 * a * b * c * x**3
                - 2 * a * b * x**3
                + 4 * a * b * c**2 * x**2
                - 8 * a * b * c * x**2
                + 4 * a * b * x**2
                - 2 * a * c**2 * x
                + 4 * a * c * x
                - 2 * a * x
                + b * c**2 * x**2
                - 2 * b * c * x**2
                + b * x**2
                - 2 * b * c**2 * x
                + 4 * b * c * x
                - 2 * b * x
                + c**2
                - 2 * c
                + 1
            )
        
        # P of correct detection sequence from false detections
        # lost 1 and detected 1 dark OR lost 2 and detected 2 dark
        P_false_detection_1_pair = (2 * P_det_clicks_1_pair * prob_dc_per_freq_per_bin * (1 -  P_det_clicks_1_pair) * (1 - prob_dc_per_freq_per_bin)) + ((prob_dc_per_freq_per_bin**2 * one_minus_prob_detection_1_pair_sq)) # eq 12

        P_false_detection_2_pair = (2 * P_det_clicks_2_pair * prob_dc_per_freq_per_bin * (1 -  P_det_clicks_2_pair) * (1 - prob_dc_per_freq_per_bin)) + ((prob_dc_per_freq_per_bin**2 * one_minus_prob_detection_2_pair_sq)) # eq 12

    

        P_all_counts_2_pair = P_true_detection_2_pair + P_false_detection_2_pair # prereq for Eq 3    
        P_all_counts_1_pair = P_true_detection_1_pair + P_false_detection_1_pair

        fidelity = (P_true_detection_1_pair)  / (P_all_counts_2_pair)

        lower_bound_rate = prob_dc_per_freq_per_bin**2 * (1 - prob_dc_per_freq_per_bin)**2

        #return P_all_counts_2_pair, fidelity
        return P_true_detection_1_pair, fidelity
