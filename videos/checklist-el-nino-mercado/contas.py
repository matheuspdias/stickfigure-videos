"""Contas do Checklist "El Niño vai encarecer o mercado: 3 passos" (24/11/2026, 10h).
Fontes (nov/2026): estudo citado pela Exame (El Niño soma 1,02 a 3,4 p.p. na inflação de alimentos; cenário extremo tipo
2015-16: 6,78 p.p.); ONS/BRA1: forte a muito forte em jan-mar/2027; proteínas sobem pela ração (milho/soja).
Preços de referência (estimativa, por isso "uns"): carne vermelha ~R$ 45/kg, frango ~R$ 20/kg, dúzia de ovos ~R$ 12."""
mercado = 800
for pp in (1.02, 3.4, 6.78):
    print(f"+{pp} p.p. -> R$ {mercado*pp/100:.0f}/mes")
extra = round(mercado * 0.07)            # 56
carne, frango, ovos = 45, 20, 12
sem = carne - frango                      # 25 (com ovos, 33: usa o menor)
mes = sem * 4                              # 100
print("pior cenario", extra, "economia/semana", sem, "mes", mes, "sobra", mes - extra)
