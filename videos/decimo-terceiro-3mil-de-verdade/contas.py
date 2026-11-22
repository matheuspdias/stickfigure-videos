"""Contas do TikTok "Seu 13º vai vir menor do que você pensa" (conferidas em 22/11/2026).
Salário fixo de R$ 3.000, 12 meses, sem dependentes. Regras e tabelas 2026 em videos/decimo-terceiro-quanto-cai/contas.py.
Saída: 1ª 1.500,00 | INSS 248,60 | IR 0 | 2ª 1.251,40 | total 2.751,40. 2025: IR no 13º de R$ 3 mil = 23,83.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "decimo-terceiro-quanto-cai"))
from contas import parcelas, r2, IR

i, ir, p2 = parcelas(3000, 1500)
print(f"1a 1500 | INSS {i} IR {ir} | 2a {p2} | total {r2(1500 + p2)}")
INSS25 = [(1518.00, .075), (2793.88, .09), (4190.83, .12), (8157.41, .14)]
tot, ant = 0, 0
for teto, a in INSS25:
    if 3000 > ant:
        tot += (min(3000, teto) - ant) * a
    ant = teto
base = 3000 - tot
for teto, a, ded in IR:
    if base <= teto:
        print("2025: IR no 13º de 3 mil = %.2f" % (base * a - ded)); break
