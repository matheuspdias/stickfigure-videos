# R$ 300 por mês em lanche e bar é exagero? Premissas redondas: salário R$ 5.000; investimento 0,8%/mês líquido
# (~10% a.a.; Selic 13,75% em nov/2026); aportes no fim de cada mês, 10 anos.
r = 0.008
fv = lambda p, n: p * ((1 + r) ** n - 1) / r
print("por ano:", 300 * 12)                       # 3.600
print("300/mes 10 anos:", round(fv(300, 120)))    # ~60.065 -> "uns sessenta mil"
print("% do salario:", 300 / 5000)                # 6%
print("150/mes 10 anos:", round(fv(150, 120)))    # ~30.033 -> "uns trinta mil"
