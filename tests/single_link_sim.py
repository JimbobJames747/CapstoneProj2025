import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def compute_g2(times_A, times_B, tau_min, tau_max, bin_width):
    """
    Compute the g2(τ) histogram from detection times.
    
    Parameters:
    - times_A, times_B: sorted arrays of detection times from detectors A and B
    - tau_min, tau_max: min and max time delays to include (in same units as detection times)
    - bin_width: width of histogram bins (same units)

    Returns:
    - tau_centers: center of each τ bin
    - g2: normalized histogram (area under curve = 1)
    """

    taus = []
    idx_B = 0
    for t_A in times_A:
        # Move idx_B forward to skip B times that are too early
        while idx_B < len(times_B) and times_B[idx_B][0] < t_A[0] + tau_min:
            idx_B += 1

        idx = idx_B
        while idx < len(times_B) and times_B[idx][0] <= t_A[0] + tau_max:
            tau = times_B[idx][0] - t_A[0]
            taus.append(tau)
            idx += 1

    taus = np.array(taus)

    # Histogram
    bins = np.arange(tau_min, tau_max + bin_width, bin_width)
    hist, edges = np.histogram(taus, bins=bins)
    tau_centers = (edges[:-1] + edges[1:]) / 2

    count_rate = np.sum(hist)

    # Normalize so area under curve = 1
    #g2 = hist / (np.sum(hist) * bin_width)
    g2 = hist

    #print("check area under curve:", np.sum(g2 * bin_width))


    return tau_centers, g2, count_rate


def get_acc_count_subtraction(max_detections):
    acc_count_subtraction = []
    for detection in max_detections:
        if detection[1]:
            acc_count_subtraction.append((detection[0], True))
    return acc_count_subtraction


def run_single_link(seed, iteration_number, delta_t):
    for _ in range(iteration_number):
        np.random.seed(seed=seed)
        ### source params: [eps datasheet]
        ### fibre params: [thor smf28j9 @ 1550nm]
        ### detector: [photon spot - joshi]

        # --- Parameters ---
        # assume links A-Source Source-B are identical
        R_rep = 50e6              # Source repetition rate [Hz]
        mu = .01                 # Mean photon pairs per pulse

        length = 10 # [km]
        midpoint_length = length / 2
        fibre_atten = -0.18        
        fibre_effeciency = 10**((fibre_atten*midpoint_length) / 10)
        n_fibre = 1.46 # assumed from Thor


        detection_effeciency = 0.75
        dead_time = 1e-8 # 10 ns

        total_effeciency = fibre_effeciency * detection_effeciency
        print("total effeciency:", total_effeciency)

        jitter = 70e-11           # Detector jitter [seconds], 70 ps
        dark_count_rate = 1000             # Dark count rate [Hz]

        T = 1e-1              # Simulation duration [seconds]

            # --- Time array for source pulses ---
        pulse_times = np.arange(0, T, 1 / R_rep)
        print("Pulse attempts:", len(pulse_times))

        # --- Lists to hold detection times ---
        coinc_and_singles_A = []
        coinc_and_singles_B = []

        c_km = 300000 # [km / s]
        speed_of_light_in_fibre_km = c_km / n_fibre # [km/s]
        transmission_delay = midpoint_length / speed_of_light_in_fibre_km
        # --- Simulate photon pair detection per pulse ---
        pairs_generated = []

        for pulse_time in pulse_times:
            det_A = False
            det_B = False
            t_A = None 
            t_B = None
            # generate random amount of random pairs
            num_pairs = np.random.poisson(mu) # [Takesue] eq 23
            pairs_generated.append(num_pairs)
            for _ in range(num_pairs):
                # simulate if photon is detected
                if np.random.rand() < total_effeciency:
                    t_A = pulse_time + transmission_delay + np.random.normal(0, jitter) # ToDO: confirm jitter is Gaussian
                    det_A = True
                if np.random.rand() < total_effeciency:
                    t_B = pulse_time + transmission_delay + np.random.normal(0, jitter)
                    det_B = True
                if det_A and det_B:
                    coinc_and_singles_A.append((t_A, True))
                    coinc_and_singles_B.append((t_B, True))
                elif det_A and not det_B:
                    coinc_and_singles_A.append((t_A, False))
                elif det_B and not det_A:
                    coinc_and_singles_B.append((t_B, False))
        print("average Pairs generated per pulse", np.mean(pairs_generated))
        print("Single and CC Detections A:", len(coinc_and_singles_A))
        print("Single and CC Detections B", len(coinc_and_singles_B))
        print("Single and CC Rate A [CC / s]:", len(coinc_and_singles_A) / T)
        print("Single and CC Rate B [CC / s]:", len(coinc_and_singles_B) / T)

         # --- Calculate dark counts ---
        num_dark_A = np.random.poisson(dark_count_rate * T) # [Chalupnik]
        num_dark_B = np.random.poisson(dark_count_rate * T)

        print("Number of dark counts A:", num_dark_A)
        print("Number of dark counts B:", num_dark_B)

        # Uniformly random arrival times over the total simulation time
        max_detections_A = coinc_and_singles_A.copy()
        max_detections_B = coinc_and_singles_B.copy()

        dark_count_times_A =  list(np.random.uniform(0, T, num_dark_A))
        dark_count_times_B = list(np.random.uniform(0, T, num_dark_B))

        # add jitter to dark counts
        for i in range(len(dark_count_times_A)):
            dark_count_times_A[i] += np.random.normal(0, jitter)
        for i in range(len(dark_count_times_B)):
            dark_count_times_B[i] += np.random.normal(0, jitter)

        max_detections_A += [(t, False) for t in dark_count_times_A]
        max_detections_B +=  [(t, False) for t in dark_count_times_B]


        # --- Sort detections ---
        max_detections_A.sort()
        max_detections_B.sort()

        print("Max Detections A Before Detector Dark Time Removals:", len(max_detections_A))
        print("Max Detections B Before Detector Dark Time Removals", len(max_detections_B))

        # apply dead time
        last_det_t = None 
        first_detection = True
        while i < len(max_detections_A):
            if first_detection: 
                first_detection = False 
                last_det_t = max_detections_A[i][0]
            else:
                # if within detector deadtime
                if max_detections_A[i][0] <= last_det_t + dead_time:
                    max_detections_A.pop(i) # eliminate this detection
            i += 1
        
        last_det_t = None 
        first_detection = True
        while i < len(max_detections_B):
            if first_detection: 
                first_detection = False 
                last_det_t = max_detections_B[i][0]
            else:
                # if within detector deadtime
                if max_detections_B[i][0] <= last_det_t + dead_time:
                    max_detections_B.pop(i) # eliminate this detection
            i += 1

        print("Max Detections A After Detector Dark Time Removals:", len(max_detections_A))
        print("Max Detections B After Detector Dark Time Removals", len(max_detections_B))

        # accidental count subtraction
        acc_count_sub_A = get_acc_count_subtraction(max_detections_A)
        acc_count_sub_B = get_acc_count_subtraction(max_detections_B)

    
        print("Max Detections A:", len(max_detections_A))
        print("Max Detections B", len(max_detections_B))
        print("Detections after Accidental Detections Subtraction A:", len(acc_count_sub_A))
        print("Detections after Accidental Detections Subtraction B", len(acc_count_sub_B))

        # --- Compute coincidences ---
        tau_max = 5e-9
        max_tau_centers, max_g2, max_counts = compute_g2(max_detections_A, max_detections_B, tau_min=-tau_max, tau_max=tau_max, bin_width=1e-10)

        #min_tau_centers, min_g2, min_counts = compute_g2(min_detections_A, min_detections_B, tau_min=-tau_max, tau_max=tau_max, bin_width=1e-10)

        acc_sub_tau_centers, acc_sub_g2, acc_sub_counts = compute_g2(acc_count_sub_A, acc_count_sub_B, tau_min=-tau_max, tau_max=tau_max, bin_width=1e-10)
        
        min_counts = max_counts - acc_sub_counts

        # [Tsujimoto]
        print("Max counts:", max_counts)
        #print("Min counts:", min_counts)
        print("Min = Max - Acc count:", min_counts)
        visibility = (max_counts - min_counts) / (max_counts + min_counts)
        # [Thomas Supplemental]
        fidelity = (1 + 3 * visibility) / 4

        
        print("CAR [before applying coincidence window]:", max_counts / min_counts)
        print("Visibility [before applying coincidence window]:", visibility)
        print("Fidelity [before appying coincidence window]:", fidelity)
        seed += 1
    return max_tau_centers, max_g2, acc_sub_tau_centers, acc_sub_g2

if __name__=="__main__":
    starting_seed = 1
    delta_t = 0.13          # Coincidence window [ns], 130 ps

    max_tau_centers, max_g2, acc_sub_tau_centers, acc_sub_g2 = run_single_link(starting_seed, iteration_number=1, delta_t=delta_t)
    
    plt.plot(max_tau_centers * 1e9, max_g2, label='max')
    #plt.plot(min_tau_centers * 1e9, min_g2, label='min')
    plt.plot(acc_sub_tau_centers * 1e9, acc_sub_g2, label='acc_subtr')
    plt.axvline(x=-delta_t, color='red', linestyle='--', linewidth=1.5)  
    plt.axvline(x=delta_t, color='red', linestyle='--', linewidth=1.5)  


    plt.xlabel("Time Delay τ [ns]")
    plt.ylabel("Un-normalized G²(τ) [CC per τ bin]")
    plt.title("Second-Order Correlation Function ")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
