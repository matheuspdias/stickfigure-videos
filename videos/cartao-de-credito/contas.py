"""Contas do ep. 5 (cartão de crédito), pesquisadas em 08/11/2026.
Fonte: Banco Central, set/2026 (divulgado em 29/10/2026): rotativo 451,7% a.a.; parcelado da fatura 193,0% a.a.
Teto: Lei 14.690/2023, em vigor desde jan/2024: juros e encargos do rotativo e do parcelamento <= 100% da dívida original.
Rotativo só até o vencimento da fatura seguinte; depois o banco oferece parcelamento (Res. CMN 4.549/2017)."""
rot_aa, parc_aa = 4.517, 1.930
rot_am = (1 + rot_aa) ** (1 / 12) - 1
parc_am = (1 + parc_aa) ** (1 / 12) - 1
print(f"rotativo ao mês: {rot_am:.2%} | parcelado ao mês: {parc_am:.2%}")
divida = 1000
apos_1_mes = divida * (1 + 0.15)          # roteiro usa 15% redondo (fora o IOF)
pmt = apos_1_mes * parc_am / (1 - (1 + parc_am) ** -12)
total = pmt * 12
print(f"1 mês no rotativo: {apos_1_mes:.0f} | 12x de {pmt:.2f} | total {total:.0f} | juros {total - divida:.0f}")
assert round(rot_am * 100) == 15 and round(parc_am * 100) == 9
assert round(pmt) == 164 and 1950 < total < 2000 and total - divida <= divida   # abaixo do teto de 100%
fatura = 640 + 250 + 35
assert fatura == 925
