# Reserva de emergencia, salario R$ 2.000, gastos essenciais R$ 1.500
gastos = 1500
print("meta 1 mes", gastos, "3 meses", 3 * gastos)
print("5% do salario", 0.05 * 2000)          # 100
# 2a parcela do 13o com salario 2000: 1000 - INSS do 13o inteiro (tabela 2026, minimo 1621)
inss = 1621 * 0.075 + (2000 - 1621) * 0.09
print("INSS 13o", round(inss, 2), "2a parcela", round(1000 - inss))  # ~155,69 -> ~844 (cabe R$ 500)
saldo = 500
for mes in range(1, 11):
    saldo += 100
    print(mes, saldo)                          # 10 meses -> 1500 (sem contar rendimento)
# rotativo ~451,7% a.a. (BC) ~15%/mes
print("rotativo 1 mes", 1500 * 1.15)           # 1725
