"""Foto de perfil do Faz a Conta com O Consultor no estilo ilustrado (desde nov 2026). Rodar da raiz:
    python marca/avatar_ilustrado.py
Gera marca/avatar_ilustrado_A.png (fundo creme, círculo dourado) e _B.png (fundo azul-marinho), 800x800.
O essencial fica dentro do círculo central (TikTok, YouTube e Instagram cortam a foto em círculo)."""
import sys, os
sys.path.insert(0, os.getcwd())
os.environ.pop("PC_VERTICAL", None)
from engine import *
from ilustrado import *
import ilustrado

OUT = os.path.dirname(os.path.abspath(__file__))
S = 1600


def avatar(variant, s_=4.6, cabeca_y=600):
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, S, S); c = cairo.Context(surf)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    fundo, disco, borda, simb = ((PAPER, GOLD, NAVY, NAVY) if variant == "A" else (NAVY, PAPER, GOLD, GOLD))
    rgb(c, fundo); c.paint()
    cx, cy, r = S / 2, S * 0.47, S * 0.37
    c.new_sub_path(); c.arc(cx, cy, r, 0, 6.283); rgb(c, disco); c.fill()
    c.new_sub_path(); c.arc(cx, cy, r, 0, 6.283); rgb(c, borda); c.set_line_width(16); c.stroke()
    for (x, y, txt) in ((250, 330, "+"), (1330, 360, "="), (190, 1060, "%"), (1420, 1060, "R$")):
        numero_i(c, txt, x, y, 90, simb, contorno=fundo)
    luz("dia")
    c.save(); c.new_sub_path(); c.arc(cx, cy, r, 0, 6.283); c.rectangle(0, cy, S, S); c.clip()
    consultor_i(c, 1.0, cx, cabeca_y + 403 * s_, s_, poses=((0, "stand"),), exprs=((0, "grin"),), look=0.0)
    c.restore()
    big = f"{OUT}/_tmp.png"; surf.write_to_png(big)
    os.system(f'ffmpeg -loglevel error -y -i "{big}" -vf scale=800:800:flags=lanczos "{OUT}/avatar_ilustrado_{variant}.png" && rm "{big}"')


if __name__ == "__main__":
    avatar("A"); avatar("B")
    print("ok")
