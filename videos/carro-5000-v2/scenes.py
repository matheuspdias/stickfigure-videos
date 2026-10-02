"""Carro de R$ 60 mil ganhando R$ 5 mil, versão 2: narração Calm Carlos (IA) + O Consultor.
Reaproveita as cenas do vídeo piloto (examples/carro-5000) re-sincronizadas por um mapa de tempos
(tempo da narração antiga -> tempo da narração nova, ancorado frase a frase)."""
import os, sys, importlib.util
import engine
from engine import *

_here = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("carro_v1", os.path.join(_here, "..", "..", "examples", "carro-5000", "scenes.py"))
old = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(old)
old.hero = engine.hero          # troca o boneco amarelo pelo Consultor
_other = old.other
old.other = lambda *a, **kw: _other(*a, **{**kw, "shirt": kw.get("shirt", ORANGE)})  # 2º personagem em laranja (contraste com o azul do Consultor)

# (tempo antigo, tempo novo) — âncoras nas frases/palavras-chave
A = [(0, 0), (1, 0.08), (6, 5.72), (8, 7.82), (13, 13.76), (18, 18.04), (22, 23.52), (27, 28.45), (29, 30.44),
     (31, 32.32), (32.4, 34.24), (34, 35.52), (36, 38.16), (36.5, 39.28), (37.3, 40.44), (38, 41.2), (38.7, 42.16),
     (40.4, 45.0), (41.6, 46.08), (43, 47.17), (46, 49.78), (50, 53.39), (52, 56.16), (55.2, 59.44), (57.5, 62.56),
     (58.6, 63.12), (60, 64.12), (61, 65.6), (62.1, 66.88), (63.1, 67.68), (65, 69.24), (67, 71.76), (73, 77.40),
     (74, 79.68), (77, 82.56), (80, 84.80), (81.4, 88.24), (82.4, 91.36), (87, 92.59), (90, 96.23), (92, 98.36),
     (95, 101.40), (96.4, 103.33), (99, 106.03), (106, 111.76), (109, 114.55), (112.2, 116.88), (113.7, 118.64),
     (115.2, 120.68), (116.7, 122.84), (118.2, 125.32), (121.2, 128.4), (124.6, 131.8), (125.2, 132.16),
     (129, 136.37), (134, 143.15), (134.4, 144.95), (135.3, 146.03), (136.4, 147.9), (140, 150.18), (143, 153.47),
     (145, 156.75), (148, 160.39), (149.8, 162.83), (151.3, 163.99), (152.6, 165.31), (154, 167.11), (155.3, 170.67),
     (156.9, 171.99), (157.8, 172.71), (159.4, 174.47), (163, 176.51), (166, 180.43), (169, 182.43), (172.5, 186.51),
     (174, 188.65), (180, 193.87), (185, 199.90), (188, 203.30), (193, 208.47), (197, 211.99), (201, 219.23),
     (206, 221.87), (206.4, 224.35), (207.8, 225.63), (209.1, 226.75), (212, 228.5), (216, 233.70), (221, 238.75),
     (225, 243.1), (225.2, 244.99), (225.9, 246.15), (226.8, 247.27), (231, 248.66), (235, 253.75), (238.3, 257.43),
     (241, 259.70), (245, 264.71), (247.6, 267.91), (248.4, 268.95), (249.2, 270.19), (251, 271.55), (253, 273.59),
     (254.5, 274.99), (257.6, 278.3)]


def _interp(x, pts):
    if x <= pts[0][0]:
        return pts[0][1] + (x - pts[0][0])
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return pts[-1][1] + (x - pts[-1][0])


def fwd(t_old):
    return _interp(t_old, A)


def back(t_new):
    return _interp(t_new, [(b, a) for a, b in A])


# efeitos sonoros: registra os eventos já no tempo novo
_cue = engine.cue
engine.cue = lambda t0, kind: _cue(fwd(t0), kind)


def _wrap(fn):
    return lambda c, t: fn(c, back(t))


SCENES = [(fwd(s), (fwd(e) if e < 900 else 999.0), _wrap(fn)) for s, e, fn in old.SCENES]

# só toques pontuais, sem ruído: Erro nº 1, 41% do salário, "o dinheiro continua seu"
SFX = [(28.45, "tum"), (140.16, "tum"), (235.42, "soft_ding")]
# (nenhum som automático)
SFX_SKIP = ("anim:pop", "anim:drop", "anim:stamp", "anim:fade", "anim:up", "anim:left", "anim:right", "arrow", "appear", "key")
