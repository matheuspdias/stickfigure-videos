"""IPVA 2027 em SP: à vista com 3% em janeiro x 5 parcelas sem juros (jan a mai). Conferido em 14/11/2026.
Fonte: calendário da Sefaz-SP (Decreto 70.960/2026), noticiado por CNN Brasil, InfoMoney etc.
- Alíquota de carro em SP: 4% do valor venal. Carro de R$ 50 mil -> IPVA R$ 2.000.
- CDI 13,65% a.a.; IR 22,5% (aplicação de até 180 dias) -> rendimento líquido ao mês.
"""
ipva = 50000 * 0.04
desc = ipva * 0.03
print("IPVA", ipva, "| à vista", ipva - desc, "| economia", desc, "| parcela", ipva / 5)
m = ((1.1365) ** (1 / 12) - 1) * (1 - 0.225)
print("rend. líquido mês %.4f" % m)
# parcelado: guarda os 2000 (menos a 1a parcela paga em jan), paga 400/mês fev..mai
saldo, rend = ipva - 400, 0.0
for _ in range(4):
    r = saldo * m; rend += r; saldo = saldo + r - 400
print("rendimento total parcelando %.1f (vs desconto %.0f)" % (rend, desc))
# taxa implícita: pagar 1940 agora vs 400 x5 (jan..mai)
import numpy as np
def vp(i): return sum(400 / (1 + i) ** k for k in range(5))
lo, hi = 0.0, 0.1
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if vp(mid) > 1940 else (lo, mid)
print("juros embutido no parcelado %.2f%% ao mês" % (mid * 100))
# se pagar à vista no cartão/cheque especial: rotativo ~ 15%/mês? (só citado: "o desconto some")
