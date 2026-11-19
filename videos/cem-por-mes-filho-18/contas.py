# R$ 100 por mês por 18 anos (216 meses), em dinheiro de hoje (IPCA ~4,5% a.a.; Focus: 5,1% 2026, 5,0% 2027)
n = 216; inf = 0.045
def fv(real):
    r = (1 + real)**(1/12) - 1
    return sum(100*(1 + r)**(n - 1 - k) for k in range(n))
print(100*n)                                         # 21.600 depositados
print(round(fv(-inf/(1 + inf))))                     # gaveta: ~15 mil de hoje
print(round(fv(0.02)))                               # poupança ~2% acima da inflação: ~26 mil (dizemos "uns 25 mil")
real = ((1.075*1.045 - 1)*0.85 + 1)/1.045 - 1        # Tesouro IPCA+/Educa+ ~IPCA+7,5% (16/11/2026), IR 15%
print(round(real, 4), round(fv(real)))               # ~5,7% real líquido -> ~37 mil de hoje
print(round(fv(real)*(1 + inf)**18))                 # na tela: ~81 mil nominais ("mais de 70 mil")
print(300000/216, 100/1400)                          # estudo B3/Plano 2022, renda R$ 2,9-7,1 mil: R$ 281-343 mil -> ~1.400/mês; 100 = 7%
print(round(fv(real)*2))                             # R$ 200/mês: ~74 mil de hoje
