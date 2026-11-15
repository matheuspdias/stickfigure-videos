"""Capa do TikTok centavo-dobrando-30-dias. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "verde", holofote=(540, 1100))
    numero_i(c, "R$ 0,01", 540, 390, 200, GOLD)
    numero_i(c, "DOBRANDO TODO DIA", 540, 560, 84, CREME)
    numero_i(c, "QUANTO DÁ EM 30 DIAS?", 540, 690, 66, CREME, contorno=NAVY)
    chuva_dinheiro(c, 1.0, 0.0, n=16, seed=7)
    c.save(); c.translate(780, 1080); c.rotate(0.08)
    c.new_sub_path(); c.arc(0, 0, 110, 0, 6.283); rgb(c, VERMELHO); c.fill()
    c.new_sub_path(); c.arc(0, 0, 110, 0, 6.283); rgb(c, TINTA); c.set_line_width(8); c.stroke()
    numero_i(c, "x2", 0, 6, 110, CREME); c.restore()
    pessoa(c, t, 400, 1640, 1.6, "lucas", poses=((0, "head"),), exprs=((0, "shocked"),), look=0.3)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
