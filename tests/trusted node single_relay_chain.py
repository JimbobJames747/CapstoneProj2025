import numpy as np
import matplotlib.pyplot as plt

class Traditional_single_relay_TrustedNode:
    """Traditional trusted node model: each link is evaluated independently and the smaller SKR is taken"""
    def __init__(self, d_A2R, d_R2B, pulse_rate=40e6, detector_eff=0.3,
                 fiber_loss=0.2, qber=0.01):
        self.d_A2R = d_A2R
        self.d_R2B = d_R2B
        self.pulse_rate = pulse_rate
        self.detector_eff = detector_eff
        self.fiber_loss = fiber_loss
        self.qber = qber

    def calc_lambda(self, distance):
        loss = 10 ** (-self.fiber_loss * distance / 10)
        lambda_raw = 0.5 * self.detector_eff * loss
        return max(0.0, lambda_raw)

    def calc_skr_single_link(self, distance):
        lam = self.calc_lambda(distance)
        raw_rate = self.pulse_rate * lam
        # Post-processing efficiency
        if 0 < self.qber < 0.5:
            h2 = -self.qber * np.log2(self.qber) - (1 - self.qber) * np.log2(1 - self.qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * self.qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
        return raw_rate * post_eff / 1000  # Convert to kbps

    def calc_total_skr(self):
        skr1 = self.calc_skr_single_link(self.d_A2R)
        skr2 = self.calc_skr_single_link(self.d_R2B)
        return min(skr1, skr2)


class single_relay_TrustedNode:
    """Trusted node model SKR calculation with Peng-Yong Kong paper (based on Equation 16)"""
    def __init__(self, Q, M=50, pulse_rate=40e6, C=500e6):
        self.Q = Q
        self.M = M
        self.pulse_rate = pulse_rate
        self.C = C
        self.T = 1 / pulse_rate
        self.lambda0 = 0.2  # Can be overwritten externally
        self.lambda1 = 0.25
        self.L = self.Q * self.lambda0 


    def _calculate_lambda(self, distance, detector_eff=0.3, fiber_loss=0.2):
        transmission = 10 ** (-fiber_loss * distance / 10)
        return max(0.0, 0.5 * detector_eff * transmission)

    def calculate_tau(self):
        t_q = (self.Q - 1) * self.T / 2
        return t_q / self.L + 1 / self.C

    def calculate_s1_equation16(self):
        λ0 = self.lambda0
        λ1 = self.lambda1
        μ = (λ0 * (1 - λ1)) / (λ1 * (1 - λ0))
        #if μ >0.62 :          # some math trick for Marginal Effect of this math model ,because if μ close to 1 then this math perform wrong(skr will have a sharp decline when disance smaller than 20km,which is not right,so make this whole curve beautiful I Manually set this condition)
            #μ =μ*λ0
        τ = self.calculate_tau()
        T = self.T
        M = self.M
        mu_M = μ ** M
        mu_2M1 = μ ** (2 * M + 1)
        one_minus_mu = 1 - μ
        numerator = λ0 ** 2 * one_minus_mu
        denominator = (
            τ*λ0 ** 2 * one_minus_mu +
            T * ((one_minus_mu * (λ0 + mu_M)) + mu_2M1)
        )
        return numerator / denominator if denominator > 0 else 0.0

    def calculate_effective_skr(self, qber=0.01):
        raw_skr = self.calculate_s1_equation16()
        if 0 < qber < 0.5:
            h2 = -qber * np.log2(qber) - (1 - qber) * np.log2(1 - qber)
            eta_EC = max(0, 1 - 1.16 * h2)
            eta_PA = max(0, 1 - 2 * qber)
            post_eff = eta_EC * eta_PA
        else:
            post_eff = 0.5
        return raw_skr * post_eff


def plot_fig5c():
    Q_values = np.array([100, 200, 400, 800, 1000, 2000, 4000, 8000, 10000])
    skr_values = []

    for Q in Q_values:
        node = sigle_relay_TrustedNode(Q=Q, M=15)
        skr = node.calculate_effective_skr(qber=0.01)
        skr_kbps = skr / 1000
        skr_values.append(skr_kbps)

    # Plot
    plt.figure(figsize=(8, 6), dpi=120)
    plt.plot(Q_values, skr_values, 'bo-', linewidth=2.5, label='Eq. (16), λ₀=0.2, λ₁=0.25, M=15')
    plt.xlabel("Block size Q", fontsize=12)
    plt.ylabel("Effective SKR (kbps)", fontsize=12)
    plt.title("Reproduction of Fig. 5(c): SKR vs Q", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig("fig5c_reproduction.png", dpi=300)
    plt.show()


def compare_new_vs_traditional():
    distances = np.linspace(10, 200, 50)
    skr_new = []
    skr_trad = []

    DELTA = 0.5
    Q = 1000
    M = 15
    qber = 0.01
    pulse_rate = 40e6
    C = 500e6
    detector_eff = 0.3
    fiber_loss = 0.2

    for D in distances:
        total_span = 2 + DELTA
        d0 = (1 + DELTA) * D / total_span  # Alice to Relay
        d1 = D / total_span                # Relay to Bob

        # Proposed model
        node = single_relay_TrustedNode(Q=Q, M=M, pulse_rate=pulse_rate, C=C)
        node.lambda0 = node._calculate_lambda(d0, detector_eff, fiber_loss)
        node.lambda1 = node._calculate_lambda(d1, detector_eff, fiber_loss)
        node.L = Q * node.lambda0
        skr = node.calculate_effective_skr(qber=qber)
        skr_new.append(skr / 1000)  # Convert to kbps

        # Traditional model
        trad_node = Traditional_single_relay_TrustedNode(
            d_A2R=d0, d_R2B=d1,
            pulse_rate=pulse_rate,
            detector_eff=detector_eff,
            fiber_loss=fiber_loss,
            qber=qber
        )
        skr_trad.append(trad_node.calc_total_skr())

    # Plot
    plt.figure(figsize=(10, 6))
    plt.plot(distances, skr_new, 'b-', linewidth=2.2, label='Proposed (Equation 16)')
    plt.plot(distances, skr_trad, 'r--', linewidth=2.2, label='Traditional (min{SKR_A→R, SKR_B→R})')
    plt.xlabel("Total Distance (km)", fontsize=12)
    plt.ylabel("Effective SKR (kbps)", fontsize=12)
    plt.title("Proposed vs Traditional Trusted Node SKR", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.savefig("skr_comparison_traditional_vs_new.png", dpi=300)
    plt.show()


# Run
if __name__ == "__main__":
   compare_new_vs_traditional()
   #plot_fig5c()
