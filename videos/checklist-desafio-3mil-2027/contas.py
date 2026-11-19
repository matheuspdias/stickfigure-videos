# Desafio R$ 3 mil em 2027 (Focus 16/11/2026: Selic 13,75% fim 2026, 12,75% fim 2027 -> CDI médio 2027 ~13,1%)
print(3000/12, 3000/52, 250/30)                      # 250 por mês, ~58 por semana, ~8 por dia
print(sum(2*i for i in range(1, 53)), 2*52)          # 52 semanas de R$ 2 subindo R$ 2: 2.756; última semana R$ 104
print(sum(2*i for i in range(49, 53)))               # dezembro (semanas 49-52): R$ 404
r = 1.131**(1/12) - 1; s = 0
for m in range(12):
    s = s*(1 + r*0.8) + 250                          # IR ~20% (prazo médio de 6 meses a 1 ano)
print(round(s), round(s - 3000))                     # ~3.140, ~R$ 140 de rendimento
