"""Contas do ep. 6 (antes de abrir MEI). Pesquisa em 12/11/2026:
- salário mínimo 2026: R$ 1.621; DAS-MEI = 5% do mínimo (INSS) + R$ 1 ICMS e/ou R$ 5 ISS
  -> comércio/indústria R$ 82,05; serviços R$ 86,05; comércio e serviços R$ 87,05 (contabeis.com.br)
- limite anual: R$ 81.000 (segue em 2026); excesso até 20% (R$ 97.200): DAS complementar sobre o excesso e
  desenquadramento a partir de jan do ano seguinte; acima de 20%: desenquadramento retroativo a janeiro (LC 123/2006, art. 18-A)
- DASN-SIMEI até 31/05, mesmo sem faturamento
- seguro-desemprego: renda própria barra o benefício (Lei 7.998/1990; Res. CODEFAT 467/2005); CNPJ ativo costuma ser lido assim
- nota fiscal obrigatória para vendas/serviços a PJ (para PF, só se o cliente pedir)"""
sm = 1621
inss = 0.05 * sm
das = {"comercio": inss + 1, "servicos": inss + 5, "comercio+servicos": inss + 6}
for k, v in das.items():
    print(f"DAS {k}: R$ {v:.2f}  | ano: R$ {12*v:.2f}")
print("limite/mes:", 81000 / 12, "| +20%:", 81000 * 1.2)
