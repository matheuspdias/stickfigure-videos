"""Contas do vídeo milhao-por-dia-1500 (pesquisa em 13/11/2026).
- Dias de 22/04/1500 a 14/11/2026: 192.324 (calendário gregoriano proléptico) -> R$ 192,3 bilhões a R$ 1 milhão/dia
- Notas de R$ 200: ~0,1 mm e ~1 g cada (valores típicos de cédula; ditos com "uns"/"quase")
- Mais rico do mundo (Forbes, nov/2026): Elon Musk, US$ 869 bi; a R$ 5,0-5,5 = R$ 4,3-4,8 tri -> 22 a 25x (roteiro: "mais de vinte vezes")
- CDI 13,65% a.a. (Selic 13,75%, Copom 04/11/2026) ~ 1,07% a.m. ("perto de um por cento ao mês"); IR 15% (aplicação longa)"""
from datetime import date
dias = (date(2026, 11, 14) - date(1500, 4, 22)).days
total = dias * 1e6
notas = total / 200
print("dias", dias, "| total R$ bi", round(total / 1e9, 1))
print("notas mi", round(notas / 1e6), "| altura km", round(notas * 0.1e-3 / 1e3, 1), "| peso t", round(notas * 1e-3 / 1e3))
print("contando 1/s: anos", round(notas / (365.25 * 86400), 1))
for usd in (5.0, 5.5):
    print("Musk / voce @", usd, round(869e9 * usd / total, 1), "x")
for am in (0.0100, 0.0107):
    print("rende/dia liquido @", am, round(total * am * 0.85 / 30 / 1e6, 1), "mi")
