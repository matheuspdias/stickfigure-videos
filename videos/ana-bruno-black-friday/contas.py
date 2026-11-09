# Black Friday: TV de R$ 3.000, à vista -10% ou 10x sem juros com o dinheiro rendendo
# Rendimento: ~14% a.a. (Selic na casa de 13,75-14,25% em 2026), IR 22,5% (até 180 dias, simplificado sobre o saldo final)
m = 1.14 ** (1/12) - 1
saldo = 3000
for _ in range(10):
    saldo = saldo * (1 + m) - 300
liquido = saldo * (1 - 0.225)
print(f"mensal {m:.4f}  sobra bruta {saldo:.0f}  liquida {liquido:.0f}")   # ~193 / ~150
for d in (0.03, 0.05, 0.10):
    print(d, 3000 * d)   # 90 / 150 / 300 -> empate perto de 5%
