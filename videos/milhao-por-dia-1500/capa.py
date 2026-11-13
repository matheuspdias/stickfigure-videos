"""Capa do TikTok milhao-por-dia-1500. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_1500", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    _m.mar_1500(c, t)
    luz("dia")
    numero_i(c, "R$ 1 MILHÃO POR DIA", 540, 360, 84, GOLD)
    numero_i(c, "DESDE 1500", 540, 500, 130, CREME, contorno=NAVY)
    numero_i(c, "QUANTO VOCÊ TERIA?", 540, 650, 76, GOLD)
    pessoa(c, t, 280, 1640, 1.5, "lucas", poses=((0, "arms_up"),), exprs=((0, "shocked"),), look=0.6)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
