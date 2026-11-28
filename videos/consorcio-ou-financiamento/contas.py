# Consórcio x financiamento, carro de R$ 80 mil, 60 meses (nov/2026)
# Fontes: BC taxa média aquisição de veículos PF ~26,4% a.a. (~1,9-2,0% a.m.);
# taxa de administração consórcio auto 15% a 20% (usamos 18%, com fundo de reserva).
V, N = 80000, 60
i = 0.019
parc_fin = V * i / (1 - (1 + i) ** -N)
tot_fin = parc_fin * N
print(f"Financiamento: parcela {parc_fin:.0f}  total {tot_fin:.0f}  juros {tot_fin-V:.0f}")
taxa = 0.18
parc_cons = V * (1 + taxa) / N
tot_cons = parc_cons * N
reaj = 0.045  # reajuste anual da carta (preço do carro)
tot_cons_reaj = sum(parc_cons * (1 + reaj) ** (m // 12) for m in range(N))
print(f"Consórcio: parcela {parc_cons:.0f}  total {tot_cons:.0f}  com reajuste {tot_cons_reaj:.0f}")
print(f"Diferença c/ reajuste {tot_fin-tot_cons_reaj:.0f}")
# guardar a parcela do consórcio rendendo ~0,9% a.m. líquido, carro subindo 4,5% a.a.
s, m = 0, 0
while True:
    m += 1
    s = s * 1.009 + parc_cons
    preco = V * (1 + reaj) ** (m / 12)
    if s >= preco:
        break
print(f"Guardando {parc_cons:.0f}/mês: compra à vista no mês {m} (preço {preco:.0f})")
