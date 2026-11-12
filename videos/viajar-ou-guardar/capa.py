"""Capa do TikTok viajar-ou-guardar. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_viajar", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "vermelho", holofote=(540, 1080))
    numero_i(c, "VIAJAR TODO ANO", 540, 360, 110, CREME)
    numero_i(c, "TE CUSTA", 540, 490, 100, CREME)
    numero_i(c, "R$ 70 MIL?", 540, 660, 170, GOLD)
    c.save(); c.translate(540, 1460); _m.mala(c, 1.0); c.restore()
    pessoa(c, t, 220, 1640, 1.45, "ana", poses=((0, "arms_up"),), exprs=((0, "grin"),), look=0.4)
    pessoa(c, t, 860, 1640, 1.45, "bruno", poses=((0, "hips"),), exprs=((0, "confident"),), look=-0.4)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
