# Lei 15.270/2025: isenção ate R$ 5 mil/mes por fonte; anual: reducao total ate R$ 60 mil, parcial ate R$ 88.200
renda = 2 * 3000 * 12          # 72.000 (13o tributado a parte)
base = renda - min(0.2 * renda, 16754.34)   # desconto simplificado
faixas = [(29145.60, 0), (33919.80, .075), (45012.60, .15), (56007.60, .225), (1e12, .275)]
imp, ant = 0, 0
for lim, al in faixas:
    if base > ant:
        imp += (min(base, lim) - ant) * al
    ant = lim
red = 8429.73 - 0.095575 * renda if renda <= 88200 else 0
print("renda", renda, "base", base, "imposto tabela", round(imp), "reducao", round(red), "a pagar", round(imp - red), "por mes", round((imp - red) / 12))
