"""Capa do TikTok carro-custa-aluguel. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "SEU CARRO", 540, 380, 130, CREME)
    numero_i(c, "CUSTA MAIS QUE", 540, 520, 100, CREME)
    numero_i(c, "UM ALUGUEL", 540, 660, 130, GOLD)
    c.save(); c.translate(760, 1560); c.scale(1.1, 1.1); carro_i(c, 0, (0.86, 0.26, 0.22)); c.restore()
    consultor_i(c, t, 300, 1640, 1.55, poses=((0, "head"),), exprs=((0, "shocked"),), look=0.5)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
