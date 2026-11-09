# Seu carro te custa mais que um aluguel? Carro de R$ 60 mil, 1.000 km/mês (valores de exemplo, redondos)
valor = 60000
ipva = 0.04 * valor            # 2.400 (alíquota de SP; outros estados 2-3,5%)
seguro = 3000
deprec = 0.10 * valor          # 6.000 (perde ~10% ao ano)
manut = 1800                   # revisão, pneus, licenciamento
comb = 1000 / 12 * 6.70 * 12   # 1.000 km/mês, 12 km/l, gasolina ~R$ 6,70 -> ~R$ 6.700/ano
estac = 1200
ano = ipva + seguro + deprec + manut + comb + estac
print("custos/ano", ipva, seguro, deprec, manut, round(comb), estac, "=", round(ano), "-> mês", round(ano / 12))
oport = valor * 0.10           # R$ 60 mil rendendo ~10% ao ano líquido
print("custo de oportunidade/ano", oport, "-> total mês", round((ano + oport) / 12))
app = 2 * 22 * 25 + 8 * 30     # 2 corridas por dia útil de R$ 25 + 8 corridas no fim de semana de R$ 30
print("app/mês", app)
