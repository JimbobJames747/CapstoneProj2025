import numpy as np

class MultiRelayEquation17TrustedNode:
    """
    ALL equations are from Peng-Yong Kong paper
    Just calculation for SKR, no Fidelity calculation (if using two-time bin, Fidelity is only related to P dark instead of distance)
    Multi-relay trusted node model based on Equation (17):
    Si = 1 / (1/Si-1 + gamma_i * L)
    gamma_i is calculated using buffering and matching model (Eq.12-14)
    L (service key rate) is fixed and determined by lambda0 (Alice to Relay-1)
    """
    def __init__(self, total_distance, relay_number=None, Q=1000, M=15, pulse_rate=40e6, C=500e6,
                 detector_eff=0.3, fiber_loss=0.2, qber=0.01):
        self.total_distance = total_distance
        self.relay_number = relay_number  # Set to None to compute optimal relay number using find_optimal_relay_number
        self.Q = Q
        self.M = M
        self.pulse_rate = pulse_rate
        self.C = C
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber
        self.T = 1 / pulse_rate

        # Initialize distances only if relay_number is specified
        if self.relay_number is not None:
            self.distances = self.calculate_distance_allocation()
            self.lambda0 = self._calc_lambda(self.distances[0])
            self.L = self.Q * self.lambda0
        else:
            self.distances = None
            self.lambda0 = None
            self.L = None
    
    def _calc_lambda(self, d): # Doesn't consider P dark
        transmission = 10 ** (-self.fiber_loss * d / 10)
        return max(0.0, 0.5 * self.detector_eff * transmission)
    
    def _calculate_gamma(self, lambda_i):  
        """Calculate gamma_i using equation 14 (expected waiting time related to lambda i and lambda0)"""

        lambda0 = self.lambda0
        mu = (lambda0 * (1 - lambda_i)) / (lambda_i * (1 - lambda0))
        if mu > 0.62:          
            mu = mu * lambda0
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
        
        # Calculate SKR1(alice-relay1)
        if denominator > 0:
            S1 = numerator / denominator
        else:
            S1 = 0.0
        # Consider error correction and Privacy Amplification
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * self.qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
        
        return S1 * post_eff / 1000  # kbps
    
    def calc_total_skr(self):
        """Calculate end-to-end SKR using Equation 17"""
        if self.distances is None:
            return 0.0

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

    def calculate_distance_allocation(self, delta=0.5):
        """Calculate distance allocation based on total distance and relay number"""
        if self.relay_number is None:
            raise ValueError("Relay number not specified. Use find_optimal_relay_number first.")

        segments = self.relay_number + 1
        total_span = segments + delta  # D = (|R| + 1 + delta) * d1
        d0 = (1 + delta) * self.total_distance / total_span
        d_list = [d0]
        for _ in range(self.relay_number - 1):
            d_i = self.total_distance / total_span
            d_list.append(d_i)
        d_list.append(self.total_distance / total_span)

        return d_list

    def find_optimal_relay_number(self, delta=0.5, max_relays=60):
        """
        Given a total distance D, compute the optimal number of relays that maximizes SKR
        using Equation (17) from the paper.
        """
        best_r = 1
        best_skr = 0
        skr_list = []

        for relays in range(1, max_relays + 1):
            # Set relay number
            self.relay_number = relays
            self.distances = self.calculate_distance_allocation(delta)

            # Calculate lambda0 and L
            self.lambda0 = self._calc_lambda(self.distances[0])
            self.L = self.Q * self.lambda0

            skr = self.calc_total_skr()
            skr_list.append(skr)

            if skr > best_skr:
                best_skr = skr
                best_r = relays

        # Restore initial state
        self.relay_number = None
        self.distances = None
        self.lambda0 = None
        self.L = None

        return best_r, best_skr, skr_list

# Example usage:
total_distance = 100  # km
# Case 1: User specifies relay_number
relay_num = 10
model1 = MultiRelayEquation17TrustedNode(total_distance, relay_number=relay_num)
print(f"SKR with {relay_num} relays: {model1.calc_total_skr()} kbps")

# Case 2: User does not specify relay_number, auto-find optimal
model2 = MultiRelayEquation17TrustedNode(total_distance)
best_r, best_skr, _ = model2.find_optimal_relay_number()
print(f"Optimal number of relays: {best_r}, SKR: {best_skr} kbps")