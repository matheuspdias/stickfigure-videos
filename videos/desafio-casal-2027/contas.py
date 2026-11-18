"""Desafio do casal 2027: R$ 10 mil em 12 meses, em 3 degraus.
CDI de referência: 13,65% a.a. (Selic 13,75% mantida pelo Copom em 04/11/2026).
Depósito no início de cada mês (jan..dez/2027), saldo conferido em 31/12/2027. IR regressivo por depósito
(até 180 dias 22,5%; 181-360 20%; acima de 360 17,5%)."""
deps = [600]*4 + [800]*4 + [1100]*4
cdi = 0.1365
m = (1+cdi)**(1/12)-1
total = sum(deps); bruto = liq = 0
for i, d in enumerate(deps):
    meses = 12 - i
    r = d*((1+m)**meses - 1)
    dias = meses*30.4
    ir = 0.225 if dias <= 180 else 0.20 if dias <= 360 else 0.175
    bruto += r; liq += r*(1-ir)
print("depositado", total, "rendimento bruto", round(bruto), "liquido", round(liq), "final", round(total+liq))
print("cada um:", [d//2 for d in (600, 800, 1100)])
