"""Contas do vídeo longo "CLT de R$ 5 mil ou PJ de R$ 7 mil? A conta completa" (premissas conferidas em 28/10/2026).

Fontes:
- INSS 2026 (Portaria Interministerial MPS/MF nº 13/2026): 7,5% até 1.621,00; 9% até 2.902,84; 12% até 4.354,27;
  14% até 8.475,55 (teto). Salário mínimo 2026: R$ 1.621,00. Contribuinte individual/pró-labore: 11%.
- IR 2026 (Lei 15.270/2025): tabela progressiva mensal (isento até 2.428,80 ... 27,5% acima de 4.664,68, parcela 908,73);
  redução: até R$ 5.000 zera o imposto; de 5.000,01 a 7.350 redução = 978,62 - 0,133145 x rendimento tributável.
  Vale também para o 13º (tributação exclusiva). Desconto simplificado mensal 607,20.
- Simples Nacional (LC 123/2006): Anexo III, 1ª faixa (RBT12 até 180 mil) 6%; Anexo V, 1ª faixa 15,5%;
  fator R = folha 12 meses / receita 12 meses >= 28% -> Anexo III.
- MEI: teto de R$ 81 mil em 2026 (PLP 186/2026 aprovado no Congresso em out/2026 eleva para 110 mil em 2027 e 140 mil em 2028);
  profissões intelectuais (programador, designer, advogado, médico...) não podem ser MEI.
- Seguro-desemprego 2026: teto R$ 2.518,65 (salário médio acima de 3.703,99), 5 parcelas com 24+ meses de carteira.
- FGTS 8% sobre salário, 13º e férias com 1/3; multa de 40% na demissão sem justa causa.
Exemplo: contador R$ 300/mês (valor ilustrativo). Benefícios ilustrativos: VR R$ 600 + plano de saúde R$ 400.
"""
FX = [(1621.00, .075), (2902.84, .09), (4354.27, .12), (8475.55, .14)]
SM = 1621.00


def inss(s):
    tot, ant = 0.0, 0.0
    for lim, a in FX:
        if s > ant:
            tot += (min(s, lim) - ant) * a
        ant = lim
    return round(tot, 2)


def ir_tabela(base):
    for lim, a, p in [(2428.80, 0, 0), (2826.65, .075, 182.16), (3751.05, .15, 394.16), (4664.68, .225, 675.49), (1e12, .275, 908.73)]:
        if base <= lim:
            return max(0.0, base * a - p)


def ir(bruto, inss_):
    base = bruto - max(inss_, 607.20)
    imp = ir_tabela(base)
    if bruto <= 5000:
        red = imp
    elif bruto <= 7350:
        red = max(0, 978.62 - 0.133145 * bruto)
    else:
        red = 0
    return round(max(0, imp - red), 2)


# ---------------- CLT
SAL = 5000.0
i_m = inss(SAL); r_m = ir(SAL, i_m); liq_m = SAL - i_m - r_m
FER = SAL * 4 / 3
i_f = inss(FER); r_f = ir(FER, i_f); liq_f = FER - i_f - r_f
liq_13 = SAL - inss(SAL) - ir(SAL, inss(SAL))
fgts = 0.08 * (12 * SAL + SAL + SAL / 3)
ano_clt = 11 * liq_m + liq_f + liq_13 + fgts
print(f"CLT: INSS {i_m}, IR {r_m}, líquido mensal {liq_m:.2f}")
print(f"  férias+1/3 {FER:.2f}: INSS {i_f}, IR {r_f}, líquido {liq_f:.2f}")
print(f"  13º líquido {liq_13:.2f}; FGTS do ano {fgts:.2f}")
print(f"  ANO CLT {ano_clt:.2f} = {ano_clt/12:.2f}/mês; só salário líquido x12 = {12*liq_m:.2f}; 'extras' = {ano_clt-12*liq_m:.2f}")
print(f"  bruto que a empresa registra no ano: 13,33 salários = {SAL*(13+1/3):.2f}")

# ---------------- PJ, Anexo III
FAT = 7000.0
CONT = 300.0
PL = max(0.28 * FAT, SM); i_pl = round(0.11 * PL, 2)
das3 = 0.06 * FAT
liq_pj = FAT - das3 - i_pl - CONT
print(f"\nPJ Anexo III: pró-labore {PL:.2f}, INSS {i_pl}, IR pró-labore {ir(PL, i_pl)}, DAS {das3:.2f}, contador {CONT}")
print(f"  líquido mensal {liq_pj:.2f}; 12 meses {12*liq_pj:.2f}")
ano_pj11 = 11 * (FAT - das3) - 12 * (i_pl + CONT)
print(f"  com 30 dias de férias sem faturar (11 faturas, pró-labore/INSS/contador 12 meses): {ano_pj11:.2f} = {ano_pj11/12:.2f}/mês")
print(f"  fator R nesse caso: {12*PL/(11*FAT):.1%}")
print(f"  diferença PJ - CLT: {ano_pj11-ano_clt:.2f}/ano = {(ano_pj11-ano_clt)/12:.2f}/mês")
print(f"  'parece' 2000 a mais por mês = 24000/ano; na mão no mês: {liq_pj - liq_m:.2f} a mais")

# ---------------- PJ, Anexo V (sem fator R, pró-labore de 1 salário mínimo)
i_sm = round(0.11 * SM, 2)
das5 = 0.155 * FAT
liq5 = FAT - das5 - i_sm - CONT
ano5 = 11 * (FAT - das5) - 12 * (i_sm + CONT)
print(f"\nPJ Anexo V: DAS {das5:.2f}, INSS {i_sm}, líquido mensal {liq5:.2f}; 12 meses {12*liq5:.2f}; com férias {ano5:.2f} ({ano5/12:.2f}/mês)")
print(f"  vs CLT: {ano5-ano_clt:.2f}")
print(f"  imposto Anexo V x Anexo III por ano (11 faturas): {11*(das5-das3):.2f}")


# ---------------- empate
def ano_pj(fat, anexo3=True):
    pl = max(0.28 * fat, SM) if anexo3 else SM
    das = (0.06 if anexo3 else 0.155) * fat
    return 11 * (fat - das) - 12 * (0.11 * pl + CONT)


def empate(alvo, anexo3=True):
    lo, hi = 3000, 30000
    for _ in range(80):
        m = (lo + hi) / 2
        if ano_pj(m, anexo3) < alvo:
            lo = m
        else:
            hi = m
    return m


e3 = empate(ano_clt); e5 = empate(ano_clt, False)
print(f"\nempate só no dinheiro: Anexo III {e3:.2f} ({e3/SAL-1:.1%} a mais); Anexo V {e5:.2f} ({e5/SAL-1:.1%})")
BEN = 12 * (600 + 400)
eb = empate(ano_clt + BEN)
print(f"com VR 600 + plano 400 (={BEN}/ano): empate Anexo III {eb:.2f} ({eb/SAL-1:.1%})")

# rede de proteção
seg = 5 * 2518.65
multa2 = 0.4 * 2 * fgts
print(f"\nseguro-desemprego 5 x 2.518,65 = {seg:.2f}; multa 40% do FGTS depois de 2 anos ~ {multa2:.2f} (sem correção)")
print(f"FGTS depositado em 2 anos ~ {2*fgts:.2f}")

# PJ sendo o próprio RH: quanto separar por mês pra ter férias, 13º e 'FGTS' próprios
sep = (liq_f - liq_m) + liq_13 + fgts   # o que a CLT dá além de 12 salários líquidos... mas o PJ precisa cobrir o mês sem faturar
print(f"extras CLT além de 12 salários líquidos: {ano_clt-12*liq_m:.2f} -> {(ano_clt-12*liq_m)/12:.2f}/mês")
mes_ferias = FAT - das3          # o PJ deixa de faturar
print(f"PJ: para tirar 30 dias, precisa ter separado ~ um mês de líquido: {liq_pj:.2f} -> {liq_pj/11:.2f} por mês nos outros 11")
print(f"aposentadoria: CLT contribui sobre {SAL}, PJ sobre {PL:.2f} ({PL/SAL:.0%})")
print(f"INSS pago no ano: CLT {12*i_m + i_f - i_m + inss(SAL):.2f}... PJ {12*i_pl:.2f}")
