def single_link(l, alpha, verbose=False):
    # l: link length from A to B
    # alpha  # [db/Km]
  
    # ToDO: free running vs. gated detectors
    
    detector_eff = 1 
    quantum_eff = .014

    
    avg_photons_per_pulse = .015
    avg_noise_photons_per_pulse = 0.01
    avg_noise_photons_per_pulse = 0

    # takesue 2005
    # assuming 1 ns gate
    # Placeholder value
    dc_rate_per_gate = 7.5e-5
    

    transm_eta = 10**((-alpha * l) / (2 * N) / 10)
    if verbose: print("transm eta", transm_eta)

    total_transm_alice = transm_eta * detector_eff * quantum_eff
    total_transm_bob = total_transm_alice

    # honjo equation 1
    # and Takesue 2005 eq 4
    avg_count_rate_per_time_slot_alice = ((avg_photons_per_pulse + avg_noise_photons_per_pulse) * total_transm_alice) + dc_rate_per_gate

    # honjo equation 2
    avg_count_rate_per_time_slot_bob = ((avg_photons_per_pulse + avg_noise_photons_per_pulse) * total_transm_bob) + dc_rate_per_gate

    # honjo equation 3
    coinc_to_acc_ratio = (avg_photons_per_pulse * total_transm_alice * total_transm_bob)
    coinc_to_acc_ratio /= (avg_count_rate_per_time_slot_alice * avg_count_rate_per_time_slot_bob)
    coinc_to_acc_ratio += 1

    # honjo equation 4
    numerator = 0.25 * avg_photons_per_pulse * total_transm_alice * total_transm_bob
    denominator = (
        numerator + 
        + 2 * ((avg_photons_per_pulse + avg_noise_photons_per_pulse) * 0.5 * total_transm_alice + dc_rate_per_gate) * ((avg_photons_per_pulse + avg_noise_photons_per_pulse) * 0.5 * total_transm_bob + dc_rate_per_gate)
    )
    visibility = numerator / denominator

     # Thomas, near eq S12
    fidelity = (1 + 3 * visibility) / 4

     # derived from honjo 3
    true_cc_rate = (avg_photons_per_pulse * total_transm_alice * total_transm_bob) + avg_count_rate_per_time_slot_alice * avg_count_rate_per_time_slot_bob

    acc_cc_rate = avg_count_rate_per_time_slot_alice * avg_count_rate_per_time_slot_bob

    # for James: for the entanglement distribution rate (coincidence count rate)
    # I've seen honjo use true + acc, and also 
    # takesue 2005 use only true counts. so I guess we can ask Joshi?

    source_rep_rate = 1e9 # 1 GHz
    ent_dist_rate = true_cc_rate * source_rep_rate

    return ent_dist_rate, fidelity
