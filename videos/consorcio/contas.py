# Contas do exemplo: consórcio de veículo, carta de R$ 50 mil, 60 meses
# Premissas (pesquisadas em 29/10/2026):
#   taxa de administração 15% (faixa comum: 12% a 20%), fundo de reserva 2% (faixa: 1% a 3%)
#   seguro: varia; não entra na conta principal
#   financiamento de veículo PF: taxa média BCB ago/2026 = 26,42% a.a. (SGS 20749)
CARTA = 50_000
N = 60
ADM = 0.15
FR = 0.02
FIN_AA = 0.2642


def pmt(pv, i, n):
    return pv * i / (1 - (1 + i) ** -n)


def irr(fluxos, lo=-0.5, hi=0.5):
    def npv(r):
        return sum(f / (1 + r) ** k for k, f in enumerate(fluxos))
    for _ in range(200):
        mid = (lo + hi) / 2
        if npv(lo) * npv(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


taxas = CARTA * (ADM + FR)
total = CARTA + taxas
parc = total / N
print(f"taxas: 15% + 2% = 17% de R$ {CARTA:,} = R$ {taxas:,.0f}; total R$ {total:,.0f}; parcela R$ {parc:,.2f}")
print(f"só a taxa de adm: R$ {CARTA*ADM:,.0f}; por mês R$ {CARTA*ADM/N:,.2f}")

# custo anual equivalente se contemplado no 1º mês (melhor caso, parece um financiamento):
# paga a 1ª parcela no ato da adesão, recebe a carta no mês 1, paga as outras 59
fl = [-parc, CARTA - parc] + [-parc] * (N - 2)
i = irr(fl)
print(f"contemplado no mês 1: {i*100:.3f}% a.m. = {((1+i)**12-1)*100:.2f}% a.a.")
# versão simples: recebe hoje, paga 60 parcelas depois
i2 = irr([CARTA] + [-parc] * N)
print(f"(recebe hoje e paga 60x: {i2*100:.3f}% a.m. = {((1+i2)**12-1)*100:.2f}% a.a.)")
# sem fundo de reserva (se ele voltar no fim): só a adm
p3 = CARTA * (1 + ADM) / N
i3 = irr([CARTA] + [-p3] * N)
print(f"(só adm 15%: {((1+i3)**12-1)*100:.2f}% a.a.)")

# financiamento de R$ 50 mil em 60x na taxa média
im = (1 + FIN_AA) ** (1 / 12) - 1
pf = pmt(CARTA, im, N)
print(f"financiamento: {im*100:.3f}% a.m. | parcela R$ {pf:,.2f} | total R$ {pf*N:,.0f} | juros R$ {pf*N-CARTA:,.0f}")

# correção: carta e parcela sobem 5% ao ano (exemplo)
for a in range(0, 3):
    print(f"ano {a+1}: carta R$ {CARTA*1.05**a:,.0f}, parcela R$ {parc*1.05**a:,.2f}")

# lance embutido de 30%
le = CARTA * 0.30
print(f"lance embutido 30%: R$ {le:,.0f}; recebe R$ {CARTA-le:,.0f}")
