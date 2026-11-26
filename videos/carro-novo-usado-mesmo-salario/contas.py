"""Contas de "Mesmo salário: carro zero x usado + investir a parcela" (25/11/2026).
Fontes: juros médios de veículos PF ~1,9% a.m. (Banco Central, 2026); depreciação de carro novo em 5 anos ~40-45%
(curvas FIPE 2026); usado de ~10 anos perde menos (~30% em 5 anos). Rendimento: 10% a.a. líquido (conservador,
CDI hoje ~13,65% bruto, Selic tende a cair). Seguro, IPVA e manutenção fora da conta (dito no vídeo)."""
r = 0.019
pv = 80000; n = 60
pmt = pv * r / (1 - (1 + r) ** -n)
i = 1.10 ** (1 / 12) - 1
fv = pmt * ((1 + i) ** n - 1) / i
novo_5a = 100000 * 0.55
usado_5a = 20000 * 0.70
print(f"parcela {pmt:.2f} | total pago Lucas {20000 + pmt * n:.0f} | carro novo vale {novo_5a:.0f}")
print(f"Bruno investido {fv:.0f} + carro {usado_5a:.0f} = {fv + usado_5a:.0f} | diferença {fv + usado_5a - novo_5a:.0f}")
