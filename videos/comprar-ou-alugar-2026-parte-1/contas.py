# Comprar ou alugar em 2026 (Parte 1 de 3): a conta do primeiro mês.
# Apê de R$ 300 mil. Aluguel 0,5% do valor/mês (~6% a.a., perto da rentabilidade média do FipeZap) = R$ 1.500.
# Financiamento SAC 30 anos (360 meses), entrada 20% (R$ 60 mil), ~12% a.a. efetivos com TR (bancos em 2026: ~11-12% + TR).
# Entrada parada no CDI: Selic 13,75% (Copom 04/11/2026), CDI ~13,65% a.a., IR 15% (longo prazo).
# Valorização do imóvel ~5% a.a. (premissa da série; FipeZap venda 2026 perto da inflação).
V = 300_000; ent = 0.2 * V; fin = V - ent
i = 1.12 ** (1/12) - 1
amort = fin / 360
juros1 = fin * i
parc1 = amort + juros1
cdi = 0.1365; liq = cdi * 0.85
rend_ent = ent * ((1 + liq) ** (1/12) - 1)
valoriz = V * (1.05 ** (1/12) - 1)
print(f"taxa mensal {i*100:.3f}%")
print(f"1a parcela {parc1:.0f} = amortização {amort:.0f} + juros {juros1:.0f} ({juros1/parc1*100:.0f}% juros)")
print(f"juros / aluguel = {juros1/1500:.2f}")
print(f"rendimento perdido da entrada/mês {rend_ent:.0f}")
print(f"custo 'que não volta' comprando: juros+rend = {juros1+rend_ent:.0f}  x aluguel 1500")
print(f"valorização do imóvel/mês ~{valoriz:.0f}")
print(f"custo líquido comprando (juros + rend - valoriz) {juros1+rend_ent-valoriz:.0f}")
print(f"diferença parcela - aluguel {parc1-1500:.0f}")
