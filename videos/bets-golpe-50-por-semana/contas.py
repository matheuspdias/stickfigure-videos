# Proibição: MP 1.394/2026 (assinada 25/09/2026, em vigor 06/10/2026, prorrogada até 05/03/2027)
# IBJR/LegitBet: 60.477 endereços suspeitos após a proibição (dados até 27/10/2026; Diario de Pernambuco 03/11/2026)
# PCDF: rede ilegal movimentou ~R$ 739 milhões, Pix para empresas de fachada (InvesTalk/Broadcast 12/11/2026)
cdi = 0.1365
im = (1 + cdi) ** (1 / 12) - 1
dep = 50 * 52 / 12
print("por mes", dep)                 # 216,67
def fv(meses):
    tot = 0
    for k in range(meses):
        n = meses - k; v = dep * (1 + im) ** n; g = v - dep
        ir = 0.225 if n <= 6 else 0.20 if n <= 12 else 0.175 if n <= 24 else 0.15
        tot += v - g * ir
    return tot
print("1 ano", fv(12), dep * 12)      # ~2.750 x 2.600
print("5 anos", fv(60), dep * 60)     # ~17.480 x 13.000
print("metade/ano", 25 * 52)          # 1.300
