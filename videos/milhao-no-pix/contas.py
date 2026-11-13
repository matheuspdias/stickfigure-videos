"""Contas do TikTok "E se você acordasse com R$ 1 milhão no Pix?" (conferidas em 13/11/2026).
- Notas de R$ 100: ~0,1 mm e ~1 g cada (mesmas premissas de videos/milhao-por-dia-1500) -> estimativas ("uns").
- Salário mínimo 2026: R$ 1.621.
- CDI: 13,65% a.a. (Selic 13,75% mantida pelo Copom em 04/11/2026). IR 17,5% (aplicação de 1 a 2 anos; com 15%, acima de 2 anos, daria ~R$ 9,1 mil).
- Inflação: IPCA-15 de outubro/2026 em 12 meses 4,62% (usado 4,6%).
"""
M = 1_000_000
notas = M // 100
print("notas", notas, "| pilha m", notas * 0.1 / 1000, "| kg", notas * 1 / 1000)
for g in (1621, 5000, 20000):
    print("gasto", g, "-> anos", round(M / g / 12, 1))
cdi = 0.1365
m = (1 + cdi) ** (1 / 12) - 1
liq = M * m * (1 - 0.175)
inf = M * ((1.046) ** (1 / 12) - 1)
print("rende/mês líquido %.0f (\"quase nove mil\")" % liq)
print("pra repor a inflação %.0f (\"uns quatro mil\") | sobra %.0f (\"uns cinco mil\")" % (inf, liq - inf))
