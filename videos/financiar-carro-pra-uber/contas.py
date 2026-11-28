"""Contas de "Financiar carro pra rodar de Uber" (27/11/2026). Lucas financia, Bruno aluga. Mesma rotina.
Jornada: 10 h/dia, 5 dias/semana (~217 h/mês), ~4.000 km/mês, faturamento de R$ 7.000/mês já sem a taxa do app
(faixa citada: R$ 7-9 mil para 60 h/semana; R$ 35-55 por hora logada nas capitais).
Gasolina R$ 6,47 (ANP, 1-7/11/2026); carro popular 12 km/l.
Lucas: carro de R$ 80 mil, entrada de R$ 10 mil, R$ 70 mil em 60x a 1,9% a.m. (média BC); manutenção/pneus ~R$ 0,18/km;
seguro comercial ~R$ 4.000/ano; IPVA ~4%. Depreciação fora do "no bolso" (ele fica com o carro, que perde valor).
Bruno: aluguel ~R$ 800/semana (Zarp/Kovi, com seguro, manutenção e IPVA inclusos), mesma gasolina.
Conferência: despesas TST ~R$ 5.566 (próprio) e ~R$ 5.706 (alugado) por mês."""
fat, km, h = 7000, 4000, 217
gas = km / 12 * 6.47
r, n, pv = 0.019, 60, 70000
parc = pv * r / (1 - (1 + r) ** -n)
manut = 0.18 * km
seg_ipva = 4000 / 12 + 0.04 * 80000 / 12
lucas_gastos = gas + manut + seg_ipva + parc
alug = 800 * 52 / 12
bruno_gastos = alug + gas
print(f"gasolina {gas:.0f} | manutenção {manut:.0f} | seguro+IPVA {seg_ipva:.0f} | parcela {parc:.0f}")
print(f"Lucas gasta {lucas_gastos:.0f}, sobra {fat - lucas_gastos:.0f} ({(fat - lucas_gastos) / h:.2f}/h)")
print(f"Bruno: aluguel {alug:.0f} + gasolina = {bruno_gastos:.0f}, sobra {fat - bruno_gastos:.0f} ({(fat - bruno_gastos) / h:.2f}/h)")
