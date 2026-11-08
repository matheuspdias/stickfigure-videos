"""Contas do TikTok assinaturas-esquecidas (08/11/2026). Valores de exemplo, redondos e genéricos (sem marca)."""
itens = {"streaming 1": 45, "streaming 2": 30, "música": 25, "nuvem do celular": 10, "app do teste grátis": 20}
mes = sum(itens.values())
print("por mês:", mes, "| por ano:", mes * 12)
corte = itens["streaming 2"] + itens["app do teste grátis"]
print("cortando 2:", corte, "/mês |", corte * 12, "/ano")
assert (mes, mes * 12, corte, corte * 12) == (130, 1560, 50, 600)
