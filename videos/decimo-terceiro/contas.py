"""Contas do vídeo do 13º (premissas conferidas em 19/10/2026)."""
SELIC = 0.1375          # Copom 16/9/2026
IPCA = 0.0458           # 12 meses até set/2026 (IBGE)
ROTATIVO = 4.449        # 444,9% a.a., ago/2026 (BC)
PARCELADO = 1.921       # 192,1% a.a., ago/2026 (BC)
REAL = 0.05             # premissa do canal: 5% a.a. acima da inflação, já com imposto
INSS = [(1621.00, .075), (2902.84, .09), (4354.27, .12), (8475.55, .14)]  # tabela 2026

def inss(s):
    tot, ant = 0, 0
    for teto, a in INSS:
        if s > ant:
            tot += (min(s, teto) - ant) * a
        ant = teto
    return tot

sal = 3000
print("1a parcela:", sal / 2)
d = inss(sal); print(f"INSS sobre 13º de {sal}: {d:.2f}; 2a parcela {sal/2 - d:.2f}; líquido total {sal - d:.2f}")
liq = round(sal - d, -1)
print("13º líquido arredondado:", liq)

m_rot = (1 + ROTATIVO) ** (1 / 12) - 1; m_par = (1 + PARCELADO) ** (1 / 12) - 1; m_sel = (1 + SELIC) ** (1 / 12) - 1
print(f"rotativo {m_rot:.2%}/mês, parcelado {m_par:.2%}/mês, selic {m_sel:.2%}/mês, razão rot/selic {m_rot/m_sel:.1f}x, par/selic {m_par/m_sel:.1f}x")
# dívida de 2.750 no parcelado do cartão por 12 meses (sem o teto) e com teto de 100%
print(f"2750 no parcelado 12m sem teto: {2750*(1+PARCELADO):.0f}; com teto da lei: {2750*2:.0f}")
# juros pagos por mês numa dívida de 2.750 no parcelado
print(f"juros 1º mês no parcelado sobre 2750: {2750*m_par:.0f}; no rotativo: {2750*m_rot:.0f}")
# reserva: 2.750 no Tesouro Selic por 1 ano, IR 17,5% (361-720 dias)
bruto = 2750 * SELIC; liq1 = bruto * (1 - .175)
print(f"reserva 1 ano: bruto {bruto:.0f}, líquido {liq1:.0f}, acima da inflação {liq1 - 2750*IPCA:.0f}")
# investir só o 13º todo ano a 5% real
for n in (10, 20, 30):
    fv = liq * ((1 + REAL) ** n - 1) / REAL
    print(f"13º de {liq:.0f} por {n} anos a 5% real: {fv:,.0f} (aportado {liq*n:,.0f})")
# renda mensal possível com o acumulado de 30 anos pela regra dos 4%
fv30 = liq * ((1 + REAL) ** 30 - 1) / REAL
print(f"renda pela regra dos 4% com 30 anos: {fv30*0.04/12:,.0f}/mês")
# Ana x Bruno: Ana investe 80% do 13º e gasta 20%
for n in (10, 20, 30):
    fv = 0.8 * liq * ((1 + REAL) ** n - 1) / REAL
    print(f"80% do 13º ({0.8*liq:.0f}) por {n} anos: {fv:,.0f}")
