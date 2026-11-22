"""Contas do Checklist "3 passos antes de parcelar" (23/11/2026, 10h).
Regra de bolso: soma das parcelas <= 1/5 (20%) do salário líquido."""
sal = 2500
cel, gel = 150, 200
ja = cel + gel
teto = sal / 5
tv, n = 2400, 12
print("ja paga", ja, f"{ja/sal:.0%}", "teto", teto, "sobra", teto - ja)
print("tv/mes", tv / n, "total com tv", ja + tv / n, f"{(ja + tv/n)/sal:.0%}")
falta = cel * 6 + gel * 8 + tv
print("falta pagar: cel", cel * 6, "gel", gel * 8, "tv", tv, "=", falta)
