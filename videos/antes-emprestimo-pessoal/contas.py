# BC, crédito pessoal não consignado, set/2026: 6,42% a.m. = 110,94% a.a. (série 20742/25464, via valorfinal.com.br 06/11/2026)
# Procon-SP nov/2026 (coleta 04/11): taxa máxima, não preferencial, 12 meses: BB 6,29%, Safra 7,25%, Caixa 8,00%, Itaú 9,49%, Bradesco 9,84%, Santander 9,99% a.m.
# Ranking BC 05-11/11/2026: mín. 3,92% a.a., 1º quartil 39,69% a.a., mediana 105,11%, 3º quartil 265,76% a.a.; consignado INSS 23,94%, privado CLT 47,69%, cheque especial 144,43%
# Rotativo do cartão set/2026: 451,7% a.a.
pv, i, n = 5000, 0.065, 12
pmt = pv * i / (1 - (1 + i) ** -n)
print("parcela", round(pmt, 2), "total", round(pmt * n), "juros", round(pmt * n - pv))  # 612,93 / 7355 / 2355
print("6,5% a.m. em a.a.", (1 + i) ** 12 - 1)
# IOF: 0,38% + 0,0082%/dia (teto 3% por parcela) -> fora da conta (narração: "tem IOF")
