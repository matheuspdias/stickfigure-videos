# Comprar ou alugar em 2026 (Parte 2 de 3): a conta de 10 anos com os números de 2026.
# Mesmo apê da Parte 1: R$ 300 mil, aluguel R$ 1.500 (0,5%/mês), reajuste 4,5%/ano (IPCA/IGP-M perto disso).
# Compra: entrada 20% (R$ 60 mil) + ITBI e cartório ~4% (R$ 12 mil; ITBI SP 3% + escritura/registro), SAC 30 anos, 12% a.a. com TR.
# Quem aluga investe a entrada + os R$ 12 mil + a diferença parcela-aluguel todo mês.
# Investimento: CDI de 2026 (~13,65% a.a.) com IR de 15% => ~11,6% a.a. líquido, mantido 10 anos (premissa "números de 2026").
# Valorização do imóvel: 5% a.a. (premissa da série).
V=300_000; ent=0.2*V; doc=0.04*V; fin=V-ent; n=360
i=1.12**(1/12)-1
def sim(liq_aa, invest_dif=True, valor=0.05):
    r=(1+liq_aa)**(1/12)-1
    amort=fin/n; saldo=fin; inv=ent+doc; alug=1500; tot_j=0; tot_alug=0
    for m in range(120):
        j=saldo*i; parc=amort+j; saldo-=amort; tot_j+=j
        if m and m%12==0: alug*=1.045
        tot_alug+=alug
        inv=inv*(1+r)+((parc-alug) if invest_dif else 0)
    imov=V*(1+valor)**10
    return dict(parc_ult=parc, alug_fim=alug, saldo=saldo, imov=imov, patr_compra=imov-saldo, inv=inv, tot_j=tot_j, tot_alug=tot_alug)
liq=0.1365*0.85
s=sim(liq)
for k,v in s.items(): print(f"{k:12s} {v:,.0f}")
print("liq a.a.", liq)
print("diferença", s['inv']-s['patr_compra'])
s2=sim(liq, invest_dif=False); print("se gastar a diferença:", f"{s2['inv']:,.0f}")
s3=sim(0.10*1); print("se investir a 10% a.a.:", f"{s3['inv']:,.0f}")
print("parcela 1", fin/n+fin*i)
