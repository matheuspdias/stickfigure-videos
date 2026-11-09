# Pagar aluguel é jogar dinheiro fora? Ana aluga e investe, Bruno financia. Apê de R$ 300 mil, 10 anos.
# Premissas (redondas): aluguel 0,5% do valor (R$ 1.500), reajuste 4,5%/ano; imóvel valoriza 5%/ano;
# financiamento SAC 30 anos, 12% a.a. efetivos (11-12% + TR em 2026), entrada 20%; investimento 0,8%/mês líquido (~10% a.a.).
V = 300000; entrada = 0.2 * V; fin = V - entrada; n = 360
i = 1.12 ** (1/12) - 1; r = 0.008
amort = fin / n
saldo_dev = fin; ana = entrada; aluguel = 1500
parc0 = amort + saldo_dev * i
tot_bruno = 0
for mes in range(120):
    parc = amort + saldo_dev * i
    saldo_dev -= amort
    if mes and mes % 12 == 0: aluguel *= 1.045
    ana = ana * (1 + r) + (parc - aluguel)
    tot_bruno += parc
imovel = V * 1.05 ** 10
print(f"1a parcela {parc0:.0f}  ultima {parc:.0f}  aluguel final {aluguel:.0f}")
print(f"Bruno: imovel {imovel:.0f} - divida {saldo_dev:.0f} = {imovel - saldo_dev:.0f}")
print(f"Ana investido: {ana:.0f}")
# cenário: Ana não investe a diferença (gasta)
ana2 = entrada * (1 + r) ** 120
print(f"Ana se gastar a diferença: {ana2:.0f}")
