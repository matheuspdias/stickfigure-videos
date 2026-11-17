# O que muda pra comprar imóvel em 2027 (juros dos bancos em nov/2026). Fontes: Exame 27/10/2026, Gazeta Brasil 12/11/2026 (MySide),
# Caixa 13/11/2026 (estuda subir), novo modelo SBPE (jan/2027; teto 12% a.a. + TR no SFH até R$ 2,25 mi; bancos/CBIC pedem adiar).
# Taxas mínimas SBPE a.a. (sem TR): Bradesco 11,69 -> 15,00; Itaú 11,99 -> 12,95; Santander 11,69 -> 12,49; BB 11,60; Caixa 11,19.
# SAC 30 anos (360 meses), sem TR, seguros e tarifas (mesma base da reportagem).
def parc1(P, a):
    i = (1 + a) ** (1/12) - 1
    return P / 360 + P * i
for nome, a in [("Caixa", .1119), ("BB", .116), ("Bradesco antes", .1169), ("Santander", .1249), ("Itaú", .1295), ("Bradesco", .15)]:
    print(f"{nome:15s} {a*100:.2f}%  R$500 mil: 1a parcela {parc1(500000, a):,.0f}")
# renda de R$ 10 mil: parcela máx 30% = R$ 3.000 -> quanto o banco financia
renda = 10000; lim = 0.30 * renda
for nome, a in [("antes 11,69%", .1169), ("Bradesco 15%", .15), ("Caixa 11,19%", .1119), ("teto SFH 12%", .12)]:
    P = lim / parc1(1, a)
    print(f"{nome:14s} financia até {P:,.0f}")
a0, a1 = .1169, .15
print("diferença de crédito:", f"{lim/parc1(1,a0) - lim/parc1(1,a1):,.0f}", f"({(1 - parc1(1,a0)/parc1(1,a1))*100:.0f}% a menos)")
# mesma parcela de R$ 3.000: renda necessária para R$ 300 mil
for a in (.1169, .15):
    p = parc1(300000, a); print(f"{a*100:.2f}%: 1a parcela de R$300 mil = {p:,.0f}; renda mínima (30%) = {p/0.3:,.0f}")
# juros pagos no total, SAC R$ 300 mil, 30 anos
def juros_tot(P, a):
    i = (1 + a) ** (1/12) - 1; am = P/360; s=P; j=0
    for _ in range(360): j += s*i; s -= am
    return j
for a in (.1169, .15): print(f"{a*100:.2f}% juros totais R$300 mil: {juros_tot(300000,a):,.0f}")
