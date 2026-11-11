"""Capa do TikTok ana-bruno-black-friday. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_bf", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1080))
    _m.faixa_bf(c, t, 330)
    numero_i(c, "À VISTA -10%", 540, 520, 120, VERDE, contorno=CREME)
    numero_i(c, "OU", 540, 650, 90, CREME)
    numero_i(c, "10X SEM JUROS?", 540, 780, 110, GOLD)
    pessoa(c, t, 240, 1640, 1.45, "ana", poses=((0, "thumb"),), exprs=((0, "grin"),), look=0.4)
    pessoa(c, t, 850, 1640, 1.45, "bruno", poses=((0, "hips"),), exprs=((0, "confident"),), look=-0.4)
    consultor_i(c, t, 545, 1660, 1.1, poses=((0, "think"),), exprs=((0, "think"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
