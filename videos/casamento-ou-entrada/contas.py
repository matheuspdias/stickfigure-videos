# Festa de casamento de R$ 50 mil ou entrada do apê? Carla x Diego. Premissas redondas:
# investimento 0,8%/mês líquido (~10% a.a.; Selic 13,75% em nov/2026); empréstimo pessoal hipotético a 4%/mês, 36x (Price).
# Festa de ~150 convidados por ~R$ 50 mil está dentro das médias publicadas para 2026 (Santander, Serasa, C6).
r = 0.008
s = 0; n = 0
while s < 50000:
    s = s * (1 + r) + 1000; n += 1
print("meses p/ juntar 50 mil com 1.000/mes:", n, "=", round(n / 12, 1), "anos")   # 43 meses ~ 3,6 anos -> "uns três anos e meio"
i = 0.04
pmt = 50000 * i / (1 - (1 + i) ** -36)
print("parcela:", round(pmt), "total:", round(pmt * 36))                             # ~2.644 / ~95.196 -> "uns noventa e cinco mil", quase o dobro
print("Diego: entrada", 50000 - 5000)                                                 # 45 mil
