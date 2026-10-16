P=240000; n=360; ra=0.0766
i=(1+ra)**(1/12)-1
inom=ra/12
def sac(i, extra=0, lump=None, mode='prazo'):
    s=P; tot=0; m=0; A=P/n; rem=n
    while s>0.005:
        m+=1
        j=s*i; a=min(A,s); s-=a; tot+=j+a
        if extra and s>0:
            e=min(extra,s); s-=e; tot+=e
        if lump and m==lump[0] and s>0:
            s-=lump[1]; tot+=lump[1]
            if mode=='parcela':
                rem_m=n-m; A=s/rem_m
        if m>2000: break
    return tot,m
for name,ii in [('efetiva',i),('nominal',inom)]:
    b,_=sac(ii); e,m=sac(ii,200)
    print(name,'mensal',round(ii*100,4),'total',round(b),'parc1',round(P/n+P*ii))
    print('  +200: total',round(e),'meses',m,'anos antes',round((n-m)/12,2),'economia',round(b-e))
    for mo,lab in [(1,'inicio'),(12,'fim ano1'),(13,'ano2'),(229,'ano20 inicio'),(240,'fim ano20')]:
        tp,mp=sac(ii,lump=(mo,10000),mode='prazo'); tq,mq=sac(ii,lump=(mo,10000),mode='parcela')
        print('  10k mes',mo,lab,'prazo econ',round(b-tp),'meses',mp,'| parcela econ',round(b-tq))
