# Black Friday: TV de R$ 3.000, à vista -10% ou 10x sem juros com o dinheiro rendendo
# Rendimento: CDB ~100% do CDI com Selic 13,75% (Copom 04/11/2026) -> ~1,07% ao mês; IR 22,5% (até 180 dias, simplificado sobre o ganho)
m = (1 + 0.1375 * 0.99) ** (1/12) - 1
saldo = 3000
for _ in range(10):
    saldo = saldo * (1 + m) - 300
liquido = saldo * (1 - 0.225)
print(f"mensal {m:.4f}  sobra bruta {saldo:.0f}  liquida {liquido:.0f}")   # ~188 / ~146 -> "uns cento e cinquenta"
for d in (0.03, 0.05, 0.10):
    print(d, 3000 * d)   # 90 / 150 / 300 -> empate perto de 5% (146/3000 = 4,9%)
