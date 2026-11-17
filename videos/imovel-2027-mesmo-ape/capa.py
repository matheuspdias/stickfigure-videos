"""Capa do TikTok imovel-2027-mesmo-ape. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1250))
    numero_i(c, "MESMO APÊ", 540, 340, 130, CREME)
    numero_i(c, "PARCELA DIFERENTE", 540, 470, 84, GOLD)
    for k, (q, x, v, cor) in enumerate((("casal", 230, "R$ 1.467", VERDE), ("bruno", 540, "R$ 1.988", GOLD), ("carla", 850, "R$ 2.783", VERMELHO))):
        numero_i(c, v, x, 640, 58, cor)
        if q == "casal":
            pessoa(c, t, x - 55, 1230, 0.75, "ana", look=0.3); pessoa(c, t, x + 55, 1230, 0.75, "diego", look=-0.3)
        else:
            pessoa(c, t, x, 1230, 0.85, q, poses=((0, "head" if q == "carla" else "stand"),),
                   exprs=((0, "shocked" if q == "carla" else "neutral"),), look=0.0)
    numero_i(c, "R$ 5 MIL", 230, 1320, 44, CREME); numero_i(c, "R$ 12 MIL", 540, 1320, 44, CREME); numero_i(c, "R$ 14 MIL", 850, 1320, 44, CREME)
    c.save(); c.translate(540, 1470); c.rotate(-0.03)
    rr(c, -440, -60, 880, 120, 22); rgb(c, VERMELHO); c.fill()
    numero_i(c, "QUEM GANHA MAIS PAGA MAIS", 0, 0, 46, CREME); c.restore()
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
