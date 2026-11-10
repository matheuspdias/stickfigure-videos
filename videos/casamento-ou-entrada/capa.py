"""Capa do TikTok casamento-ou-entrada. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_casamento", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1080))
    _m.luzinhas(c, t, 60, 2, 60)
    numero_i(c, "R$ 50 MIL", 540, 380, 170, GOLD)
    numero_i(c, "NA FESTA", 540, 540, 110, CREME)
    numero_i(c, "OU NO APÊ?", 540, 690, 130, CREME)
    pessoa(c, t, 240, 1640, 1.45, "carla", poses=((0, "arms_up"),), exprs=((0, "grin"),), look=0.4,
           roupa="vestido", cor_roupa=(0.97, 0.96, 0.93))
    pessoa(c, t, 850, 1640, 1.45, "diego", poses=((0, "hips"),), exprs=((0, "confident"),), look=-0.4)
    consultor_i(c, t, 545, 1660, 1.1, poses=((0, "think"),), exprs=((0, "think"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
