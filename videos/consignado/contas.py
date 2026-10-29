# Contas do exemplo: empréstimo consignado CLT (Crédito do Trabalhador)
# Taxas médias BCB, ago/2026 (SGS 20744 e 20742):
#   consignado privado (CLT): 3,79% a.m. (56,3% a.a.)
#   crédito pessoal não consignado: 6,39% a.m. (110,2% a.a.)
# Teto com garantia de FGTS (Res. CGCONSIG 3 / Portaria MTE 1.115/2026): 1,99% a.m.
VALOR = 5_000
N = 24
TAXAS = {"consignado CLT (média BC)": 0.0379,
         "pessoal não consignado (média BC)": 0.0639,
         "teto com garantia FGTS": 0.0199}
SALARIO = 2_500   # líquido, "na mão"
MARGEM = 0.35


def pmt(pv, i, n):
    return pv * i / (1 - (1 + i) ** -n)


for nome, i in TAXAS.items():
    p = pmt(VALOR, i, N)
    print(f"{nome}: {i*100:.2f}% a.m. = {((1+i)**12-1)*100:.1f}% a.a. | "
          f"parcela R$ {p:,.2f} | total R$ {p*N:,.2f} | juros R$ {p*N-VALOR:,.2f} "
          f"({(p*N-VALOR)/VALOR*100:.0f}% do valor)")

lim = SALARIO * MARGEM
print(f"margem: 35% de R$ {SALARIO:,} = R$ {lim:,.2f}; sobra R$ {SALARIO-lim:,.2f}")
p = pmt(VALOR, TAXAS['consignado CLT (média BC)'], N)
print(f"parcela do exemplo = {p/SALARIO*100:.1f}% do salário; sobra R$ {SALARIO-p:,.2f}")
