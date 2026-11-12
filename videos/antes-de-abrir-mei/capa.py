"""Capa do TikTok antes-de-abrir-mei (série ep. 6). O perfil corta em 3:4: o essencial fica entre y 260 e 1660."""
from engine import *
VERTICAL = True
from ilustrado import *
import importlib.util, os
_spec = importlib.util.spec_from_file_location("cenas_mei", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scenes.py"))
_m = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_m)

STYLE = "ilustrado"


def capa(c, t):
    fundo_marca(c, t, "navy", holofote=(540, 1080))
    numero_i(c, "O QUE NINGUÉM", 540, 340, 100, CREME)
    numero_i(c, "TE CONTA ANTES DE", 540, 460, 80, CREME)
    numero_i(c, "ABRIR MEI", 540, 640, 170, GOLD)
    c.save(); c.translate(540, 820); _m.selo("EP. 6", VERMELHO, 60, CREME)(c); c.restore()
    c.save(); c.translate(790, 1230); c.scale(0.9, 0.9); _m.tela_cnpj(c); c.restore()
    consultor_i(c, t, 290, 1640, 1.5, poses=((0, "finger_up"),), exprs=((0, "worried"),), look=0.7)
    numero_i(c, "FAZ A CONTA", 540, 1760, 64, CREME, contorno=NAVY)


SCENES = [(0, 999, capa)]
