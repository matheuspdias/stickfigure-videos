"""Contas do Quanto rende R$ 10 mil em 1 ano (Parte 3 de 3). Mesmas taxas das Partes 1 e 2 (19/11/2026):
Selic 13,75%, CDI 13,65% a.a., poupança 0,6638% a.m. (isenta); IR 17,5% (361-720 dias), 15% (>720 dias)."""
P = 10000
CDI = 0.1365
poup = P * 1.006638 ** 12
b100 = P * CDI; l100 = b100 * 0.825
b110 = b100 * 1.1; l110 = b110 * 0.825
print("poup", round(poup), "cdb100 bruto", b100, "IR", round(b100 * .175, 2), "->", round(P + l100), "cdb110 ->", round(P + l110))
print("por mes", round(l100 / 12, 2), round((poup - P) / 12, 2), "dif ano", round(l100 - (poup - P)))
# salário mínimo 2026 R$ 1.621; rendimento anual líquido (IR 15%) / 12
print("pra render 1 minimo/mes", round(1621 / (CDI * 0.85 / 12)))
