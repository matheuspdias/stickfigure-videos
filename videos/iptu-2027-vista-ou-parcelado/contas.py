"""IPTU à vista (3%) x 10 parcelas sem juros (regra de SP em 2026; a de 2027 sai em jan/fev). Conferido em 15/11/2026.
- IPTU de R$ 1.500 -> à vista R$ 1.455 (economia R$ 45); parcelado 10 x R$ 150 (fev a nov).
- CDI 13,65% a.a.; IR 22,5% (conservador, mesmo para resgates de mais de 180 dias).
"""
iptu = 1500
desc = iptu * 0.03
print("à vista", iptu - desc, "| economia", desc, "| parcela", iptu / 10)
m = ((1.1365) ** (1 / 12) - 1) * (1 - 0.225)
saldo, rend = iptu - 150, 0.0
for _ in range(9):
    r = saldo * m; rend += r; saldo = saldo + r - 150
print("rendimento parcelando %.1f (vs desconto %.0f) | sobra final %.1f" % (rend, desc, saldo))
def vp(i): return sum(150 / (1 + i) ** k for k in range(10))
lo, hi = 0.0, 0.1
for _ in range(60):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if vp(mid) > iptu - desc else (lo, mid)
print("juros embutido no parcelado %.2f%% ao mês | rendimento líquido %.2f%% ao mês" % (mid * 100, m * 100))
# IPVA da Parte 1: 5 parcelas -> juros embutido 1,5%/mês (o desconto ganhou)
