"""Contas do vídeo "À vista com desconto ou parcelado sem juros?" (premissas conferidas em 21/10/2026).

Fontes: Selic 13,75% (Copom, 16/9/2026); CDI ~ Selic - 0,10 p.p.; IR da renda fixa pela tabela regressiva
(22,5% até 180 dias, 20% de 181 a 360; a MP 1.303/2025 caducou); Abecs 1T26: R$ 390,5 bi parcelados sem juros,
43,2% das compras no cartão; rotativo 444,9% a.a. (BC, ago/2026).
Modelo: o dinheiro fica numa aplicação de liquidez diária a 100% do CDI; cada parcela vence a cada 30 dias
(a 1ª, 30 dias depois da compra) e é paga com o dinheiro que estava aplicado desde o dia da compra.
"""
SELIC = 0.1375
CDI = SELIC - 0.0010
ROTATIVO = 4.449
g = (1 + CDI) ** (1 / 12) - 1          # rendimento bruto por mês (30 dias)


def ir(dias):
    return .225 if dias <= 180 else .20 if dias <= 360 else .175 if dias <= 720 else .15


def fator_liq(k):
    """quanto R$ 1 aplicado hoje vale líquido depois de k meses"""
    return 1 + ((1 + g) ** k - 1) * (1 - ir(30 * k))


def preciso_hoje(parcela, n):
    """quanto precisa estar aplicado hoje para pagar n parcelas"""
    return sum(parcela / fator_liq(k) for k in range(1, n + 1))


def taxa_embutida(preco_vista, parcela, n):
    lo, hi = 0.0, 0.2
    for _ in range(200):
        i = (lo + hi) / 2
        pv = sum(parcela / (1 + i) ** k for k in range(1, n + 1))
        lo, hi = (i, hi) if pv > preco_vista else (lo, i)
    return i


print(f"CDI {CDI:.2%} a.a. = {g:.3%} bruto/mês; líquido 6m {(fator_liq(6)-1):.2%}, 10m {(fator_liq(10)-1):.2%}")
print(f"líquido médio ao mês (10m): {fator_liq(10) ** (1/10) - 1:.3%}")

PRECO, N, DESC = 3000, 10, 0.10
P = PRECO / N
VISTA = PRECO * (1 - DESC)
hoje = preciso_hoje(P, N)
print(f"\nTV de {PRECO}: 10x de {P:.0f} ou à vista {VISTA:.0f}")
print(f"para pagar as 10 parcelas basta ter aplicado hoje: {hoje:.2f}  -> o parcelado 'custa' hoje {hoje:.0f}")
print(f"desconto de equilíbrio 10x: {1 - hoje / PRECO:.2%}")

# Carla (à vista) x Diego (parcela), os dois com R$ 3.000 aplicados
carla = (PRECO - VISTA) * fator_liq(N)
saldo = PRECO
diego_extrato = []
# Diego: tira de cada "envelope" o necessário; equivalente a sobrar (PRECO - hoje) aplicado por 10 meses
diego = (PRECO - hoje) * fator_liq(N)
print(f"\nCarla paga {VISTA:.0f}, sobra {PRECO-VISTA:.0f} aplicado 10 meses -> {carla:.2f}")
print(f"Diego mantém {PRECO} aplicado e paga {P:.0f}/mês -> sobra {diego:.2f} no fim")
print(f"diferença: {carla - diego:.2f} a favor da Carla")

# rendimento do Diego em 10 meses (juros líquidos ganhos)
print(f"juros líquidos que o Diego ganhou: {diego - 0:.0f} (sobra) ; o desconto da Carla vale {PRECO-VISTA:.0f} no dia")

i = taxa_embutida(VISTA, P, N)
print(f"\njuros embutidos no 'sem juros' com 10% de desconto: {i:.2%} ao mês = {(1+i)**12-1:.1%} ao ano")
print(f"aplicação líquida rende ~{fator_liq(10)**(1/10)-1:.2%} ao mês")

print("\nDesconto de equilíbrio por número de parcelas (acima disso, à vista ganha):")
for n in (2, 3, 4, 5, 6, 8, 10, 12):
    p = PRECO / n
    print(f"  {n:2d}x: {1 - preciso_hoje(p, n) / PRECO:.2%}   (metade de n = {n/2:.1f}%)")

# desconto de 3% em 10x
for d in (0.03, 0.05, 0.07, 0.15):
    v = PRECO * (1 - d)
    print(f"desconto {d:.0%}: à vista {v:.0f}; Carla fica com {(PRECO - v)*fator_liq(N):.0f} x Diego {diego:.0f}")

# juros embutidos para 5% e 15%
for d in (0.05, 0.15):
    ii = taxa_embutida(PRECO * (1 - d), P, N)
    print(f"desconto {d:.0%}: juros embutidos {ii:.2%}/mês = {(1+ii)**12-1:.1%} a.a.")

# 5 compras parceladas: o Diego
compras = [("TV", 3000, 10), ("celular", 2400, 12), ("geladeira", 3600, 12), ("air fryer", 600, 6), ("tênis", 500, 5)]
tot = sum(v / n for _, v, n in compras)
print("\nparcelas do Diego:", [(nm, round(v / n)) for nm, v, n in compras], f"total {tot:.0f}/mês")
print(f"sobre renda de 4.000: {tot/4000:.0%}")

# atrasou uma fatura de 1.000 e caiu no rotativo por 1 mês
m_rot = (1 + ROTATIVO) ** (1 / 12) - 1
print(f"\nrotativo: {m_rot:.2%} ao mês; 1.000 no rotativo 1 mês = {1000*m_rot:.0f} de juros")
print("Abecs 1T26: R$ 390,5 bi sem juros, 43,2% do cartão; 7 a 12 parcelas = 35,4% do PSJ")
