"""Contas do TikTok "E se você guardasse R$ 1 por segundo?" (conferidas em 14/11/2026).
- Salário mínimo 2026: R$ 1.621 (220 h/mês).
- Moeda de R$ 1: 7,0 g (Banco Central) -> estimativas com "uns"/"quase".
- CDI 13,65% a.a. (Selic 13,75%), IR 17,5% (mesmas premissas de videos/milhao-no-pix).
"""
s_dia = 86400
print("minuto", 60, "| hora", 3600, "| dia", s_dia, "| ano", s_dia * 365)
print("salário mínimo em minutos", round(1621 / 60, 1))
print("1 milhão em dias", round(1e6 / s_dia, 1))
print("1 bilhão em anos", round(1e9 / s_dia / 365, 1))
print("peso moedas dia kg", s_dia * 7 / 1000, "| ano t", s_dia * 365 * 7 / 1e6)
print("min de trabalho por real no mínimo", round(220 * 60 / 1621, 1))
m = (1.1365) ** (1 / 12) - 1
ano = s_dia * 365
print("rende/mês líquido de 1 ano guardado %.0f" % (ano * m * 0.825))
print("rende por segundo %.3f" % (ano * m * 0.825 / (30 * s_dia)))
# quando os juros sozinhos passam de R$1/s (mês de 30 dias), guardando 1/s e reinvestindo
saldo, mes = 0.0, 0
while True:
    mes += 1
    saldo = saldo * (1 + m * 0.825) + 30 * s_dia
    if saldo * m * 0.825 >= 30 * s_dia:
        break
print("juros > R$1/s após meses", mes, "anos", round(mes / 12, 1), "saldo %.0f" % saldo)
print("vídeo de 75 s -> R$", 75)
