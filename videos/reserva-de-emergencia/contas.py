"""Contas do vídeo "Se você fosse demitido hoje, quanto tempo aguentaria?" (premissas conferidas em 25/10/2026).

Fontes:
- Selic 13,75% a.a. (Copom, 16/9/2026; próxima reunião 3-4/11/2026); CDI ~ Selic - 0,10 p.p. = 13,65% a.a.
- IR da renda fixa pela tabela regressiva (22,5% até 180 dias, 20% até 360, 17,5% até 720, 15% acima).
- Seguro-desemprego 2026 (MTE, vigente desde 11/1/2026): até R$ 2.222,17 -> 0,8 x salário médio;
  de R$ 2.222,18 a R$ 3.703,99 -> R$ 1.777,74 + 0,5 x o que passar de R$ 2.222,17; acima -> R$ 2.518,65 (teto).
  Piso R$ 1.621,00 (salário mínimo). 3 a 5 parcelas; 24 meses ou mais trabalhados -> 5 parcelas.
- Cheque especial: 8,00% ao mês (151,82% a.a.), Procon-SP, coleta de 2/10/2026 (também é o teto legal, Res. CMN 4.765/2019).
- Empréstimo pessoal: 8,55% ao mês (Procon-SP, 2/10/2026).
- PNAD Contínua 1º tri/2026 (IBGE): 6,6 milhões desocupados; 21,2% procuram há menos de 1 mês, 51,4% de 1 mês a
  menos de 1 ano, 10,9% de 1 a 2 anos, 16,5% há 2 anos ou mais (27,4% há 1 ano ou mais).
- IPCA 4,58% em 12 meses (setembro/2026).

Personagens (exemplo): salário de R$ 4.000 (salário médio dos últimos 3 meses), custo de vida de R$ 3.200 por mês,
guarda R$ 400 por mês (10% do salário). Mais de 2 anos de carteira -> 5 parcelas de seguro.
Na conta não entram rescisão nem FGTS (variam muito, e quem aderiu ao saque-aniversário não saca o saldo na demissão).
"""
SELIC = 0.1375
CDI = SELIC - 0.0010
g = (1 + CDI) ** (1 / 12) - 1
CHEQUE = 0.08
EMPREST = 0.0855


def ir(dias):
    return .225 if dias <= 180 else .20 if dias <= 360 else .175 if dias <= 720 else .15


def seguro(sal):
    if sal <= 2222.17:
        v = sal * 0.8
    elif sal <= 3703.99:
        v = 1777.74 + (sal - 2222.17) * 0.5
    else:
        v = 2518.65
    return max(v, 1621.00)


SAL, CUSTO, GUARDA = 4000, 3200, 400
SEG = seguro(SAL)
print(f"CDI {CDI:.2%} a.a. = {g:.3%} bruto/mês")
print(f"seguro-desemprego com salário de {SAL}: {SEG:.2f} por mês, 5 parcelas = {5*SEG:.2f}")
print(f"buraco por mês com seguro: {CUSTO-SEG:.2f}; sem seguro: {CUSTO}")
for s in (1621, 2000, 2500, 3000, 3500, 5000, 10000):
    print(f"  salário {s}: seguro {seguro(s):.2f}")

META = 6 * CUSTO
print(f"\nmeta de 6 meses do custo de vida: {META}; 3 meses: {3*CUSTO}; 12 meses: {12*CUSTO}")


def saldo_liquido(n):
    """saldo líquido de IR depois de n depósitos mensais de GUARDA (depósito no fim de cada mês)"""
    tot = 0
    for k in range(n):          # depósito feito no mês k+1, fica (n-1-k) meses aplicado
        m = n - 1 - k
        ganho = GUARDA * ((1 + g) ** m - 1)
        tot += GUARDA + ganho * (1 - ir(30 * m) if m else 1)
    return tot


def meses_ate(meta):
    n = 1
    while saldo_liquido(n) < meta:
        n += 1
    return n


for alvo in (CUSTO, 3 * CUSTO, META):
    n = meses_ate(alvo)
    print(f"até {alvo}: {n} meses ({n//12} anos e {n%12} meses), sem juros seriam {alvo/GUARDA:.0f} meses; "
          f"saldo {saldo_liquido(n):.2f}, do bolso {n*GUARDA}")
n6 = meses_ate(META)
print(f"juros líquidos na meta: {saldo_liquido(n6) - n6*GUARDA:.2f}")

# com o 13º (R$ 4.000 bruto ~ líquido ~ R$ 3.600 na soma das parcelas) indo pra reserva no fim de cada ano
def meses_com_13(meta, extra=3600):
    saldo, n = 0.0, 0
    while saldo < meta:
        n += 1
        saldo = saldo * (1 + g * (1 - 0.175)) + GUARDA + (extra if n % 12 == 0 else 0)   # aproximação: rendimento líquido médio
    return n
print(f"aproximação com 13º de ~3.600 na reserva todo dezembro: {meses_com_13(META)} meses")

# ---------------------------------------------------------------- Bruno x Camila, 8 meses sem emprego
MESES = 8
gaps = [CUSTO - SEG if m < 5 else CUSTO for m in range(MESES)]
print(f"\nburacos mês a mês: {[round(x,2) for x in gaps]}  total {sum(gaps):.2f}")

# Bruno: sem reserva, cobre o buraco no cheque especial (8% ao mês)
divida = 0.0
for m, gap in enumerate(gaps, 1):
    divida = divida * (1 + CHEQUE) + gap
    print(f"  mês {m}: dívida do Bruno {divida:.2f}")
juros_bruno = divida - sum(gaps)
print(f"Bruno: usou {sum(gaps):.2f}, deve {divida:.2f} -> juros {juros_bruno:.2f}")
print(f"juros por mês sobre essa dívida: cheque {divida*CHEQUE:.2f}, empréstimo pessoal {divida*EMPREST:.2f}")
# quanto tempo leva pra quitar pagando 400 / 1.000 / 1.500 por mês a 8,55%
for p in (400, 1000, 1500):
    d, n = divida, 0
    while d > 0 and n < 600:
        d = d * (1 + EMPREST) - p
        n += 1
    print(f"  quitar a 8,55% pagando {p}/mês: {'nunca' if n >= 600 else f'{n} meses, pago {n*p - max(0,-d):.0f}'}")

# Camila: tem a reserva de 6 meses (19.200) aplicada a 100% do CDI há mais de 2 anos (IR 15% aprox.)
r_liq = g * (1 - 0.15)
res = META
for m, gap in enumerate(gaps, 1):
    res = res * (1 + r_liq) - gap
    print(f"  mês {m}: reserva da Camila {res:.2f}")
print(f"Camila: termina com {res:.2f} e nenhuma dívida")
print(f"diferença de patrimônio entre os dois no fim: {res + divida:.2f}")
print(f"meses para a Camila repor a reserva guardando 400 (aprox., sem juros): {(META-res)/GUARDA:.1f}")

# sem o seguro (ex.: autônomo / pediu demissão): quantos meses a reserva de 6 meses dura? 6. E o cheque especial em 6 meses?
d = 0
for m in range(6):
    d = d * (1 + CHEQUE) + CUSTO
print(f"\nsem seguro, 6 meses no cheque especial cobrindo 3.200: deve {d:.2f}")
