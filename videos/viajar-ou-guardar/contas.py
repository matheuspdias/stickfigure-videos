# Viajar todo ano ou guardar? R$ 5.000 por ano durante 10 anos, rendendo ~10% a.a. (conservador; Selic 13,75% em nov/2026), IR 15% no ganho
def sim(anos_deposito, r=0.10, anos=10):
    s = 0; ap = 0
    for y in range(1, anos + 1):
        s *= (1 + r)
        if y in anos_deposito:
            s += 5000; ap += 5000
    return s, ap + (s - ap) * 0.85
print("Bruno, todo ano:", sim(range(1, 11)))            # ~79,7 mil bruto, ~75 mil liquido -> "mais de setenta mil"
print("meio-termo, ano sim ano nao:", sim(range(1, 11, 2)), sim(range(2, 11, 2)))  # ~36-39 mil liquido -> "quase quarenta mil"
