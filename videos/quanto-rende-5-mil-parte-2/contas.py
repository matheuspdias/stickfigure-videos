"""Contas do Quanto rende R$ 5 mil em 1 ano (Parte 2). Mesmas taxas da Parte 1 (19/11/2026):
Selic 13,75%, CDI 13,65% a.a., poupança 0,6638% a.m. (isenta); IR 17,5% (361-720 dias), 15% (>720 dias)."""
P = 5000
CDI = 0.1365
poup = P * 1.006638 ** 12
b100 = P * CDI; l100 = b100 * (1 - 0.175)
b110 = P * CDI * 1.10; l110 = b110 * (1 - 0.175)
print("poupanca", round(poup, 2), round(poup - P, 2))
print("cdb100/tesouro bruto", round(b100, 2), "IR", round(b100 * .175, 2), "liq", round(l100, 2), "->", round(P + l100))
print("cdb110 bruto", round(b110, 2), "liq", round(l110, 2), "->", round(P + l110))
print("dif 110 x poup 1 ano", round(l110 - (poup - P), 2))
print("por mes: cdb100", round(l100 / 12, 2), "poup", round((poup - P) / 12, 2))
# 5 anos, taxas constantes, IR 15% no resgate
p5 = P * 1.006638 ** 60
c5_100 = P + (P * (1 + CDI) ** 5 - P) * 0.85
c5_110 = P + (P * (1 + CDI * 1.1) ** 5 - P) * 0.85
print("5 anos poup", round(p5), "cdb100", round(c5_100), "cdb110", round(c5_110), "dif110", round(c5_110 - p5), "dif100", round(c5_100 - p5))
