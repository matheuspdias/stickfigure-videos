"""Contas de "Pedir demissão x acordo x demitido" (27/11/2026). Mesmas premissas de videos/demitido-hoje/contas.py.
Salário R$ 3.000, admitido em 01/10/2024, saída em 30/11/2026 (2 anos e 2 meses), sem horas extras, valores ANTES de
INSS/IR (que só incidem no saldo e no 13º; com R$ 3.000 o IR zera). FGTS simplificado: 8% x 3.000 x 26 meses, sem rendimento.
- Pedido de demissão (aviso de 30 dias trabalhado em novembro): saldo, férias vencidas + 2/12 com 1/3, 13º 11/12.
  Não saca FGTS (fica na conta), sem multa, sem seguro-desemprego. Se não cumprir o aviso, a empresa pode descontar 30 dias.
- Acordo (CLT art. 484-A, reforma de 2017): metade do aviso indenizado (36/2 = 18 dias, projeta até 18/12 -> 13º 12/12,
  férias 3/12), multa de 20%, saca 80% do FGTS, sem seguro-desemprego. Depende de a empresa aceitar.
- Sem justa causa: aviso de 36 dias indenizado (projeta até 05/01/2027 -> 13º 12/12, férias 3/12), multa de 40%,
  saca 100% do FGTS, seguro-desemprego 2026 (1º pedido, 24+ meses: 5 parcelas de 1.777,74 + 50% do que passa de 2.222,17).
"""
S = 3000
fgts = 0.08 * S * 26
ferias = lambda n: (S + S * n / 12) * 4 / 3
ped = dict(saldo=S, aviso=0, ferias=ferias(2), dec=S * 11 / 12, fgts=0, multa=0, seguro=0)
aco = dict(saldo=S, aviso=S / 30 * 18, ferias=ferias(3), dec=S, fgts=0.8 * fgts, multa=0.2 * fgts, seguro=0)
seg = 1777.74 + 0.5 * (S - 2222.17)
dem = dict(saldo=S, aviso=S / 30 * 36, ferias=ferias(3), dec=S, fgts=fgts, multa=0.4 * fgts, seguro=5 * seg)
for nome, d in (("pedido", ped), ("acordo", aco), ("demitido", dem)):
    resc = d["saldo"] + d["aviso"] + d["ferias"] + d["dec"]
    tot = resc + d["fgts"] + d["multa"]
    print(f"{nome:9s} rescisão {resc:8.0f} | FGTS {d['fgts']:6.0f} + multa {d['multa']:6.0f} | na saída {tot:8.0f} | seguro {d['seguro']:6.0f} | tudo {tot + d['seguro']:8.0f}")
print("FGTS total na conta", fgts, "| parcela seguro", round(seg, 2))
