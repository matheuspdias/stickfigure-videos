# Contas do exemplo (apartamento na planta, MCMV faixa 2)
IMOVEL = 250_000
FIN = 160_000          # financiado pela Caixa
FGTS_SUB = 54_000      # FGTS + subsidio (exemplo)
ENTRADA = IMOVEL - FIN - FGTS_SUB   # 36.000 parcelado com a construtora
N_OBRA = 36
TAXA = 0.06            # nominal a.a. (faixa 2: 4,75% a 7%)
SEG = 50               # seguros MIP/DFI + taxa adm aprox.
INCC_AA = 0.066        # INCC-M 12 meses ate set/2026 = 6,61%
i_m = TAXA / 12
incc_m = (1 + INCC_AA) ** (1 / 12) - 1
import math
def lib(m):  # % liberado: 10% no inicio, curva S ate 100% no mes 36
    x = m / N_OBRA
    return 0.10 + 0.90 * (3 * x**2 - 2 * x**3)
print("entrada construtora", ENTRADA, "->", ENTRADA / N_OBRA, "por mes")
for m in [1, 6, 12, 18, 24, 30, 36]:
    ev = FIN * lib(m) * i_m + SEG * lib(m)
    ent = ENTRADA / N_OBRA * (1 + incc_m) ** (m - 1)
    print(f"mes {m:2d}: liberado {lib(m)*100:5.1f}%  evolucao R$ {ev:6.0f}  entrada R$ {ent:6.0f}  soma R$ {ev+ent:6.0f}")
amort = FIN / 420
p1 = amort + FIN * i_m + SEG
print(f"1a parcela SAC 420m: {p1:.0f} (amort {amort:.0f}), 30% renda 4000 = 1200")
print(f"ultima parcela SAC: {amort + amort*i_m + SEG:.0f}")
