"""Contas do TikTok "Vai tirar férias? Cuidado com o mês seguinte" (conferidas em 05/11/2026).
Premissas: CLT, 30 dias de férias gozadas, salário fixo, sem dependentes, sem pensão.
- Salário mínimo 2026: R$ 1.621,00
- Férias (CLT art. 142 e CF art. 7º, XVII): salário dos 30 dias + 1/3. Pagas até 2 dias antes do início (CLT art. 145).
- INSS 2026 (progressivo): 7,5% até 1.621,00; 9% até 2.902,84; 12% até 4.354,27; 14% até 8.475,55.
  Simplificação: INSS sobre o valor cheio das férias (como as calculadoras; se as férias pegam dois meses,
  a folha divide por competência e os centavos mudam).
- IRRF das férias: calculado em separado do salário do mês, base = férias + 1/3 - INSS (ou desconto simplificado
  de R$ 607,20, o que for melhor). Tabela mensal 2026 + redução da Lei 15.270/2025 sobre o rendimento bruto:
  até 5.000 zera; 5.000,01 a 7.350: redução = 978,62 - 0,133145 x rendimento.
  Atenção: com salário de 5 mil, férias + 1/3 = 6.666,67, então passa de 5 mil e tem IR (pouco).
- Abono pecuniário (art. 143): vender até 1/3 (10 de 30 dias), pedido até 15 dias antes do fim do período
  aquisitivo; abono sem INSS e sem IR (o 1/3 sobre o abono tem IR segundo a Receita; com o redutor, só importa acima de 5 mil).
- 1ª parcela do 13º nas férias (Lei 4.749/65, art. 2º, §2º): metade do salário, se pedir em janeiro.
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


def irrf(bruto, ded):
    base = bruto - max(ded, 607.20)
    imp = 0
    for teto, a, d in IR:
        if base <= teto:
            imp = base * a - d
            break
    imp = max(r2(imp), 0)
    if bruto <= 5000:
        red = imp
    elif bruto <= 7350:
        red = min(imp, r2(978.62 - 0.133145 * bruto))
    else:
        red = 0
    return r2(imp - red)


def ferias(s):
    bruto = r2(s * 4 / 3); i = inss(bruto); ir = irrf(bruto, i)
    return bruto, i, ir, r2(bruto - i - ir)


def salario(s):
    i = inss(s); ir = irrf(s, i)
    return i, ir, r2(s - i - ir)


if __name__ == "__main__":
    print("FÉRIAS 30 DIAS (líquido)  |  salário normal líquido")
    for s in (1621, 2000, 3000, 5000):
        b, i, ir, liq = ferias(s); _, _, ls = salario(s)
        print(f"{s:>6}: bruto {b:>9.2f} INSS {i:>7.2f} IR {ir:>6.2f} -> líquido {liq:>9.2f} | salário líquido {ls:>8.2f}")
    assert inss(3000) == 248.60
    print("\nVIRADA: R$ 3 mil, férias de 16/jun a 15/jul, volta dia 16 (mês comercial de 30 dias)")
    s = 3000; _, _, liq_normal = salario(s)
    meio = r2(s / 2); i_meio = r2(inss(s) / 2)
    print(f"salário normal líquido {liq_normal}; próximo pagamento: 15 dias = {meio} bruto, ~{r2(meio - i_meio)} líquido")
    b, i, ir, liq = ferias(s)
    print(f"férias líquidas {liq}: salário do mês adiantado {s} + terço {r2(s/3)} - INSS {i}")
    print("\nOPÇÕES (R$ 3 mil)")
    dia = s / 30
    ab = r2(dia * 10 * 4 / 3)          # abono + 1/3, sem INSS (e sem IR nessa faixa)
    f20 = r2(dia * 20 * 4 / 3); i20 = inss(f20); ir20 = irrf(f20, i20)
    print(f"vender 10 dias: férias 20 dias {f20} - INSS {i20} = {r2(f20-i20-ir20)} + abono {ab} = {r2(f20-i20-ir20+ab)}"
          f"  (vs {liq}, +{r2(f20-i20-ir20+ab-liq)}); e volta 10 dias antes, trabalhando (salário desses dias normal)")
    print(f"1ª parcela do 13º junto: + {r2(s/2)} sem desconto -> total {r2(liq + s/2)}")
