"""Contas do TikTok "Se você fosse demitido hoje, quanto receberia?" (conferidas em 05/11/2026).
Exemplo simplificado: salário R$ 3.000, admitido em 01/10/2024, demitido sem justa causa em 15/11/2026,
primeiro pedido de seguro-desemprego, sem dependentes, sem médias de horas extras.
- Saldo de salário: 15/30 do salário.
- Aviso prévio indenizado (CLT art. 487 + Lei 12.506/2011): 30 dias + 3 por ano completo = 36 dias.
  Projeta o contrato até 21/12/2026 (OJ 82 SDI-1 TST): conta para férias e 13º.
- Férias: período 01/10/2024-30/09/2025 já gozado; 01/10/2025-30/09/2026 vencido (inteiro);
  01/10/2026 em diante: 3/12 proporcionais (out, nov, dez projetado com 21 dias >= 15). Tudo + 1/3.
- 13º proporcional: jan a dez (dezembro projetado com 21 dias) = 12/12.
- FGTS: 8% x 3.000 x 24 meses (simplificado: sem rendimento, sem o 13º e sem o FGTS da própria rescisão).
- Multa: 40% do saldo (Lei 8.036/1990, art. 18 §1º).
- Seguro-desemprego 2026 (MTE, desde 11/01/2026): até 2.222,17 -> x0,8; até 3.703,99 -> 1.777,74 + 50% do que
  passar de 2.222,17; acima, teto 2.518,65. Piso 1.621,00. 1º pedido com 24+ meses: 5 parcelas.
- Descontos: INSS e IRRF no saldo de salário e no 13º; aviso indenizado e férias indenizadas + 1/3 sem INSS/IR.
  Com R$ 3.000, IR zera (Lei 15.270/2025). INSS: 112,50 (saldo) + 248,60 (13º).
- Prazo: 10 dias corridos do fim do contrato (CLT art. 477 §6º).
- Saque-aniversário: na demissão sem justa causa saca só a multa de 40%; o saldo fica retido.
"""
S = 3000
saldo = S / 30 * 15
aviso = S / 30 * (30 + 3 * 2)
ferias = (S + S * 3 / 12) * 4 / 3
dec = S * 12 / 12
resc = saldo + aviso + ferias + dec
fgts = 0.08 * S * 24
multa = 0.40 * fgts
seg = 1777.74 + 0.5 * (S - 2222.17)
if __name__ == "__main__":
    print(saldo, aviso, ferias, dec, resc, fgts, multa, resc + fgts + multa, round(seg, 2), round(5 * seg, 2))
    assert (resc, fgts, multa, resc + fgts + multa) == (13100, 5760, 2304, 21164)
