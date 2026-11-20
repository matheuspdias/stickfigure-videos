# R$ 200 mil: quitar o financiamento ou deixar rendendo? (Selic 13,75%, Copom 04/11/2026; CDI ~13,65%)
cdi = 0.1365
liq = cdi * (1 - 0.15)            # IR 15% (prazo > 2 anos): ~11,6% a.a.
print(liq, 200000 * liq)          # ~R$ 23,2 mil no 1º ano
print(200000 * 0.12)              # contrato 12% a.a. (com TR): ~R$ 24 mil de juros no 1º ano -> quitar ganha (+ seguro MIP/DFI)
print(200000 * 0.08)              # contrato 8% a.a. (com TR): ~R$ 16 mil -> render ganha ~R$ 7 mil/ano
print(200000 * liq - 200000 * 0.08)
# Simplificação: 1º ano, saldo de R$ 200 mil; juros do contrato sobre o saldo devedor (cai com as parcelas).
