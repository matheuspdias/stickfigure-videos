"""Contas de "Dólar a R$ 6: o que fica mais caro no seu bolso" (24/11/2026, 18h).
Fontes: CNN/Reuters, dólar à vista fechou R$ 4,9896 em 23/10/2026; Exame/Seu Dinheiro, passou de R$ 6,00 em 23/11/2026
(maior desde abr/2025); IOF 3,5% em cartão, pré-pago e espécie (Decreto 12.499/2025)."""
antes, hoje = 5.00, 6.00
print("alta", f"{hoje/antes-1:.0%}", "(real:", f"{6.0/4.9896-1:.1%})")
iof = 0.035
v = 1000
a, h = v*antes*(1+iof), v*hoje*(1+iof)
print("viagem", a, h, h - a)
print("compra 40 USD", 40*antes, 40*hoje)
