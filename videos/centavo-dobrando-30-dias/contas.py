"""E se você ganhasse 1 centavo que dobrasse todo dia por 30 dias? (conferido em 15/11/2026)
- Dia n recebe 0,01 * 2^(n-1).  CDI 13,65% a.a., IR 15% (longo prazo) -> tempo para dobrar.
- Nota de R$ 100: ~1 g, ~0,11 mm (estimativa: narração diz "uns"/"quase").
"""
import math
for n in (1, 7, 10, 15, 20, 21, 25, 27, 28, 29, 30):
    print("dia", n, "%.2f" % (0.01 * 2 ** (n - 1)), "| acumulado %.2f" % (0.01 * (2 ** n - 1)))
d30 = 0.01 * 2 ** 29; tot = 0.01 * (2 ** 30 - 1)
print("dia 30 / total %.3f" % (d30 / tot), "| ultimos 3 dias / total %.3f" % ((0.01*(2**27+2**28+2**29)) / tot))
notas = d30 / 100
print("notas de 100 no dia 30", int(notas), "peso kg", round(notas / 1000), "altura m", round(notas * 0.11 / 1000, 1))
liq = 1 + 0.1365 * 0.85
dob = math.log(2) / math.log(liq)
print("CDI líquido a.a. %.4f" % (liq - 1), "| anos para dobrar %.1f" % dob, "| 29 dobras: anos", round(29 * dob))
