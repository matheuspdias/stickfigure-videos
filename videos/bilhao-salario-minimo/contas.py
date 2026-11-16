# E se você guardasse um salário mínimo por mês até chegar a R$ 1 bilhão?
# Salário mínimo 2026: R$ 1.621 (decreto de 24/12/2025). CDI ~13,65% a.a. (Selic 13,75%, Copom 04/11/2026), IR 15%.
import math
sm = 1621; B = 1e9
meses = B / sm; anos = meses / 12
print(f"sem juros: {meses:,.0f} meses = {anos:,.0f} anos")
# referências: pirâmides de Gizé ~4.500 anos; agricultura ~12 mil anos; Jesus ~2.026 anos
print(f"anos / pirâmides(4500) = {anos/4500:.1f}")
liq = 0.1365 * 0.85
r = (1 + liq) ** (1/12) - 1
n = math.log(B * r / sm + 1) / math.log(1 + r)
print(f"CDI liq a.a. {liq*100:.2f}%  r mensal {r*100:.3f}%  -> {n:.0f} meses = {n/12:.1f} anos")
tot_dep = sm * n
print(f"total depositado {tot_dep:,.0f}  juros {B - tot_dep:,.0f}  ({(B-tot_dep)/B*100:.1f}% juros)")
# um milhão
n1 = math.log(1e6 * r / sm + 1) / math.log(1 + r)
print(f"R$ 1 milhão: sem juros {1e6/sm/12:.0f} anos; com CDI {n1/12:.1f} anos")
# pilha de notas: 1621 em notas de 100 ~ 16 notas/mês
notas = B / 100; esp = 0.11e-3  # nota ~0,11 mm
print(f"R$ 1 bi em notas de 100: {notas:,.0f} notas, pilha {notas*esp/1000:.1f} km, peso ~{notas*1.0/1000/1000:.0f} t (1 g/nota)")
# inflação 4,5% a.a.: valor de hoje do bilhão daqui n anos
print(f"bilhão em dinheiro de hoje (IPCA 4,5%) {B/1.045**(n/12):,.0f}")
