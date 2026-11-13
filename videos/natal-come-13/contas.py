"""Contas do TikTok "Seu 13º já tem dono: o Natal" (conferidas em 13/11/2026).
Natal: pesquisas CNDL/SPC Brasil do Natal 2025 (as de 2026 ainda não saíram):
  4 presentes em média, R$ 174 cada; ceia/almoço R$ 338; roupa nova R$ 324; amigo secreto R$ 72 por presente.
13º: salário fixo de R$ 3.000, 12 meses, sem dependentes; regras e tabelas 2026 em videos/decimo-terceiro-quanto-cai/contas.py
  (1ª parcela até 30/11 sem desconto; 2ª até 18/12 com INSS e IR do 13º inteiro; IR zero até R$ 5 mil).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "decimo-terceiro-quanto-cai"))
from contas import parcelas, r2

presentes = 4 * 174
natal = presentes + 338 + 324 + 72
s = 3000
p1 = r2(s / 2); inss, ir, p2 = parcelas(s, p1)
if __name__ == "__main__":
    print("presentes", presentes, "| Natal", natal)
    print("1a", p1, "| INSS", inss, "IR", ir, "| 2a", p2, "| líquido", p1 + p2)
    print("Natal / 1a parcela = %.0f%%" % (100 * natal / p1), "| Natal / 13º líquido = %.0f%%" % (100 * natal / (p1 + p2)))
