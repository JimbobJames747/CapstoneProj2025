import numpy as np
import matplotlib.pyplot as plt

class MultiRelayEquation17TrustedNode:
    """
    ALL equations are from Peng-Yong Kong paper
    Just calculation for SKR, no Fidelity calculation (if using two-time bin, Fidelity is only related to P dark instead of distance)
    Multi-relay trusted node model based on Equation (17):
    Si = 1 / (1/Si-1 + gamma_i * L)
    gamma_i is calculated using buffering and matching model (Eq.12-14)
    L (service key rate) is fixed and determined by lambda0 (Alice to Relay-1)
    """
    def __init__(self, distances, Q=1000, M=15, pulse_rate=40e6, C=500e6,
                 detector_eff=0.3, fiber_loss=0.2, qber=0.01):
        """
        Initialize multi-relay model
        
        Args:
            distances: List of N+1 nodes: [Alice, R1, R2, ..., Bob]
            Q: Block size for key generation
            M: Buffer size for matching
            pulse_rate: Laser pulse rate (Hz)
            C: Processing rate (operations per second)
            detector_eff: Detector efficiency
            fiber_loss: Fiber loss (dB/km)
            qber: Quantum bit error rate
        """
        self.distances = distances
        self.Q = Q
        self.M = M
        self.pulse_rate = pulse_rate
        self.C = C
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber
        self.T = 1 / pulse_rate  # Time between pulses

        # Calculate lambda0 and L (fixed for all hops)
        self.lambda0 = self._calc_lambda(self.distances[0])
        self.L = self.Q * self.lambda0  # Service key rate

    def _calc_lambda(self, d):
        """Calculate detection probability for given distance (ignoring dark count)"""
        transmission = 10 ** (-self.fiber_loss * d / 10)
        return max(0.0, 0.5 * self.detector_eff * transmission)

    def _calculate_gamma(self, lambda_i):
        """
        Calculate gamma_i using equation 14 (expected waiting time related to lambda i and lambda0)
        See explanation in line64 of "trusted node single_relay_chain.py" for the mu > 0.62 adjustment
        """
        lambda0 = self.lambda0
        mu = (lambda0 * (1 - lambda_i)) / (lambda_i * (1 - lambda0))
        # Apply heuristic adjustment based on empirical observation
        if mu > 0.62:          
            mu = mu * lambda0

        pi_minus = 1 - mu ** self.M

        try:
            # Calculate K based on mu value
            if mu < 1:
                K = (mu ** (self.M + 1)) / (1 - mu)
            elif mu == 1:
                K = 0
            else:
                K = float('inf')

            U_i = lambda_i / self.T  # Detection rate

            # Calculate waiting delay for matching
            if U_i > 0 and not np.isinf(K):
                waiting_delay = (K + 1) / U_i + self.T
            else:
                waiting_delay = float('inf')

            numerator = pi_minus * self.T + (1 - pi_minus) * waiting_delay
            gamma_i = numerator / lambda0
            return gamma_i

        except (ZeroDivisionError, ValueError, OverflowError):
            return float('inf')

    def calculate_s1_equation16(self, lambda0, lambda1):
        """Calculate single-hop SKR using Equation 16"""
        # Validate inputs
        if lambda1 <= 0 or (1 - lambda0) <= 0:
            return 0.0

        # Calculate probability factor mu (Equation 5)
        mu = (lambda0 * (1 - lambda1)) / (lambda1 * (1 - lambda0))
        
        # Check stability condition (mu < 1)
        if mu >= 1 or self.L == 0:
            return 0.0

        # Calculate tau (auxiliary variable in Equation 16)
        t_q = (self.Q - 1) * self.T / 2  # Block waiting time
        tau = t_q / self.L + 1 / self.C  # tau = t_q/L + 1/C

        # Precompute powers of mu for efficiency
        mu_M = mu ** self.M          # mu^M
        mu_2M1 = mu ** (2 * self.M + 1)  # mu^{2M+1}
        one_minus_mu = 1 - mu   # 1 - mu

        # Calculate numerator (Equation 16)
        numerator = lambda0 ** 2 * one_minus_mu

        # Calculate denominator (Equation 16)
        term1 = tau * lambda0 ** 2 * one_minus_mu
        term2 = self.T * (one_minus_mu * (lambda0 + mu_M) + mu_2M1)
        denominator = term1 + term2

        # Calculate S1 (Alice to first relay)
        if denominator <= 0:
            return 0.0

        S1 = numerator / denominator
        
        # Apply error correction and privacy amplification
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)  # Error correction efficiency
            eta_PA = max(0, 1 - 2 * self.qber)  # Privacy amplification efficiency
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5  # Default efficiency for invalid QBER
        
        return S1 * post_eff / 1000  # Convert to kbps

    def calc_total_skr(self):
        """Calculate end-to-end SKR using Equation 17"""
        N = len(self.distances) - 1  # Number of hops
        if N < 1:  # No relays, direct connection
            return 0.0

        # Calculate SKR for first hop (Alice to Relay1)
        lambda1 = self._calc_lambda(self.distances[1])
        Si = self.calculate_s1_equation16(self.lambda0, lambda1)

        # Cascade through subsequent hops
        for i in range(1, N):
            lambda_next = self._calc_lambda(self.distances[i + 1])
            gamma_i = self._calculate_gamma(lambda_next)
            
            # Skip if current SKR is zero
            if Si == 0:
                return 0.0
                
            # Apply Equation 17: Si = 1 / (1/Si-1 + gamma_i * L)
            Si = 1 / (1 / Si + gamma_i * self.L)

        return Si


class MultiRelayTraditionalTrustedNode:
    """Traditional trusted node model where end-to-end SKR is limited by the weakest link"""
    def __init__(self, distances, pulse_rate=40e6, detector_eff=0.3, fiber_loss=0.2, qber=0.01):
        self.distances = distances
        self.pulse_rate = pulse_rate
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber

    def _calc_lambda(self, d):
        """Calculate detection probability for given distance"""
        transmission = 10 ** (-self.fiber_loss * d / 10)
        return max(0.0, 0.5 * self.detector_eff * transmission)

    def _calc_skr(self, lam):
        """Calculate raw SKR for a single hop"""
        raw = self.pulse_rate * lam
        
        # Apply error correction and privacy amplification
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * self.qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
            
        return raw * post_eff / 1000  # Convert to kbps

    def calc_total_skr(self):
        """End-to-end SKR is the minimum SKR across all hops"""
        skr_list = [self._calc_skr(self._calc_lambda(d)) for d in self.distances]
        return min(skr_list)


def compare_plot():
    """
    Compare the SKR performance of traditional and Equation 17 models
    for a fixed total distance (300km) across different relay counts
    """
    total_distance = 300  # km
    relay_counts = list(range(1, 60))  # Test 1 to 59 relays
    DELTA = 0.5  # Distance allocation parameter
    
    skr_traditional = []
    skr_equation17 = []

    for relays in relay_counts:
        # Calculate distance allocation based on relay count
        segments = relays + 1
        total_span = segments + DELTA  # D = (|R| + 1 + Δ) * d1
        d0 = (1 + DELTA) * total_distance / total_span  # First segment: (1+Δ)d1
        d_list = [d0]  # Alice to first relay
        
        # Intermediate segments (each length d1)
        for _ in range(relays - 1):
            d_i = total_distance / total_span
            d_list.append(d_i)
            
        # Last segment (Relay_n to Bob)
        d_list.append(total_distance / total_span)

        # Calculate SKR for Equation 17 model
        eq17 = MultiRelayEquation17TrustedNode(d_list)
        skr_equation17.append(eq17.calc_total_skr())

        # Calculate SKR for traditional model
        trad = MultiRelayTraditionalTrustedNode(d_list)
        skr_traditional.append(trad.calc_total_skr())

    # Plot results
    plt.figure(figsize=(8, 6))
    plt.plot(relay_counts, skr_traditional, 'r--o', label='Traditional (min SKR)', linewidth=2)
    plt.plot(relay_counts, skr_equation17, 'b-o', label='Equation (17)', linewidth=2)
    plt.xlabel('Number of Relays', fontsize=12)
    plt.ylabel('Total Effective SKR (kbps)', fontsize=12)
    plt.title('Multi-Relay Trusted Node SKR Comparison (300 km)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("multi_relay_skr_comparison.png", dpi=300)
    plt.show()


def find_optimal_relay_number(total_distance, delta=0.5, max_relays=60, **params):
    """
    Given a total distance D, compute the optimal number of relays that maximizes SKR
    using Equation (17) from the paper.
    
    Args:
        total_distance: Total end-to-end distance (km)
        delta: Distance allocation parameter
        max_relays: Maximum number of relays to test
        **params: Additional parameters for model initialization
    """
    best_r = 1  # Optimal relay count
    best_skr = 0  # Maximum SKR found
    skr_list = []  # SKR values for each relay count

    for relays in range(1, max_relays + 1):
        # Calculate distance allocation
        segments = relays + 1
        total_span = segments + delta  # D = (|R| + 1 + delta) * d1
        d0 = (1 + delta) * total_distance / total_span  # First segment
        
        # Create distance list: [d0, d1, d1, ..., d1]
        d_list = [d0]
        for _ in range(relays - 1):
            d_i = total_distance / total_span  # Intermediate segments
            d_list.append(d_i)
        d_list.append(total_distance / total_span)  # Last segment

        # Initialize model and calculate SKR
        eq17 = MultiRelayEquation17TrustedNode(d_list, **params)
        skr = eq17.calc_total_skr()
        skr_list.append(skr)

        # Update best result if current SKR is higher
        if skr > best_skr:
            best_skr = skr
            best_r = relays

    print(f"[Optimal Relay Search] Best r = {best_r}, Max SKR = {best_skr:.2f} kbps")

    # Plot SKR vs relay count
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, max_relays + 1), skr_list, 'b-o', label='SKR (Equation 17)')
    plt.axvline(best_r, color='red', linestyle='--', label=f'Optimal Relays = {best_r}')
    plt.xlabel('Number of Relays')
    plt.ylabel('Effective SKR (kbps)')
    plt.title(f'Optimal Relay Search for D = {total_distance} km')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig('optimal_relay_search.png', dpi=300)
    plt.show()


if __name__ == "__main__":
    # Optimal relay number search
    try:
        D_input = float(input("Enter total distance D (in km): "))
        if D_input <= 0:
            raise ValueError("Distance must be positive.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        # Default parameters (can be customized)
        params = {
            "Q": 1000,
            "M": 15,
            "pulse_rate": 40e6,
            "C": 500e6,
            "detector_eff": 0.3,
            "fiber_loss": 0.2,
            "qber": 0.01
        }
        find_optimal_relay_number(D_input, **params)
     
    # compare_plot()