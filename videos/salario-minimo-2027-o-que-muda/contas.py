# Salario minimo 2026 R$ 1.621; previsao 2027 (PLOA) R$ 1.741
a, b = 1621, 1741
print("aumento", b - a, f"{(b/a-1)*100:.1f}%")        # 120, 7,4%
ia, ib = a * 0.075, b * 0.075
print("INSS", round(ia, 2), round(ib, 2))             # 121,58 -> 130,58
liq = (b - ib) - (a - ia)
print("liquido a mais/mes", round(liq, 2), "ano c/13o", round(liq * 13))  # 111 -> 1443
# MEI: DAS-INSS = 5% do minimo (+R$1 ICMS / +R$5 ISS)
print("DAS", a * 0.05, b * 0.05, "dif/ano", round((b - a) * 0.05 * 12))   # 81,05 -> 87,05 ; 72
