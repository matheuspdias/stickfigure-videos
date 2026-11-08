"""Contas do vídeo longo "Ganhei R$ 1.000 de aumento e só vieram R$ 475" (premissas conferidas em 08/11/2026).

Fontes:
- INSS 2026 (Portaria Interministerial MPS/MF nº 13/2026): 7,5% até 1.621,00; 9% até 2.902,84; 12% até 4.354,27;
  14% até 8.475,55 (teto). Salário mínimo 2026: R$ 1.621,00.
- IR 2026 (Lei 15.270/2025 + orientação da Receita Federal de dez/2025): tabela progressiva mensal
  (isento até 2.428,80; 7,5% até 2.826,65; 15% até 3.751,05; 22,5% até 4.664,68; 27,5% acima, parcela 908,73);
  redução mensal: até R$ 5.000 zera o imposto; de 5.000,01 a 7.350 redução = 978,62 - 0,133145 x rendimento tributável
  (exemplo oficial: R$ 6.000 -> redução 179,75). Vale também para o 13º. Desconto simplificado mensal 607,20
  (a fonte usa o que for maior: INSS ou simplificado).
- Declaração anual: até R$ 60 mil isento, redução parcial até R$ 88,2 mil (não detalhada no vídeo).
- FGTS 8% sobre salário, 13º e férias + 1/3 (depositado pela empresa, não sai do salário).
- INSS patronal: 20% da folha para empresas fora do Simples (fora RAT e terceiros), citado só como "pelo menos".
"""
FX = [(1621.00, .075), (2902.84, .09), (4354.27, .12), (8475.55, .14)]


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


def ir(bruto, inss_=None):
    if inss_ is None:
        inss_ = inss(bruto)
    base = bruto - max(inss_, 607.20)
    imp = ir_tabela(base)
    if bruto <= 5000:
        red = imp
    elif bruto <= 7350:
        red = max(0, 978.62 - 0.133145 * bruto)
    else:
        red = 0
    return round(max(0, imp - red), 2)


def liq(s):
    return round(s - inss(s) - ir(s), 2)


# conferência com o exemplo oficial da Receita (só desconto simplificado, sem INSS): 6.000 -> 394,54
b = 6000 - 607.20
print("exemplo Receita 6000 (simplificado):", round(ir_tabela(b), 2), round(978.62 - 0.133145 * 6000, 2), round(ir_tabela(b) - (978.62 - 0.133145 * 6000), 2))

print("\n== Lucas: 5.000 -> 6.000")
for s in (5000, 6000):
    print(f"  {s}: INSS {inss(s):.2f}  IR {ir(s):.2f}  líquido {liq(s):.2f}")
ganho = liq(6000) - liq(5000)
print(f"  ganho líquido {ganho:.2f} de 1000 -> fica {ganho/10:.1f}%, somem {1000-ganho:.2f}")
print(f"  INSS a mais {inss(6000)-inss(5000):.2f}; IR a mais {ir(6000)-ir(5000):.2f}")
print(f"  IR 6000 detalhe: base {6000-inss(6000):.2f} tabela {ir_tabela(6000-inss(6000)):.2f} redução {978.62-0.133145*6000:.2f}")

print("\n== aumento de 1.000 em cada salário")
for s in (2000, 3000, 4000, 5000, 6000, 7000, 8000, 10000, 15000):
    g = liq(s + 1000) - liq(s)
    print(f"  {s:>6} -> {s+1000:>6}: líquido {liq(s):9.2f} -> {liq(s+1000):9.2f}  fica {g:7.2f} ({g/10:.1f}%)")

print("\n== taxa marginal (cada 100 reais a mais)")
for s in (4800, 5200, 6000, 7000, 7400, 8000, 9000):
    print(f"  {s}: de cada 100 a mais ficam {liq(s+100)-liq(s):.2f}")
print(f"  teórico na faixa 5-7,35 mil (INSS 14%): somem {100*(0.14 + 0.86*0.275 + 0.133145):.1f}%")

print("\n== mito: aumento que faz ganhar menos")
for s in (4999, 5000, 5001, 5010, 5100, 7349, 7350, 7351):
    print(f"  {s}: IR {ir(s):.2f}  líquido {liq(s):.2f}")
ok = all(liq(s + 1) >= liq(s) for s in range(1600, 20000))
print("  líquido sempre sobe com o bruto (1.600 a 20.000, de 1 em 1 real):", ok)

print("\n== o ano inteiro (11 meses + férias com 1/3 + 13º + FGTS)")
def ano(s):
    fer = s * 4 / 3
    l13 = s - inss(s) - ir(s)          # 13º: tributação exclusiva, mesma tabela e redução
    return 11 * liq(s) + liq(fer) + l13, 0.08 * s * (12 + 1 + 1/3)
a5, f5 = ano(5000); a6, f6 = ano(6000)
print(f"  5000: líquido ano {a5:.2f}  FGTS {f5:.2f}")
print(f"  6000: líquido ano {a6:.2f}  FGTS {f6:.2f}")
print(f"  aumento no papel: 1000 x 13,33 = {1000*(13+1/3):.2f}")
print(f"  a mais no bolso no ano {a6-a5:.2f}; + FGTS {f6-f5:.2f} = {a6-a5+f6-f5:.2f}")
print(f"  férias 6000: bruto {8000:.2f} INSS {inss(8000):.2f} IR {ir(8000):.2f}; férias 5000: {6666.67} INSS {inss(6666.67):.2f} IR {ir(6666.67):.2f}")

print("\n== custo pra empresa (fora do Simples, mínimo): 1000 + 20% INSS patronal + 8% FGTS =", 1000 * 1.28)

print("\n== Lucas: plano de 1.000 x 474,90")
print(f"  em 12 meses só de contracheque: planejou {12000} recebe {12*ganho:.2f}")
