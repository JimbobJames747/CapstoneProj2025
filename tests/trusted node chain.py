import numpy as np
import matplotlib.pyplot as plt
class MultiRelayEquation17TrustedNode:
    """
    ALL equations are from Peng-Yong Kong paper
    Just calcualation for SKR no Fidelity calculation(if use two-time bin then Fidelity is only realated to P dark instead of distance)
    Multi-relay trusted node model based on Equation (17):
    Si = 1 / (1/Si-1 + gamma_i * L)
    gamma_i is calculated using buffering and matching model (Eq.12-14)
    L(service key rate) is fixed and determined by lambda0 (Alice to Relay-1)
    """
    def __init__(self, distances, Q=1000, M=15, pulse_rate=40e6, C=500e6,
                 detector_eff=0.3, fiber_loss=0.2, qber=0.01):
        self.distances = distances  # List of N+1 nodes: [Alice, R1, R2, ..., Bob]
        self.Q = Q
        self.M = M
        self.pulse_rate = pulse_rate
        self.C = C
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber
        self.T = 1 / pulse_rate

        # Calculate lambda0 and L (fixed for all hops)
        self.lambda0 = self._calc_lambda(self.distances[0])
        self.L = self.Q * self.lambda0
    
    def _calc_lambda(self, d): #didn't consider P dark
        transmission = 10 ** (-self.fiber_loss * d / 10)
        return max(0.0, 0.5 * self.detector_eff * transmission)
    
    def _calculate_gamma(self, lambda_i):  
        """Use equation 14(expected waiting time which related to lambda i and lambda 0 ) for consistent γᵢ computation"""

        lambda0 = self.lambda0
        mu = (lambda0 * (1 - lambda_i)) / (lambda_i * (1 - lambda0))
        if mu >0.62 :          # see explanation in line64 of"trusted node single_relay_chain.py"
            mu =mu*lambda0
        pi_minus = 1 - mu ** self.M
        try:
            if mu < 1:
                K = (mu ** (self.M + 1)) / (1 - mu)
            elif mu == 1:
                K = 0
            else:
                K = float('inf')

            U_i = lambda_i / self.T

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
        λ0 = lambda0 
        λ1 = lambda1
        
        # Calculate probability factor μ (Equation 5)
        if λ1 > 0 and (1 - λ0) > 0:
            μ = (λ0 * (1 - λ1)) / (λ1 * (1 - λ0))
        else:
            μ = 0.0
        
        # Check stability condition (μ < 1)
        if μ >= 1 or self.L == 0:
            return 0.0
        
        # Calculate τ (auxiliary variable in Equation 16)
        t_q = (self.Q - 1) * self.T / 2  # Block waiting time
        τ = t_q / self.L + 1 / self.C    # τ = t_q/L + 1/C
        
        T = self.T
        M = self.M
        mu_M = μ ** M          # μ^M
        mu_2M1 = μ ** (2 * M + 1)  # μ^{2M+1}
        one_minus_mu = 1 - μ   # 1 - μ
        
        # Calculate numerator (Equation 16)
        numerator = λ0 ** 2 * one_minus_mu
        
        # Calculate denominator (Equation 16)
        term1 = τ * λ0 ** 2 * one_minus_mu
        term2 = T * (one_minus_mu * (λ0 + mu_M) + mu_2M1)
        denominator = term1 + term2
        
        # Calculate S1
        if denominator > 0:
            S1 = numerator / denominator
        else:
            S1 = 0.0
        #Consider erro correcation and Privacy Amplification
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * self.qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
        
        return S1*post_eff/1000 #kbps
    
    def calc_total_skr(self):
        """Calculate end-to-end SKR using Equation 17"""
        N = len(self.distances) - 1
        if N < 1:
            return 0.0

        lambda1 = self._calc_lambda(self.distances[1])
        Si_prev = self.calculate_s1_equation16(self.lambda0, lambda1)

        for i in range(1, N):
            lambda_next = self._calc_lambda(self.distances[i + 1])
            gamma_i = self._calculate_gamma(lambda_next)
            if Si_prev == 0:
                return 0.0
            Si = 1 / (1 / Si_prev + gamma_i * self.L)
            Si_prev = Si

        return Si_prev


class MultiRelayTraditionalTrustedNode:
    def __init__(self, distances, pulse_rate=40e6, detector_eff=0.3,
                 fiber_loss=0.2, qber=0.01):
        self.distances = distances
        self.pulse_rate = pulse_rate
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber

    def _calc_lambda(self, d):
        transmission = 10 ** (-self.fiber_loss * d / 10)
        return max(0.0, 0.5 * self.detector_eff * transmission)

    def _calc_skr(self, lam):
        raw = self.pulse_rate * lam
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * self.qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
        return raw * post_eff / 1000

    def calc_total_skr(self):
        skr_list = [self._calc_skr(self._calc_lambda(d)) for d in self.distances]
        return min(skr_list)


def compare_plot(): #compare two scheme in 200km
    total_distance = 300
    relay_counts = list(range(1, 60))

    skr_traditional = []
    skr_equation17 = []

    DELTA = 0.5

    for relays in relay_counts:
        segments = relays + 1
        total_span = segments + DELTA  # D = (|R| + 1 + Δ)d1
        d0 = (1 + DELTA) * total_distance / total_span  # d0 = (1 + Δ)d1
        d_list = [d0]  # Alice to Relay1
        for _ in range(relays - 1):
            d_i = total_distance / total_span # D / (|R| + 1 + Δ=d1
            d_list.append(d_i)  # Relay_i to Relay_i+1
        d_list.append(total_distance / total_span)  # Last relay to Bob

        eq17 = MultiRelayEquation17TrustedNode(d_list)
        skr_equation17.append(eq17.calc_total_skr())

        trad = MultiRelayTraditionalTrustedNode(d_list)
        skr_traditional.append(trad.calc_total_skr())

    plt.figure(figsize=(8, 6))
    plt.plot(relay_counts, skr_traditional, 'r--o', label='Traditional (min SKR)', linewidth=2)
    plt.plot(relay_counts, skr_equation17, 'b-o', label='Equation (17)', linewidth=2)
    plt.xlabel('Number of Relays', fontsize=12)
    plt.ylabel('Total Effective SKR (kbps)', fontsize=12)
    plt.title('Multi-Relay Trusted Node SKR Comparison(200KM)', fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("multi_relay_skr_comparison.png", dpi=300)
    plt.show()


def find_optimal_relay_number(total_distance, delta=0.5, max_relays=60, **params):
    """
    Given a total distance D, compute the optimal number of relays that maximizes SKR
    using Equation (17) from the paper.
    """
    best_r = 1
    best_skr = 0
    skr_list = []

    for relays in range(1, max_relays + 1):
        segments = relays + 1
        total_span = segments + delta  # D = (|R| + 1 + delta) * d1
        d0 = (1 + delta) * total_distance / total_span
        d_list = [d0]
        for _ in range(relays - 1):
            d_i = total_distance / total_span
            d_list.append(d_i)
        d_list.append(total_distance / total_span)

        eq17 = MultiRelayEquation17TrustedNode(d_list, **params)
        skr = eq17.calc_total_skr()
        skr_list.append(skr)

        if skr > best_skr:
            best_skr = skr
            best_r = relays

    print(f"[Optimal Relay Search] Best r = {best_r}, Max SKR = {best_skr:.2f} kbps")

    # Optional: plot
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


#  optimal relay number

if __name__ == "__main__":
    try:
        D_input = float(input("Please enter the total distance D (in km)(for Accuracy please set distance bigger than at least 25KM): "))
        if D_input <= 0:
            raise ValueError("Distance must be positive.")
    except ValueError as e:
        print(f"Invalid input: {e}")
    else:
        # Parameter settings (customizable)
        params = {
            "Q": 1000,
            "M": 15,
            "pulse_rate": 40e6,
            "C": 500e6,
            "detector_eff": 0.3,
            "fiber_loss": 0.2,
            "qber": 0.01
        }

        find_optimal_relay_number(total_distance=D_input, **params)


# compare the SKR of two scheme in 200KM
#if __name__ == "__main__":
 #   compare_plot()