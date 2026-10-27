# Contas do exemplo: financiamento de carro de R$ 60 mil
# Taxa média BCB (aquisição de veículos PF), ago/2026: 26,42% a.a. ~= 1,97% a.m.
CARRO = 60_000
ENTRADA = 0.20 * CARRO          # 12.000
FIN = CARRO - ENTRADA           # 48.000
TAXA_AA = 0.2642
i = (1 + TAXA_AA) ** (1 / 12) - 1


def pmt(pv, i, n):
    return pv * i / (1 - (1 + i) ** -n)


def saldo(pv, i, n, k):
    p = pmt(pv, i, n)
    return pv * (1 + i) ** k - p * ((1 + i) ** k - 1) / i


def iof(pv, i, n):
    # IOF PF: 0,0082% ao dia sobre cada amortização (teto 365 dias) + 0,38% adicional
    p = pmt(pv, i, n)
    total, s = 0.38 / 100 * pv, pv
    for k in range(1, n + 1):
        amort = p - s * i
        s -= amort
        dias = min(30 * k, 365)
        total += amort * 0.000082 * dias
    return total


print(f"taxa mensal: {i*100:.3f}%")
for n in (36, 48, 60, 72):
    p = pmt(FIN, i, n)
    print(f"{n}x: parcela R$ {p:,.0f}  total R$ {p*n:,.0f}  juros R$ {p*n-FIN:,.0f}  "
          f"(+entrada: carro sai por R$ {p*n+ENTRADA:,.0f})  IOF ~R$ {iof(FIN, i, n):,.0f}")


def valor_carro(m, perda1=0.15, perda_dep=0.10):
    # 15% no primeiro ano (faixa típica 10-20%), depois ~10% ao ano (8-12%)
    anos = m / 12
    if anos <= 1:
        return CARRO * (1 - perda1 * anos)
    return CARRO * (1 - perda1) * (1 - perda_dep) ** (anos - 1)


print("\nDesvalorização x dívida (saldo devedor)")
for nome, pv, n in (("20% entrada 48x", FIN, 48), ("sem entrada 60x", CARRO, 60),
                    ("10% entrada 60x", 0.9 * CARRO, 60)):
    print(nome)
    for m in (0, 6, 12, 18, 24, 30, 36, 42, 48):
        if m > n:
            break
        print(f"  mês {m:2d}: carro R$ {valor_carro(m):7,.0f}  dívida R$ {saldo(pv, i, n, m):7,.0f}")
