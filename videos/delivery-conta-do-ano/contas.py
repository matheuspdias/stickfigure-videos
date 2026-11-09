# Delivery 3x por semana: a conta do ano (valores de exemplo, redondos)
lanche, entrega, servico = 35, 8, 2
pedido = lanche + entrega + servico          # 45
semana = 3 * pedido                          # 135
mes = semana * 52 / 12                       # 585 ("quase seiscentos")
pedidos_ano = 3 * 52                         # 156
ano = pedidos_ano * pedido                   # 7020
taxas_ano = pedidos_ano * (entrega + servico)  # 1560
casa = 15
economia_ano = (pedido - casa) * 52          # 1560
print(pedido, semana, round(mes), pedidos_ano, ano, taxas_ano, economia_ano)
assert (pedido, semana, ano, taxas_ano, economia_ano) == (45, 135, 7020, 1560, 1560)
