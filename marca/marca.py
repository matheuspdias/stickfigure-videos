"""Foto de perfil (800x800) e banner (2560x1440) do canal Faz a Conta. Rodar da raiz: python marca/marca.py"""
import sys, os
sys.path.insert(0, os.getcwd())
from engine import *

OUT = os.path.dirname(os.path.abspath(__file__))


def surface(w, h):
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, w, h); c = cairo.Context(s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    return s, c


def save(s, name, w, h):
    big = f"{OUT}/{name}_big.png"
    s.write_to_png(big)
    os.system(f'ffmpeg -loglevel error -y -i "{big}" -vf scale={w}:{h}:flags=lanczos "{OUT}/{name}.png" && rm "{big}"')


def avatar(variant):
    S = 1600
    s, c = surface(S, S)
    if variant == "A":
        rgb(c, PAPER); c.paint()
        circle(c, S / 2, S * 0.47, S * 0.36, GOLD, 0)
        circle(c, S / 2, S * 0.47, S * 0.36, None, 14, NAVY)
    else:
        rgb(c, NAVY); c.paint()
        circle(c, S / 2, S * 0.47, S * 0.37, PAPER, 0)
        circle(c, S / 2, S * 0.47, S * 0.37, None, 18, GOLD)
    for i, (x, y, r, sym) in enumerate(((0.16, 0.22, 70, "+"), (0.84, 0.24, 70, "="), (0.13, 0.70, 60, "%"), (0.87, 0.68, 60, "R$"))):
        text(c, sym, S * x, S * y, r * 1.6, MARKER, NAVY if variant == "A" else GOLD)
    hero(c, 1.3, S * 0.5, S * 1.45, 4.1, [(0, "stand")], [(0, "confident")], look=0.0)
    save(s, f"avatar_fazaconta_{variant}", 800, 800)


def banner():
    Wb, Hb = 2560, 1440
    s, c = surface(Wb, Hb)
    rgb(c, PAPER); c.paint()
    # faixa central (área segura 1546x423 no centro)
    c.rectangle(0, 470, Wb, 500); rgb(c, NAVY); c.fill()
    line(c, 0, 470, Wb, 470, 8, GOLD); line(c, 0, 970, Wb, 970, 8, GOLD)
    # elementos de conta espalhados nas bordas (aparecem só na TV)
    rnd = random.Random(4)
    for _ in range(26):
        x, y = rnd.uniform(60, Wb - 60), rnd.choice([rnd.uniform(80, 400), rnd.uniform(1040, 1380)])
        text(c, rnd.choice(["+", "-", "=", "%", "R$", "÷", "x"]), x, y, rnd.uniform(60, 110), MARKER, (0.80, 0.78, 0.72))
    # título e slogan
    text(c, "FAZ A CONTA", 1330, 655, 170, MARKER, PAPER, outline=INK, ow=14)
    text(c, "a conta de verdade das decisões da vida", 1330, 830, 64, HAND, GOLD)
    # Consultor com a calculadora, à esquerda dentro da área segura
    c.save(); c.translate(0, 0)
    hero(c, 1.2, 600, 905, 0.76, [(0, "present")], [(0, "confident")], prop=("l", prop_calculator), look=1)
    c.restore()
    # moeda e gráfico à direita
    c.save(); c.translate(1985, 640); c.scale(1.2, 1.2); coin(c); c.restore()
    save(s, "banner_fazaconta", Wb, Hb)


avatar("A"); avatar("B"); banner()
print("ok")
