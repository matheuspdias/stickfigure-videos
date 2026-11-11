# Morar com os pais dos 25 aos 30: Lucas guarda R$ 1.000/mês por 60 meses; Carla paga R$ 1.200 de aluguel
# Rendimento conservador: 10% a.a. (Selic 13,75% em nov/2026, mas deve cair em 5 anos), IR 15% sobre o ganho
m = 1.10 ** (1/12) - 1
s = 0
for _ in range(60):
    s = s * (1 + m) + 1000
aportes = 60000
liq = aportes + (s - aportes) * 0.85
print(f"Lucas: bruto {s:.0f}, liquido {liq:.0f}")   # ~77.4 mil bruto, ~74 mil liquido -> "mais de setenta mil"
print("Carla aluguel 5 anos:", 1200 * 60)             # 72.000
