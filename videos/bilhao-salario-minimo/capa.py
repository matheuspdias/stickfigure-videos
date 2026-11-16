"""Capa do TikTok bilhao-salario-minimo. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    numero_i(c, "1 SALÁRIO MÍNIMO", 540, 380, 90, CREME)
    numero_i(c, "POR MÊS ATÉ", 540, 500, 80, CREME, contorno=NAVY)
    numero_i(c, "R$ 1 BILHÃO", 540, 660, 160, GOLD)
    numero_i(c, "QUANTOS ANOS?", 540, 820, 84, CREME, contorno=NAVY)
    chuva_dinheiro(c, 1.0, 0.0, n=14, seed=5)
    for i in range(10):
        c.save(); c.translate(800 + (i % 2) * 6, 1420 - i * 26); nota_i(c, "100", 300); c.restore()
    pessoa(c, t, 380, 1640, 1.55, "lucas", poses=((0, "head"),), exprs=((0, "shocked"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
