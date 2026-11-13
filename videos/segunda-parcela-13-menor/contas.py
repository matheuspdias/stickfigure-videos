"""Contas do TikTok "Por que a 2ª parcela do 13º vem menor" (conferidas em 13/11/2026).
Salário fixo, 12 meses, sem dependentes. Regras e tabelas 2026 em videos/decimo-terceiro-quanto-cai/contas.py
(INSS 2026: Portaria Interministerial MPS/MF 13/2026; IR: redução da Lei 15.270/2025, que vale para o 13º).
2025 (comparação): INSS 2025 7,5% até 1.518; 9% até 2.793,88; 12% até 4.190,83; 14% até 8.157,41; mesma tabela de IR, sem a redução.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "decimo-terceiro-quanto-cai"))
from contas import parcelas, r2, IR

for s in (2000, 3000, 5000, 7000):
    p1 = r2(s / 2); i, ir, p2 = parcelas(s, p1)
    print(f"{s}: 1a {p1} | INSS {i} IR {ir} | 2a {p2}")

INSS25 = [(1518.00, .075), (2793.88, .09), (4190.83, .12), (8157.41, .14)]
tot, ant = 0, 0
for teto, a in INSS25:
    if 5000 > ant:
        tot += (min(5000, teto) - ant) * a
    ant = teto
base = 5000 - tot
for teto, a, ded in IR:
    if base <= teto:
        print("2025, salário 5 mil: INSS %.2f, IR no 13º %.2f (\"uns trezentos e trinta\")" % (tot, base * a - ded)); break
