# Rotativo: 451,7% a.a. em set/2026 (BC, divulgado 30/10/2026)
a = 4.517
m = (1 + a) ** (1 / 12) - 1
print(f"ao mes: {m*100:.1f}%")            # ~15,3%
print(f"juros 1 mes em 1000: {1000*m:.0f}")  # ~153
for k in range(1, 7):
    print(k, round(1000 * (1 + m) ** k))      # dobra em ~5 meses
# teto Lei 14.690/2023 (desde 03/01/2024): juros+encargos <= 100% da divida -> 1000 vira no maximo 2000
# consignado INSS ~1,85%/mes -> ~R$ 19; CLT ~3% -> ~R$ 30
print(1000 * 0.0185, 1000 * 0.03)
