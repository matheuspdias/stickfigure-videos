"""Contas do vídeo "R$ 10 por dia vira R$ 1 milhão? A conta completa" (premissas conferidas em 01/11/2026).

Premissas
- R$ 10 por dia = R$ 300 por mês (30 dias), aportados no fim de cada mês.
- Rendimento: 0,8% ao mês líquido de imposto (~10,03% ao ano), constante (mesma premissa dos vídeos
  "primeiros 100 mil" e do TikTok "dez reais por dia"). Referência de hoje: Selic 13,75% (Copom 16/09/2026),
  CDI ~13,65%; CDB 100% CDI com IR de 15% (acima de 720 dias) = ~11,6% a.a. líquido. Tesouro IPCA+ 2050 a
  IPCA + 7,24% (30/10/2026). Ou seja, 0,8% a.m. é mais conservador que os juros de hoje, que não devem durar 35 anos.
- IR renda fixa: tabela regressiva vigente (15% acima de 720 dias). Já embutido na taxa líquida.
- Inflação: 4% ao ano constante (IPCA 12 meses até set/2026: 4,58%; meta 3%).
"""
i = 0.008
INF = 0.04
APORTE = 300.0

def fv(aporte, meses, taxa=i):
    return aporte * ((1 + taxa) ** meses - 1) / taxa

def br(x):
    return f"R$ {x:,.0f}".replace(",", ".")

print("taxa anual equivalente:", round(((1 + i) ** 12 - 1) * 100, 2), "%")
print("CDB 100% CDI liquido 15%:", round(13.65 * 0.85, 2), "% a.a.")

# 1. conta principal
for anos in (5, 10, 20, 25, 30, 35):
    n = anos * 12
    print(f"{anos:2d} anos: {br(fv(APORTE, n))}  do bolso {br(APORTE * n)}  juros {fv(APORTE,n)/1 - APORTE*n:,.0f}")
n = 1
while fv(APORTE, n) < 1_000_000:
    n += 1
print("1 milhão no mês", n, "=", n // 12, "anos e", n % 12, "meses")
f35 = fv(APORTE, 420)
print("juros/total aos 35:", round((f35 - 126000) / f35 * 100, 1), "%")
print("anos 30-35 somam:", br(f35 - fv(APORTE, 360)), " primeiros 25 anos:", br(fv(APORTE, 300)))
# quanto o dinheiro rende por mes no fim
print("rendimento do mês 420:", br(fv(APORTE, 419) * i))
# primeiros 100 mil
n = 1
while fv(APORTE, n) < 100_000: n += 1
print("100 mil no mês", n, n/12)

# 2. inflação
defl35 = (1 + INF) ** 35
print("deflator 35 anos:", round(defl35, 3), " 1 milhão vale hoje:", br(1_000_000 / defl35), " f35 hoje:", br(f35 / defl35))
print("R$ 10 daqui a 35 anos (preço do lanche):", round(10 * defl35, 2))

# 3. aporte reajustado pela inflação todo ano
def fv_reaj(aporte0, anos, taxa=i, inf=INF):
    s = 0.0
    a = aporte0
    for m in range(1, anos * 12 + 1):
        s = s * (1 + taxa) + a
        if m % 12 == 0:
            a *= (1 + inf)
    return s, a
for anos in (30, 35):
    s, a = fv_reaj(APORTE, anos)
    d = (1 + INF) ** anos
    print(f"reaj {anos}a: nominal {br(s)}  em dinheiro de hoje {br(s/d)}  ultimo aporte mensal {a/(1+INF):.0f} (por dia {a/(1+INF)/30:.2f})")
s, a = fv_reaj(APORTE, 35)
# do bolso nominal
tot = 0; a2 = APORTE
for m in range(1, 421):
    tot += a2
    if m % 12 == 0: a2 *= 1 + INF
print("do bolso nominal reajustado 35a:", br(tot))
# aporte por dia (reajustado) para 1 milhão de hoje em 35 anos
alvo_nom = 1_000_000 * defl35
base, _ = fv_reaj(1.0, 35)
print("para 1 milhão DE HOJE em 35 anos: por mês", round(alvo_nom / base), "por dia", round(alvo_nom / base / 30, 2))
base30, _ = fv_reaj(1.0, 30)
print("para 1 milhão DE HOJE em 30 anos: por dia", round(1_000_000 * (1+INF)**30 / base30 / 30, 2))

# 4. Ana x Bruno
# Ana: dos 25 aos 35 guarda R$10/dia (120 meses) e para; deixa rendendo até 60.
# Bruno: começa aos 35 e guarda R$10/dia até os 60 (300 meses).
ana35 = fv(APORTE, 120)
ana60 = ana35 * (1 + i) ** 300
bru60 = fv(APORTE, 300)
print("Ana aos 35:", br(ana35), " aos 60:", br(ana60), " do bolso", br(APORTE*120))
print("Bruno aos 60:", br(bru60), " do bolso", br(APORTE*300))
# Ana continua até 60 (35 anos)
print("Ana se continuasse até os 60:", br(fv(APORTE, 420)))
# quanto Bruno precisaria por dia para empatar com Ana-que-parou
print("Bruno precisaria por dia:", round(ana60 / fv(1, 300) / 30, 2))
# Bruno pra empatar com Ana-que-continuou
print("Bruno p/ empatar com Ana que continuou, por dia:", round(fv(APORTE, 420) / fv(1, 300) / 30, 2))

# 5. quanto por dia para 1 milhão (nominal) em X anos
for anos in (15, 20, 25, 30, 35):
    print(f"1 milhão em {anos} anos: por mês {1e6/fv(1, anos*12):,.0f}  por dia {1e6/fv(1, anos*12)/30:,.2f}")

# 6. custo de esperar 1 ano / sacar
print("começando 5 anos depois (30 anos):", br(fv(APORTE, 360)), " perda:", br(f35 - fv(APORTE, 360)))

# 7. poupança (Selic > 8,5%: 0,5% a.m. + TR; TR ~0,167% a.m. em 2026, isenta de IR)
ip = 1.005 * 1.00167 - 1
print("poupança a.m.:", round(ip * 100, 4), "% a.a.:", round(((1 + ip) ** 12 - 1) * 100, 2))
fp = fv(APORTE, 420, ip)
print("poupança 35 anos:", br(fp), " diferença p/ 0,8%:", br(f35 - fp))
n = 1
while fv(APORTE, n, ip) < 1_000_000: n += 1
print("poupança chega a 1 milhão no mês", n, "=", n // 12, "anos e", n % 12, "meses")
# poupança com TR zero (regra de longo prazo mais conservadora)
fp0 = fv(APORTE, 420, 0.005)
print("poupança TR zero 35 anos:", br(fp0))
