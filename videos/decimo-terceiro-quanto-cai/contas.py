"""Contas do TikTok "Quanto vai cair de verdade no seu 13º" (conferidas em 02/11/2026).
Premissas: salário fixo, 12 meses trabalhados, sem dependentes, sem pensão.
- Salário mínimo 2026: R$ 1.621,00
- INSS 2026 (progressivo): 7,5% até 1.621,00; 9% até 2.902,84; 12% até 4.354,27; 14% até 8.475,55
- IRRF 13º: tributação exclusiva na fonte, base = 13º - INSS (- dependentes).
  Tabela mensal: isento até 2.428,80; 7,5% (-182,16) até 2.826,65; 15% (-394,16) até 3.751,05;
  22,5% (-675,49) até 4.664,68; 27,5% (-908,73) acima.
  Redução Lei 15.270/2025 (vale para o 13º, segundo a Receita): até 5.000 de rendimento zera o imposto;
  5.000,01 a 7.350: redução = 978,62 - 0,133145 x rendimento; acima de 7.350 nenhuma.
- 1ª parcela: até 30/11, metade do salário do mês anterior, sem desconto (Decreto 57.155/65, art. 3º).
- 2ª parcela: até 20/12 (domingo em 2026, então até sexta 18/12): 13º cheio sobre dezembro + médias,
  menos a 1ª, menos INSS e IR sobre o 13º cheio.
"""
INSS = [(1621.00, .075), (2902.84, .09), (4354.27, .12), (8475.55, .14)]
IR = [(2428.80, 0, 0), (2826.65, .075, 182.16), (3751.05, .15, 394.16), (4664.68, .225, 675.49), (1e12, .275, 908.73)]


def r2(x):
    return round(x + 1e-9, 2)


def inss(s):
    tot, ant = 0, 0
    for teto, a in INSS:
        if s > ant:
            tot += (min(s, teto) - ant) * a
        ant = teto
    return r2(tot)


def irrf(bruto, inss_v):
    base = bruto - inss_v
    imp = 0
    for teto, a, ded in IR:
        if base <= teto:
            imp = base * a - ded
            break
    imp = max(r2(imp), 0)
    if bruto <= 5000:
        red = imp
    elif bruto <= 7350:
        red = min(imp, r2(978.62 - 0.133145 * bruto))
    else:
        red = 0
    return r2(imp - red)


def parcelas(total13, primeira):
    i = inss(total13); ir = irrf(total13, i)
    seg = r2(total13 - primeira - i - ir)
    return i, ir, seg


if __name__ == "__main__":
    print("TABELA (salário fixo)")
    for s in (1621, 2000, 3000, 5000, 8000):
        p1 = r2(s / 2); i, ir, p2 = parcelas(s, p1)
        print(f"{s:>6}: 1a {p1:>8.2f} | INSS {i:>7.2f} IR {ir:>8.2f} | 2a {p2:>8.2f} | total {p1+p2:>8.2f}")
    # conferência das faixas do INSS pela fórmula com parcela a deduzir
    assert inss(3000) == 248.60 and inss(5000) == 501.51 and inss(8000) == 921.51
    print("\nEXEMPLO: salário 2.500 + insalubridade 20% do mínimo + média de horas extras 500")
    sal, ins, he = 2500, r2(0.20 * 1621), 500
    p1 = r2((sal + ins) / 2)        # metade do salário de outubro (salário + insalubridade, sem as médias)
    tot = sal + ins + he
    i, ir, p2 = parcelas(tot, p1)
    print(f"insalubridade {ins}; 13º cheio {tot:.2f}; 1a {p1}; INSS {i}; IR {ir}; 2a {p2}; total {p1+p2:.2f}; 2a-1a {p2-p1:.2f}")
    print(f"horas extras/mês aprox. (HE 50%, 220h): {he/(sal/220*1.5):.0f} h")
