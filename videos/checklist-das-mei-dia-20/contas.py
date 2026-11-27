# DAS-MEI 2026 (salário mínimo R$ 1.621): comércio R$ 82,05, serviços R$ 86,05, comércio+serviços R$ 87,05 (contabeis.com.br, 27/01/2026)
das = 86.05
print("por dia", das / 30)  # 2,87 -> "menos de R$ 3 por dia"
# atraso: multa 0,33%/dia limitada a 20% + juros Selic (Lei 9.430/96). Um ano esquecido (12 DAS, pago no 13º mês):
selic_m = 0.0105  # ~13,75% a.a. ~1,08%/mês, juros simples acumulados (aprox.)
tot = 0
for k in range(12):           # k = meses de atraso do boleto (12 ... 1)
    meses = 12 - k
    dias = meses * 30
    multa = min(0.0033 * dias, 0.20)
    tot += das * (1 + multa + selic_m * max(meses - 1, 0) + 0.01)
print("um ano esquecido", round(tot))  # ~1.300 -> "mais de R$ 1.200"
print("12 x DAS", 12 * das)          # 1.032,60
# parcelamento de débitos do MEI: até 60 parcelas, mínima R$ 50 (Portal do Simples Nacional)
# qualidade de segurado: até 12 meses após a última contribuição. DASN-SIMEI até 31/05.
