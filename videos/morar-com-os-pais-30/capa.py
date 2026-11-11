"""Capa do TikTok morar-com-os-pais-30. O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_morar", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1080))
    numero_i(c, "MORAR COM", 540, 360, 130, CREME)
    numero_i(c, "OS PAIS AOS 30", 540, 500, 100, CREME)
    numero_i(c, "VERGONHA?", 540, 660, 150, VERMELHO, contorno=CREME)
    c.save(); c.translate(540, 820); _m.selo("OU ESTRATÉGIA?", VERDE, 80, CREME)(c); c.restore()
    pessoa(c, t, 240, 1640, 1.45, "carla", poses=((0, "hips"),), exprs=((0, "confident"),), look=0.4)
    pessoa(c, t, 850, 1640, 1.45, "lucas", poses=((0, "arms_up"),), exprs=((0, "grin"),), look=-0.4)
    consultor_i(c, t, 545, 1660, 1.1, poses=((0, "think"),), exprs=((0, "think"),), look=0.0)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
