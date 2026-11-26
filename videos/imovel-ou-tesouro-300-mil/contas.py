"""Contas de "Apê de R$ 300 mil pra alugar x R$ 300 mil no Tesouro" (26/11/2026).
Aluguel: R$ 1.900 (cenário favorável ao apê, 7,6% a.a.; média FipeZAP ~6,13% a.a. = ~R$ 1.530; 1 dorm 6,78%; Recife 8,47%).
Custos do apê: 1 mês vazio por ano + R$ 150/mês de conserto/manutenção. IR do aluguel fora (depende da renda da pessoa).
Tesouro Selic: Selic 13,75%, custódia 0,20%, IR 15% (mais de 2 anos). Valorização do imóvel: ~5,5% em 12 meses (FipeZAP venda)."""
alug = 1900
ana_mes = alug * 11 / 12 - 150
selic, cust, ir = 0.1375, 0.002, 0.15
liq = (selic - cust) * (1 - ir)
bruno_mes = 300000 * ((1 + liq) ** (1 / 12) - 1)
val = 300000 * 0.055
print(f"Ana/mês {ana_mes:.0f} | Bruno/mês {bruno_mes:.0f} ({liq*100:.2f}% a.a.) | diferença/mês {bruno_mes-ana_mes:.0f}")
print(f"ano: Ana aluguel {ana_mes*12:.0f} + valorização {val:.0f} = {ana_mes*12+val:.0f} | Bruno {bruno_mes*12:.0f}")
print(f"média FipeZAP 6,13%: {300000*0.0613/12:.0f}/mês")
