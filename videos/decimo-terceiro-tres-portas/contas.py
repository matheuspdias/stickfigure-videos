"""Contas do TikTok "O que fazer com o 13º antes do dia 30" (parte 2 de decimo-terceiro-quanto-cai).
Conferidas em 04/11/2026 com os dados do BC de setembro/2026 (divulgados em 29/10/2026).
Mesmas premissas do videos/decimo-terceiro/contas.py: Ana, salário R$ 3.000, 13º líquido ~R$ 2.750,
investimento a 5% a.a. acima da inflação (já com imposto), aporte corrigido pela inflação.
"""
ROTATIVO = 4.517    # 451,7% a.a., set/2026 (BC); em ago/2026 era 444,9%
PARCELADO = 1.930   # 193,0% a.a., set/2026 (BC); em ago/2026 era 192,1%
REAL = 0.05
LIQ = 2750          # 13º líquido da Ana (3.000 - INSS 248,60 = 2.751,40, arredondado)

m_rot = (1 + ROTATIVO) ** (1 / 12) - 1
m_par = (1 + PARCELADO) ** (1 / 12) - 1
print(f"rotativo {m_rot:.2%}/mês | parcelado {m_par:.2%}/mês")
import math
print(f"meses pra dobrar no rotativo sem teto: {math.log(2)/math.log(1+m_rot):.1f}")
print(f"2750 no parcelado 12m sem teto: {LIQ*(1+PARCELADO):.0f} | teto da Lei 14.690/2023 (juros+encargos <= 100%): {LIQ*2}")
for pct in (1.0, 0.8):
    a = pct * LIQ
    for n in (10, 20, 30):
        print(f"{pct:.0%} do 13º ({a:.0f}) por {n} anos: {a*((1+REAL)**n-1)/REAL:,.0f}")
