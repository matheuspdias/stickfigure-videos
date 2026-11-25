# Janeiro de 2027: contas que vêm todo ano (exemplo: salário R$ 3 mil, carro de R$ 40 mil em SP, 1 filho)
ipva = 40000 * 0.04          # SP: 4% para carro; 2027: 3% de desconto em janeiro ou 5x (calendário divulgado em nov/2026)
iptu = 1000                  # exemplo, varia muito por cidade
material = 500               # estimativa de lista básica por filho; Procon-SP: mesmo item varia até ~270% entre lojas
fatura = 1000                # exemplo: Natal + Black Friday na fatura de janeiro
total = ipva + iptu + material + fatura
print("ipva", ipva, "desconto 3%", ipva * 0.03, "5x", ipva / 5)
print("total", total, "salarios de 3 mil", round(total / 3000, 2))
seg_13 = 1500 - 249          # 2ª parcela do 13º de R$ 3 mil: metade menos o INSS do 13º inteiro (~R$ 249), IR zero em 2026
print("2a parcela", seg_13, "fração", round(seg_13 / total, 2))
