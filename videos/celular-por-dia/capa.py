"""Capa do TikTok celular-por-dia. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_celular", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "CELULAR DE R$ 8 MIL", 540, 360, 84, CREME)
    numero_i(c, "CUSTA QUANTO", 540, 490, 110, CREME)
    numero_i(c, "POR DIA?", 540, 660, 170, GOLD)
    c.save(); c.translate(780, 1180); _m.fone(_m.TOP_COR, 1.05, rot=0.1)(c); c.restore()
    consultor_i(c, t, 290, 1640, 1.5, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.7)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
