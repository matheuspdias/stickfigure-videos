# Mesmo apartamento, 3 rendas: quem ganha um pouco mais paga mais caro (2026/2027). Pedido do Matheus em 17/11/2026.
# Apê R$ 350 mil, entrada 20% (R$ 70 mil), financia R$ 280 mil. SAC, 1a parcela sem TR/seguros/tarifas.
# MCMV (tabela 2026, valorfinal 07/11/2026; myside 12/08/2026): Faixa 3 (R$ 5.000,01-9.600) 7,66% cotista FGTS / 8,16%, teto R$ 400 mil, 420 meses;
#   Faixa 4 (até R$ 13.000) 10% a.a., teto R$ 600 mil, 420 meses.
# Fora do MCMV (SBPE, taxas mínimas nov/2026, Gazeta Brasil 12/11): Caixa 11,19%, BB 11,60%, Santander 12,49%, Itaú 12,95%, Bradesco 15% (+TR), 360 meses.
# 2027: novo modelo da poupança, teto 12% a.a. + TR no SFH (até R$ 2,25 mi); bancos pedem adiar/rever; Caixa estuda subir (13/11).
def sac1(P, a, n):
    i = (1 + a) ** (1/12) - 1; return P / n + P * i
def juros_tot(P, a, n):
    i = (1 + a) ** (1/12) - 1; am = P / n; s = P; j = 0
    for _ in range(n): j += s * i; s -= am
    return j
P = 280000
casos = [("Ana R$ 9 mil, F3", .0766, 420), ("Bruno R$ 12 mil, F4", .10, 420), ("Carla R$ 14 mil, Caixa", .1119, 360),
         ("Carla R$ 14 mil, Bradesco", .15, 360), ("Carla com teto 12%", .12, 360)]
for nome, a, n in casos:
    print(f"{nome:26s} 1a parcela {sac1(P,a,n):6,.0f}  juros totais {juros_tot(P,a,n):9,.0f}")
print("Carla Bradesco - Ana:", round(sac1(P,.15,360) - sac1(P,.0766,420)), "/mês;", round(juros_tot(P,.15,360) - juros_tot(P,.0766,420)), "de juros")
print("R$ 13.100 (sai da F4): +", round(sac1(P,.1119,360) - sac1(P,.10,420)), "a +", round(sac1(P,.15,360) - sac1(P,.10,420)), "/mês")
