"""Simulação Alugar x Comprar (Faz a Conta). Valores nominais, mensais."""
import sys

def m(a): return (1+a)**(1/12)-1

def corrida(preco=300_000, entrada_pct=0.20, juro=0.115, anos=30, prazo=30,
            yield_aluguel=0.06, valoriz=0.045, invest=0.10, custos_pct=0.04,
            manut_pct=0.005, sistema="SAC", comprador_investe=True, verbose=False):
    n = prazo*12
    fin = preco*(1-entrada_pct); entrada = preco*entrada_pct
    i = m(juro); r = m(invest)
    custos = preco*custos_pct
    inq = entrada + custos           # inquilino investe entrada + custos que não pagou
    comp = 0.0
    saldo = fin; juros_tot = 0; pagos = 0
    aluguel_ini = preco*yield_aluguel/12
    hist = []
    if sistema == "PRICE":
        pmt_price = fin*i/(1-(1+i)**-n)
    for k in range(anos*12):
        ano = k//12
        fator = (1+valoriz)**ano
        aluguel = aluguel_ini*fator
        manut = preco*manut_pct/12*fator
        if k < n:
            jur = saldo*i
            amort = fin/n if sistema=="SAC" else pmt_price-jur
            parcela = jur+amort
            saldo -= amort; juros_tot += jur
        else:
            parcela = 0
        custo_comp = parcela+manut
        dif = custo_comp-aluguel
        inq *= 1+r; comp *= 1+r
        if dif > 0: inq += dif
        elif comprador_investe: comp += -dif
        pagos += aluguel
        if k % 12 == 11:
            imovel = preco*(1+valoriz)**(ano+1)
            hist.append((ano+1, round(imovel+comp-max(saldo,0)), round(inq), round(parcela), round(aluguel)))
    return dict(juros_tot=juros_tot, hist=hist, alug_total=pagos,
                parcela1=fin/n+fin*i if sistema=="SAC" else pmt_price,
                aluguel_ini=aluguel_ini, inq_ini=entrada+custos)

if __name__ == "__main__":
    b = corrida()
    print("BASE: parcela1 %.0f  aluguel1 %.0f juros totais %.0f aluguel total pago %.0f" % (b['parcela1'], b['aluguel_ini'], b['juros_tot'], b['alug_total']))
    for h in b['hist']:
        if h[0] in (1,2,3,5,10,15,20,25,30): print(h)
    p = corrida(sistema="PRICE"); print("PRICE parcela %.0f juros %.0f fim" % (p['parcela1'], p['juros_tot']), p['hist'][-1])
    nb = corrida(comprador_investe=False); print("comprador não investe sobra:", nb['hist'][-1])
    print("\n-- sensibilidade (patrimônio comprador / inquilino aos 30 anos) --")
    for inv in (0.08,0.09,0.10,0.11,0.12):
        h = corrida(invest=inv)['hist'][-1]; print("invest %.0f%%: %s  razao %.2f" % (inv*100, h[1:3], h[2]/h[1]))
    for y in (0.04,0.05,0.06,0.07,0.08):
        h = corrida(yield_aluguel=y)['hist'][-1]; print("yield %.0f%%: %s razao %.2f" % (y*100, h[1:3], h[2]/h[1]))
    for j in (0.08,0.09,0.10,0.115,0.13):
        h = corrida(juro=j)['hist'][-1]; print("juro %.1f%%: %s razao %.2f" % (j*100, h[1:3], h[2]/h[1]))
    for v in (0.03,0.045,0.06,0.07):
        h = corrida(valoriz=v)['hist'][-1]; print("valoriz %.1f%%: %s razao %.2f" % (v*100, h[1:3], h[2]/h[1]))
    # inquilino que não investe nada (gasta a diferença)
    print("\n-- MCMV faixa 3: 35% entrada, 7.66% --")
    mc = corrida(entrada_pct=0.35, juro=0.0766)
    print("parcela1 %.0f juros %.0f" % (mc['parcela1'], mc['juros_tot']), mc['hist'][-1], [h for h in mc['hist'] if h[0] in (1,5,10,20)])
    mc2 = corrida(entrada_pct=0.20, juro=0.0766); print("MCMV 20% entrada", mc2['hist'][-1], "parcela1 %.0f"%mc2['parcela1'])
    # base with 35% entrada for fair comparison
    b35 = corrida(entrada_pct=0.35); print("SBPE 35% entrada", b35['hist'][-1])

def extra():
    # ano de cruzamento e totais
    from math import isclose
    preco=300_000; fin=240_000; n=360; i=m(0.115)
    man=sum(preco*0.005/12*(1.045)**(k//12) for k in range(360))
    print("manutencao total %.0f" % man)
    for k in range(360):
        ano=k//12; parc=fin/n+(fin-fin/n*k)*i; cc=parc+preco*0.005/12*1.045**ano; al=1500*1.045**ano
        if cc<al: print("cruzamento mes",k+1,"ano",ano+1,round(parc),round(al)); break
    inf=1.045**30; print("deflator 30a %.2f" % inf)
    b=corrida(); print("reais de hoje:", round(b['hist'][-1][1]/inf), round(b['hist'][-1][2]/inf))
    # inquilino gastador: só a entrada+custos investida, nada mensal
    print("72k a 10%% por 30 anos: %.0f" % (72000*1.1**30))
    # breakevens
    def be(key, lo, hi):
        for _ in range(60):
            mid=(lo+hi)/2; h=corrida(**{key:mid})['hist'][-1]
            if (h[2]>h[1]) == (corrida(**{key:lo})['hist'][-1][2]>corrida(**{key:lo})['hist'][-1][1]): lo=mid
            else: hi=mid
        return mid
    print("BE invest", be('invest',0.08,0.12)); print("BE yield", be('yield_aluguel',0.05,0.08))
    print("BE juro", be('juro',0.08,0.13)); print("BE valoriz", be('valoriz',0.03,0.07))
    # MCMV breakevens
    print("MCMV hist", [h for h in corrida(entrada_pct=0.35, juro=0.0766)['hist'] if h[0] in (2,3,5,10,15,20,25,30)])
    print("base hist inq lead anos", [(h[0],h[2]-h[1]) for h in corrida()['hist'] if h[0]%5==0])
    # quem mora em cidade com yield baixo (SP ~5%)? and selic hoje cdi liquido
    print("cdi liq 13.65*0.85=%.2f"%(13.65*0.85))
    # base, comprador e inquilino ambos sem investir nada mensal
    print("comprador nao investe vs inq so entrada", corrida(comprador_investe=False)['hist'][-1][1], round(72000*1.1**30))
extra()
