import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def find_coincidences(detections_A, detections_B, delta_t):
    i, j = 0, 0
    true_cc = []
    false_cc = []
    while i < len(detections_A) and j < len(detections_B):
        t_A = detections_A[i][0]
        t_B = detections_B[j][0]
        dt = t_A - t_B
        if abs(dt) <= delta_t:
            if detections_A[i][1] and detections_B[j][1]: # true CC
                true_cc.append(dt)
            else: # accidental cc
                false_cc.append(dt)
            if t_A <= t_B:
                i += 1
            else:
                j += 1
        elif dt < -delta_t:
            i += 1
        else:
            j += 1

    return true_cc, false_cc


def run_single_link(seed, iteration_number, delta_t):
    for _ in range(iteration_number):
        np.random.seed(seed=seed)
        ### source params: [eps datasheet]
        ### fibre params: [thor smf28j9 @ 1550nm]
        ### detector: [photon spot - joshi]

        # --- Parameters ---
        # assume links A-Source Source-B are identical
        R_rep = 50e6              # Source repetition rate [Hz]
        mu = 0.01                 # Mean photon pairs per pulse

        length = 10 # [km]
        midpoint_length = length / 2
        fibre_atten = -0.18        
        fibre_effeciency = 10**((fibre_atten*midpoint_length) / 10)
        n_fibre = 1.46 # assumed from Thor


        detection_effeciency = 0.8

        total_effeciency = fibre_effeciency * detection_effeciency
        print("total effeciency:", total_effeciency)

        jitter = 70e-12           # Detector jitter [seconds], 70 ps
        dark_count_rate = 1000             # Dark count rate [Hz]

        T = 1              # Simulation duration [seconds]

            # --- Time array for source pulses ---
        pulse_times = np.arange(0, T, 1 / R_rep)
        print("Pulse attempts:", len(pulse_times))

        # --- Lists to hold detection times ---
        min_detections_A = []
        min_detections_B = []

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
                    min_detections_A.append((t_A, True))
                    min_detections_B.append((t_B, True))
                elif det_A and not det_B:
                    min_detections_A.append((t_A, False))
                elif det_B and not det_A:
                    min_detections_B.append((t_B, False))
        print("average Pairs generated per pulse", np.mean(pairs_generated))
        print("Single and CC Detections A:", len(min_detections_A))
        print("Single and CC Detections B", len(min_detections_B))
        print("Single and CC Rate A [CC / s]:", len(min_detections_A) / T)
        print("Single and CC Rate B [CC / s]:", len(min_detections_B) / T)

         # --- Calculate dark counts ---
        num_dark_A = np.random.poisson(dark_count_rate * T) # [Chalupnik]
        num_dark_B = np.random.poisson(dark_count_rate * T)

        print("Number of dark counts A:", num_dark_A)
        print("Number of dark counts B:", num_dark_B)

        # Uniformly random arrival times over the total simulation time
        max_detections_A = min_detections_A.copy()
        max_detections_B = min_detections_B.copy()

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
        min_detections_A.sort()
        min_detections_B.sort()
        max_detections_A.sort()
        max_detections_B.sort()
    
        print("Max Detections A:", len(max_detections_A))
        print("Max Detections B", len(max_detections_B))
        print("Min Detections A:", len(min_detections_A))
        print("Min Detections B", len(min_detections_B))


        # --- Compute coincidences ---
        true_cc, acc_cc = find_coincidences(max_detections_A, max_detections_B, delta_t)

        true_cc_counts = len(true_cc)
        acc_cc_counts = len(acc_cc)

        # [Tsujimoto]
        visibility = true_cc_counts / (true_cc_counts + 2 * acc_cc_counts)

        print("True CC counts:", true_cc_counts)
        print("Acc CC counts:", acc_cc_counts)
        print("CAR:", true_cc_counts / acc_cc_counts)
        print("Visibility:", visibility)
        seed += 1
    return true_cc, acc_cc

if __name__=="__main__":
    starting_seed = 1
    delta_t = 1.3e-10          # Coincidence window [seconds], 130 ps

    true_cc, acc_cc = run_single_link(starting_seed, iteration_number=1, delta_t=delta_t)

    all_cc_times = true_cc + [dt for dt in acc_cc]

    plt.hist(true_cc, bins=1000, range=(-1e-9, 1e-9), alpha=0.6, label="Min CC")
    plt.hist(all_cc_times, bins=1000, range=(-1e-9, 1e-9), alpha=0.6, label="Max CC")
    plt.legend()
    plt.xlabel("Time difference [s]")
    plt.ylabel("Counts")
    plt.show()

    max_cc_kde = sns.kdeplot(all_cc_times, common_norm=True, bw_adjust=0.5)
    max_cc_x, max_cc_y = max_cc_kde.get_lines()[0].get_data()
    max_cc_kde.clear()  # Clear the plot

    # Normalize to peak of 1
    max_y_normalized = max_cc_y / np.max(max_cc_y)

    min_cc_kde = sns.kdeplot(true_cc, common_norm=True, bw_adjust=0.5)
    min_cc_x, min_cc_y = min_cc_kde.get_lines()[0].get_data()
    min_cc_kde.clear()  # Clear the plot

    # Normalize to peak of 1
    min_y_normalized = min_cc_y / np.max(min_cc_y)

    plt.plot(min_cc_x, min_y_normalized, label='Min CC')
    plt.plot(max_cc_x, max_y_normalized, label='Max CC')
    plt.xlabel("g2??")
    plt.ylabel("Counts")
    plt.legend()
    plt.show()
