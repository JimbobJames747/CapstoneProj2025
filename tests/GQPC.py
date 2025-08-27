import numpy as np
import matplotlib.pyplot as plt

# 参数设置
eta = np.linspace(0.0, 1, 500)


# 定义公式
def P_formula(eta, m):
    prod1 = np.ones_like(eta)
    prod2 = np.ones_like(eta)
    for mi in m:
        prod1 *= (1 - (1 - eta)**mi)
        prod2 *= (1 - (1 - eta)**mi - eta**mi / 2)
    return prod1 - prod2


# 更新参数
n = 7
m = [3, 3, 3] + [4]*4

# 重新计算
P1 = eta/2
P2 = P_formula(eta, m)
P3 = P_formula(eta, [5, 5, 5, 5, 5])

# 作图
plt.figure(figsize=(6, 4.8))  # 英寸；论文小图可 5~7 宽
plt.plot(eta, P1, label='BSM(no QEC)')
plt.plot(eta, P3, label='BSM(QPC[5,5])')
plt.plot(eta, P2, label='BSM(GQPC[3,3,3,4,4,4,4])')
plt.xlabel(r'$\eta$')
plt.ylabel('P')
plt.title('Performance Analysis of QEC in Quantum Chain (n=25)')
plt.legend()
plt.grid(False)
plt.tick_params(direction='in')
plt.tight_layout()
plt.margins(x=0, y=0)
plt.savefig('GQPC.png', dpi=300)
plt.show()

    
    
