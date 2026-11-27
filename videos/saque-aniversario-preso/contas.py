"""Contas de "Saque-aniversário: Ana x Bruno, demitidos" (27/11/2026).
Salário R$ 3.000, 5 anos de empresa. FGTS: 8% ao mês + 13º + 1/3 de férias = 8% de 13,33 salários/ano; rende 3% a.a. + TR (~3,5% a.a. aqui).
Saque-aniversário: tabela da Lei 13.932/2019 (alíquota + parcela adicional por faixa), saca 1x por ano.
Demissão sem justa causa: multa de 40% sobre TODOS os depósitos do contrato (corrigidos), mesmo os já sacados.
Quem está no saque-aniversário recebe só a multa; o saldo fica preso e volta aos poucos, 1x por ano.
Exceção da MP 1.290/2025 só para demissões de 01/01/2020 a 23/12/2025: não vale para quem for demitido agora."""
TAB = [(500, .50, 0), (1000, .40, 50), (5000, .30, 150), (10000, .20, 650), (15000, .15, 1150), (20000, .10, 1900), (1e12, .05, 2900)]


def saque(s):
    for lim, a, p in TAB:
        if s <= lim:
            return min(s, s * a + p)


dep_ano = 3000 * 0.08 * (13 + 1 / 3)
r = 0.035
ana = bruno = base_multa = 0.0
sacado = 0
for ano in range(1, 6):
    for mes in range(12):
        ana = ana * (1 + r) ** (1 / 12) + dep_ano / 12
        bruno = bruno * (1 + r) ** (1 / 12) + dep_ano / 12
        base_multa = base_multa * (1 + r) ** (1 / 12) + dep_ano / 12
    if ano < 5:          # o 5º aniversário ainda não chegou quando ela é demitida
        s = saque(ana); ana -= s; sacado += s
        print(f"ano {ano}: Ana saca {s:.0f}, fica {ana:.0f}")
multa = 0.40 * base_multa
print(f"depósito/ano {dep_ano:.0f} | multa {multa:.0f}")
print(f"Bruno na demissão: saldo {bruno:.0f} + multa {multa:.0f} = {bruno + multa:.0f}")
print(f"Ana na demissão: multa {multa:.0f}; preso {ana:.0f}; já tinha sacado {sacado:.0f}; próximo saque anual {saque(ana):.0f}")
