# Primeiros R$ 10 mil: CDI 13,65% (Selic 13,75%, Copom 04/11/2026), IR 17,5% (prazo 1-2 anos) -> ~11,26% a.a. líquido
# poupança ~0,5% + TR (~0,15%/mês) -> ~8,1% a.a.
def meses(dep, rate_a, extra=0, extra_m=()):
    r = (1 + rate_a) ** (1 / 12) - 1; s = 0; m = 0
    while s < 10000:
        m += 1; s = s * (1 + r) + dep
        if m in extra_m: s += extra
    return m, round(s)
net = 0.1365 * (1 - 0.175); pou = (1.005 * 1.0015) ** 12 - 1
for d in (300, 500, 1000): print(d, meses(d, net))           # 30 (2,5 anos), 19 (1 ano e 7), 10 meses
r = (1 + net) ** (1/12) - 1; s = p = 0; rp = (1 + pou) ** (1/12) - 1
for m in range(19): s = s*(1+r)+500; p = p*(1+rp)+500
print(round(s - p))                                            # ~R$ 230 a mais que a poupança em 19 meses
print(meses(500, net, 1000, (1, 13)))                          # R$ 1.000 do 13º em cada dezembro: 15 meses
