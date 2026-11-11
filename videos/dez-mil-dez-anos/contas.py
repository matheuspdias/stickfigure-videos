# R$ 10 mil há 10 anos: onde você estaria mais rico hoje?  (contas feitas em 11/11/2026)
# Aplicação em 10/11/2016, resgate em 10/11/2026. R$ 10.000 em cada.
from math import prod
CAP = 10_000

# CDI mensal (patrimo.app, base BCB), nov/2016 a out/2026 = 120 meses
cdi = [1.04,1.12, 1.08,0.86,1.05,0.79,0.93,0.81,0.8,0.8,0.64,0.64,0.57,0.54,
 0.58,0.46,0.53,0.52,0.52,0.52,0.54,0.57,0.47,0.54,0.49,0.49,
 0.54,0.49,0.47,0.52,0.54,0.47,0.57,0.5,0.46,0.48,0.38,0.37,
 0.38,0.29,0.34,0.28,0.24,0.21,0.19,0.16,0.16,0.16,0.15,0.16,
 0.15,0.13,0.2,0.21,0.27,0.31,0.36,0.43,0.44,0.49,0.59,0.77,
 0.73,0.76,0.93,0.83,1.03,1.02,1.03,1.17,1.07,1.02,1.02,1.12,
 1.12,0.92,1.17,0.92,1.12,1.07,1.07,1.14,0.97,1,0.92,0.89,
 0.97,0.8,0.83,0.89,0.83,0.79,0.91,0.87,0.84,0.93,0.79,0.93,
 1.01,0.99,0.96,1.06,1.14,1.1,1.28,1.16,1.22,1.28,1.05,1.22,
 1.16,1,1.21,1.09,1.07,1.12,1.22,1.09,1.08,1.07]
# Poupança mensal (numerando.com.br), nov/2016 a out/2026
poup = [0.64,0.69, 0.67,0.53,0.65,0.50,0.58,0.55,0.56,0.55,0.50,0.47,0.43,0.43,
 0.40,0.40,0.39,0.37,0.37,0.37,0.37,0.37,0.37,0.37,0.37,0.37,
 0.37,0.37,0.37,0.37,0.37,0.37,0.37,0.34,0.34,0.32,0.29,0.29,
 0.26,0.26,0.24,0.22,0.22,0.17,0.13,0.13,0.12,0.12,0.12,0.12,
 0.12,0.12,0.12,0.16,0.16,0.20,0.24,0.24,0.30,0.36,0.44,0.49,
 0.56,0.50,0.60,0.56,0.67,0.65,0.66,0.74,0.68,0.65,0.65,0.71,
 0.71,0.58,0.74,0.58,0.72,0.68,0.66,0.72,0.61,0.61,0.58,0.57,
 0.54,0.56,0.58,0.54,0.59,0.57,0.57,0.58,0.57,0.57,0.58,0.62,
 0.67,0.58,0.64,0.67,0.67,0.67,0.68,0.68,0.67,0.68,0.67,0.67,
 0.67,0.67,0.67,0.67,0.67,0.67,0.67,0.67,0.67,0.66]
# IPCA mensal (IBGE via yahii), nov/2016 a set/2026 + out/2026 estimado pelo IPCA-15 (0,32%)
ipca = [0.18,0.30, 0.38,0.33,0.25,0.14,0.31,-0.23,0.24,0.19,0.16,0.42,0.28,0.44,
 0.29,0.32,0.09,0.22,0.40,1.26,0.33,-0.09,0.48,0.45,-0.21,0.15,
 0.32,0.43,0.75,0.57,0.13,0.01,0.19,0.11,-0.04,0.10,0.51,1.15,
 0.21,0.25,0.07,-0.31,-0.38,0.26,0.36,0.24,0.64,0.86,0.89,1.35,
 0.25,0.86,0.93,0.31,0.83,0.53,0.96,0.87,1.16,1.25,0.95,0.73,
 0.54,1.01,1.62,1.06,0.47,0.67,-0.68,-0.36,-0.29,0.59,0.41,0.62,
 0.53,0.84,0.71,0.61,0.23,-0.08,0.12,0.23,0.26,0.24,0.28,0.56,
 0.42,0.83,0.16,0.38,0.46,0.21,0.38,-0.02,0.44,0.56,0.39,0.52,
 0.16,1.31,0.56,0.43,0.26,0.24,0.26,-0.11,0.48,0.09,0.18,0.33,
 0.33,0.70,0.88,0.67,0.58,0.16,0.07,-0.32,0.82,0.32]
for n,s in (("cdi",cdi),("poup",poup),("ipca",ipca)): assert len(s)==120,(n,len(s))
f = lambda s: prod(1+x/100 for x in s)
F_cdi, F_poup, F_ipca = f(cdi), f(poup), f(ipca)

def liq(bruto, ir=0.15): return bruto - max(bruto-CAP,0)*ir
res = {}
res["CDB 100% do CDI"] = (CAP*F_cdi, liq(CAP*F_cdi))
res["Poupança"] = (CAP*F_poup, CAP*F_poup)
ibov0, ibov1 = 61_200.95, 171_336.99          # 10/11/2016 e 10/11/2026 (já com dividendos: índice de retorno total)
res["Bolsa (Ibovespa)"] = (CAP*ibov1/ibov0, liq(CAP*ibov1/ibov0))
usd0, usd1 = 3.3615, 5.586                     # dólar comercial, fechamento 10/11/2016 e 10/11/2026
res["Dólar"] = (CAP*usd1/usd0, CAP*usd1/usd0)  # dólar parado (em espécie), sem rendimento
ifix0, ifix1 = 1_816.56, 3_573.50              # IFIX fechamento out/2016 e 10/11/2026 (rendimentos reinvestidos)
res["Fundos imobiliários (IFIX)"] = (CAP*ifix1/ifix0, CAP*ifix1/ifix0)
btc0, btc1 = 715.53*usd0, 73_796.40*usd1
bitcoin = CAP*btc1/btc0
infl = CAP*F_ipca

print(f"Fatores: CDI {F_cdi:.4f}  Poupança {F_poup:.4f}  IPCA {F_ipca:.4f}")
print(f"Inflação: R$ 10 mil de 2016 = R$ {infl:,.0f} hoje (IPCA acumulado {100*(F_ipca-1):.1f}%)")
for k,(b,l) in sorted(res.items(), key=lambda kv:-kv[1][1]):
    real = l/F_ipca
    print(f"{k:28s} bruto R$ {b:>10,.0f}  líquido R$ {l:>10,.0f}  ganho real (em reais de 2016) R$ {real:>8,.0f}  ({100*(real/CAP-1):+.0f}%)  a.a. nominal {100*((l/CAP)**(1/10)-1):.1f}%")
print(f"Bitcoin bruto: R$ {bitcoin:,.0f}  (x{bitcoin/CAP:.0f})  BTC em reais: {btc0:,.0f} -> {btc1:,.0f}")
# caminho do bitcoin: topo dez/2017 ~US$ 19.500; fundo dez/2018 ~US$ 3.200 (-84%); topo nov/2021 ~US$ 69 mil; fundo nov/2022 ~US$ 15.500 (-77%); recorde US$ 126.080 (out/2025)
print("bitcoin -84% 2018 e -77% 2022; hoje -41% do recorde")
# Ibovespa: caiu 9,88% em outubro de 2026 (maior queda mensal desde 2022)
ib_out = res["Bolsa (Ibovespa)"]
print(f"Se a bolsa estivesse 10% acima (antes da queda de outubro): R$ {liq(CAP*ibov1/ibov0/0.9012):,.0f}")
# Diferença CDB x bolsa
print(f"Bolsa - CDB: R$ {res['Bolsa (Ibovespa)'][1]-res['CDB 100% do CDI'][1]:,.0f}")
print(f"CDB - poupança: R$ {res['CDB 100% do CDI'][1]-res['Poupança'][1]:,.0f}")

# --- O caminho até aqui ---
# Fundo da covid: Ibovespa 63.569,62 em 23/03/2020 (Suno). Poupança nov/2016 a mar/2020 = 41 meses (mar/2020 cheio, aproximação)
ib_covid = 63_569.62
bruno_covid = CAP*ib_covid/ibov0
ana_covid = CAP*f(poup[:41])
cdb_covid = CAP*f(cdi[:41])
print(f"\nMarço/2020: Bruno (bolsa) R$ {bruno_covid:,.0f} | Ana (poupança) R$ {ana_covid:,.0f} | CDB R$ {cdb_covid:,.0f}")
# Topo de outubro/2026: o Ibovespa passou dos 209 mil pontos (InfoMoney); fechou outubro em 167.922
print(f"Bolsa a 209 mil pontos: R$ {CAP*209_000/ibov0:,.0f} bruto | fim de out/2026 (167.922): R$ {CAP*167_922/ibov0:,.0f}")
# Metade CDB, metade bolsa
meio = (res['CDB 100% do CDI'][1]+res['Bolsa (Ibovespa)'][1])/2
meio_covid = (cdb_covid+bruno_covid)/2
print(f"Metade CDB + metade bolsa: hoje R$ {meio:,.0f} | no fundo de 2020 R$ {meio_covid:,.0f}")
print(f"IR pago no CDB: R$ {res['CDB 100% do CDI'][0]-res['CDB 100% do CDI'][1]:,.0f} | na bolsa: R$ {res['Bolsa (Ibovespa)'][0]-res['Bolsa (Ibovespa)'][1]:,.0f}")
# Comparação com o vídeo de 5 anos (15/10/2021 a 16/10/2026, videos/dez-mil-cinco-anos): CDB R$ 16.956, Ibovespa R$ 16.731, poupança R$ 14.569
print(f"Dólar: R$ {usd0} -> R$ {usd1} (+{100*(usd1/usd0-1):.0f}%) | inflação +{100*(F_ipca-1):.0f}%")
print(f"Poupança acima da inflação: R$ {res['Poupança'][1]-infl:,.0f} | dólar acima: R$ {res['Dólar'][1]-infl:,.0f}")

# Caminho do bitcoin para os mesmos R$ 10 mil (aprox.: preço US$ x dólar da época)
qtd = CAP/btc0
for nome,usd,brl in (("topo dez/2017",19_500,3.30),("fundo dez/2018",3_200,3.90),("topo nov/2021",69_000,5.55),("fundo nov/2022",15_500,5.30),("recorde out/2025",126_080,5.33)):
    print(f"bitcoin {nome}: R$ {qtd*usd*brl:,.0f}")
print(f"Ibovespa: topo jan/2020 119.527 -> 23/03/2020 63.570 = {100*(63_569.62/119_527.63-1):.0f}%")
