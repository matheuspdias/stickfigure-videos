# Pagar aluguel é jogar dinheiro fora? Versão Minha Casa Minha Vida (pedido do Matheus: o dele é R$ 298 mil, parcela ~R$ 1.900)
# Premissas (redondas): MCMV faixa 3, ~8% a.a., tabela Price, 35 anos (420 meses), entrada R$ 30 mil (10%);
# parcela ~R$ 1.850 + seguros/taxa ~R$ 50 = ~R$ 1.900. Aluguel do mesmo apê: 0,5% do valor (R$ 1.500), +4,5%/ano.
# Imóvel valoriza 5%/ano. Investimento 0,8%/mês líquido (~10% a.a.).
V = 298000; entrada = 30000; fin = V - entrada; n = 420
i = 1.08 ** (1/12) - 1; r = 0.008
pmt = fin * i / (1 - (1 + i) ** -n)
parcela = pmt + 50
for anos in (10, 20):
    saldo = fin; ana = entrada; ana_gasta = entrada; aluguel = 1500; pago = 0
    for mes in range(12 * anos):
        saldo = saldo * (1 + i) - pmt
        if mes and mes % 12 == 0: aluguel *= 1.045
        ana = ana * (1 + r) + (parcela - aluguel)
        ana_gasta = ana_gasta * (1 + r)
        pago += parcela
    imovel = V * 1.05 ** anos
    print(f"{anos} anos | parcela {parcela:.0f} | aluguel final {aluguel:.0f} | Bruno: imóvel {imovel:.0f} - dívida {saldo:.0f} = {imovel - saldo:.0f}"
          f" | Ana investindo {ana:.0f} | Ana gastando a diferença {ana_gasta:.0f} | Bruno pagou {pago:.0f}")
