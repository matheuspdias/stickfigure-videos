"""
ESTILO ILUSTRADO do Faz a Conta (ilustração vetorial chapada, sem contorno), portado do Ponto Cego.
Funciona em 16:9 (YouTube) e no vertical (VERTICAL = True, TikTok).

    from engine import *
    from ilustrado import *
    STYLE = "ilustrado"

Cada cena escolhe um CENÁRIO de vida real (cozinha, padaria, mercado, escritório, sala, rua, agência)
ou um FUNDO de marca para cenas de número/gráfico, e põe O Consultor (consultor_i) reagindo.
Luzes: dia, tarde, crepusculo, noite, nublado, sepia, vela, interior.
"""
import cairo, math, random
from engine import *
import engine

# fontes e cores do Faz a Conta
SERIF = MARKER      # títulos e números (Permanent Marker)
TYPE = HAND         # textos de apoio (Patrick Hand)
AMBER = GOLD

# ================================================================ cores e luz
def mix(a, b, k):
    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k)


def mul(a, b):
    return (a[0] * b[0], a[1] * b[1], a[2] * b[2])


def dk(col, k=0.2):
    return mix(col, (0, 0, 0), k)


def lt(col, k=0.2):
    return mix(col, (1, 1, 1), k)


# ceu=(topo, horizonte)  tinta=cor da luz ambiente  tk=força da tinta  neb=névoa de distância  nebk=força
# astro=("sol"|"lua", x, y, cor)  dir = de onde vem a luz (-1 esquerda, 1 direita)  noite = janelas acesas
LUZES = {
    "dia":        dict(ceu=((0.52, 0.71, 0.84), (0.86, 0.89, 0.84)), tinta=(1, 1, 1), tk=0.0,
                       neb=(0.80, 0.86, 0.88), nebk=0.75, astro=("sol", 1500, 210, (1.0, 0.97, 0.86)),
                       nuvem=(0.97, 0.96, 0.92), dir=-1, noite=False, estrelas=False, fora=(0.70, 0.82, 0.90)),
    "tarde":      dict(ceu=((0.86, 0.62, 0.42), (0.99, 0.86, 0.60)), tinta=(1.0, 0.86, 0.68), tk=0.85,
                       neb=(0.98, 0.84, 0.62), nebk=0.70, astro=("sol", 1480, 560, (1.0, 0.93, 0.70)),
                       nuvem=(0.99, 0.88, 0.72), dir=1, noite=False, estrelas=False, fora=(0.98, 0.80, 0.55)),
    "crepusculo": dict(ceu=((0.30, 0.25, 0.45), (0.95, 0.62, 0.46)), tinta=(0.78, 0.62, 0.72), tk=0.9,
                       neb=(0.78, 0.55, 0.58), nebk=0.70, astro=("sol", 1380, 640, (1.0, 0.80, 0.55)),
                       nuvem=(0.80, 0.55, 0.62), dir=1, noite=True, estrelas=False, fora=(0.80, 0.55, 0.55)),
    "noite":      dict(ceu=((0.05, 0.08, 0.17), (0.17, 0.22, 0.35)), tinta=(0.42, 0.50, 0.74), tk=1.0,
                       neb=(0.20, 0.26, 0.40), nebk=0.70, astro=("lua", 1500, 200, (0.95, 0.94, 0.86)),
                       nuvem=(0.22, 0.27, 0.40), dir=1, noite=True, estrelas=True, fora=(0.12, 0.17, 0.30)),
    "nublado":    dict(ceu=((0.58, 0.62, 0.66), (0.80, 0.80, 0.76)), tinta=(0.86, 0.88, 0.90), tk=1.0,
                       neb=(0.74, 0.76, 0.76), nebk=0.75, astro=None,
                       nuvem=(0.70, 0.72, 0.74), dir=-1, noite=False, estrelas=False, fora=(0.72, 0.75, 0.78)),
    "sepia":      dict(ceu=((0.85, 0.77, 0.58), (0.95, 0.89, 0.72)), tinta=(1.0, 0.90, 0.72), tk=0.8,
                       neb=(0.93, 0.86, 0.68), nebk=0.75, astro=None,
                       nuvem=(0.96, 0.90, 0.76), dir=-1, noite=False, estrelas=False, fora=(0.95, 0.88, 0.70)),
    "vela":       dict(ceu=((0.10, 0.09, 0.10), (0.16, 0.13, 0.12)), tinta=(0.80, 0.58, 0.40), tk=1.0,
                       neb=(0.20, 0.14, 0.10), nebk=0.6, astro=None,
                       nuvem=(0.2, 0.2, 0.2), dir=1, noite=True, estrelas=False, fora=(0.10, 0.14, 0.26)),
    "interior":   dict(ceu=((0.55, 0.60, 0.66), (0.70, 0.72, 0.74)), tinta=(0.86, 0.88, 0.94), tk=1.0,
                       neb=(0.70, 0.72, 0.76), nebk=0.6, astro=None,
                       nuvem=(0.9, 0.9, 0.9), dir=1, noite=False, estrelas=False, fora=(0.82, 0.88, 0.94)),
    # terror / mistério pesado
    "sombrio":    dict(ceu=((0.04, 0.06, 0.07), (0.15, 0.19, 0.19)), tinta=(0.38, 0.46, 0.48), tk=1.0,
                       neb=(0.26, 0.32, 0.32), nebk=0.85, astro=("lua", 1480, 210, (0.80, 0.84, 0.78)),
                       nuvem=(0.12, 0.15, 0.16), dir=1, noite=True, estrelas=False, fora=(0.08, 0.10, 0.11)),
    "tempestade": dict(ceu=((0.08, 0.08, 0.12), (0.24, 0.23, 0.29)), tinta=(0.44, 0.45, 0.55), tk=1.0,
                       neb=(0.28, 0.28, 0.34), nebk=0.8, astro=None,
                       nuvem=(0.16, 0.16, 0.21), dir=1, noite=True, estrelas=False, fora=(0.10, 0.10, 0.14)),
    "lua_sangue": dict(ceu=((0.07, 0.02, 0.03), (0.30, 0.09, 0.07)), tinta=(0.62, 0.34, 0.32), tk=1.0,
                       neb=(0.32, 0.10, 0.08), nebk=0.8, astro=("lua", 1460, 230, (0.86, 0.32, 0.22)),
                       nuvem=(0.18, 0.06, 0.06), dir=1, noite=True, estrelas=True, fora=(0.12, 0.04, 0.04)),
}
_L = LUZES["dia"]


def luz(nome="dia"):
    """define a luz da cena (chame no começo de cada cena; os cenários prontos já chamam)"""
    global _L
    if getattr(engine, "TOM", "normal") == "sombrio":
        nome = {"dia": "nublado", "tarde": "crepusculo", "sepia": "nublado"}.get(nome, nome)
    if nome not in LUZES:
        raise ValueError(f"luz desconhecida: {nome} (opções: {', '.join(LUZES)})")
    _L = LUZES[nome]
    return _L


def P(col, depth=0.0):
    """cor iluminada pela luz da cena. depth 0 = primeiro plano, 1 = horizonte (some na névoa)"""
    tin = mix((1, 1, 1), _L["tinta"], _L["tk"])
    out = mul(col, tin)
    if depth > 0:
        out = mix(out, _L["neb"], min(1.0, depth) * _L["nebk"])
    return out


def pinta(c, col, a=1.0, depth=0.0):
    rgb(c, P(col, depth), a); c.fill()


def pg(c, pts):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()


def rr(c, x, y, w, h, r):
    rrect(c, x, y, w, h, r)


def lgrad(c, x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for k, col, a in stops:
        g.add_color_stop_rgba(k, col[0], col[1], col[2], a)
    c.set_source(g)


def rglow(c, x, y, r, col, a=0.4):
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, col[0], col[1], col[2], a)
    g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
    c.set_source(g); c.arc(x, y, r, 0, 2 * math.pi); c.fill()


# paleta base (antes da luz)
PEDRA = (0.72, 0.68, 0.60)
REBOCO = (0.86, 0.76, 0.60)
TELHA = (0.70, 0.38, 0.26)
MADEIRA = (0.45, 0.31, 0.20)
MADEIRA_ESC = (0.30, 0.20, 0.13)
GRAMA = (0.52, 0.62, 0.36)
TERRA = (0.62, 0.50, 0.36)
AREIA = (0.90, 0.76, 0.52)
NEVE_C = (0.92, 0.94, 0.97)
AGUA = (0.30, 0.48, 0.60)
FOLHA = (0.30, 0.48, 0.30)
JANELA_ACESA = (1.0, 0.78, 0.42)
OURO = (0.88, 0.70, 0.30)
PELES = dict(clara=(0.95, 0.80, 0.68), media=(0.85, 0.65, 0.50), morena=(0.66, 0.47, 0.34), escura=(0.44, 0.30, 0.22))
CABELOS = dict(preto=(0.14, 0.11, 0.10), castanho=(0.33, 0.22, 0.14), loiro=(0.80, 0.64, 0.38),
               ruivo=(0.66, 0.32, 0.16), grisalho=(0.62, 0.60, 0.58), branco=(0.90, 0.89, 0.86))


# ================================================================ céu e astros
def nuvem(c, x, y, w, col, seed=1, depth=0.3):
    """nuvem chapada de base reta"""
    rnd = random.Random(seed)
    c.save()
    c.rectangle(x - w, y - w, w * 2, w)  # só acima da base
    c.clip()
    n = 5
    for i in range(n):
        cx = x - w * 0.42 + i * w * 0.84 / (n - 1)
        r = w * (0.16 + 0.12 * math.sin(i / (n - 1) * math.pi)) * rnd.uniform(0.85, 1.15)
        c.new_sub_path(); c.arc(cx, y - r * 0.35, r, 0, 2 * math.pi)
    rgb(c, P(col, depth)); c.fill()
    c.restore()
    rr(c, x - w * 0.5, y - 10, w, 10, 5)
    rgb(c, dk(P(col, depth), 0.07)); c.fill()


def ceu(c, t, nuvens=True, astro=True, passaros=False, seed=1, horizonte=760):
    L = _L
    lgrad(c, 0, 0, 0, horizonte, [(0, L["ceu"][0], 1), (1, L["ceu"][1], 1)])
    c.paint()
    if L["estrelas"]:
        rnd = random.Random(seed * 7)
        for i in range(140):
            x, y, r = rnd.uniform(0, W), rnd.uniform(0, horizonte * 0.75), rnd.uniform(0.8, 2.4)
            a = 0.35 + 0.5 * (0.5 + 0.5 * math.sin(t * rnd.uniform(0.6, 2.0) + i))
            rgb(c, (0.95, 0.93, 0.85), a * (1 - y / horizonte)); c.new_sub_path(); c.arc(x, y, r, 0, 6.283); c.fill()
    if astro and L["astro"]:
        kind, ax, ay, col = L["astro"]
        if isinstance(astro, tuple):
            ax, ay = astro
        if kind == "sol":
            c.save()
            for i in range(9):
                a = i * math.pi * 2 / 9 + t * 0.02
                c.move_to(ax, ay); c.line_to(ax + math.cos(a) * 1600, ay + math.sin(a) * 1600)
                c.line_to(ax + math.cos(a + 0.09) * 1600, ay + math.sin(a + 0.09) * 1600); c.close_path()
            g = cairo.RadialGradient(ax, ay, 40, ax, ay, 1200)
            g.add_color_stop_rgba(0, col[0], col[1], col[2], 0.16)
            g.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
            c.set_source(g); c.fill(); c.restore()
            rglow(c, ax, ay, 520, col, 0.45)
            rglow(c, ax, ay, 160, (1, 1, 0.95), 0.5)
            c.new_sub_path(); c.arc(ax, ay, 56, 0, 6.283); rgb(c, lt(col, 0.4)); c.fill()
        else:
            rglow(c, ax, ay, 380, mix(col, (0.75, 0.80, 0.95), 0.5), 0.22)
            c.new_sub_path(); c.arc(ax, ay, 58, 0, 6.283); rgb(c, col); c.fill()
            for dx, dy, r in ((-18, -10, 11), (14, 16, 8), (20, -20, 6), (-6, 24, 5)):
                c.new_sub_path(); c.arc(ax + dx, ay + dy, r, 0, 6.283); rgb(c, dk(col, 0.08)); c.fill()
    if nuvens:
        rnd = random.Random(seed)
        for i in range(nuvens if isinstance(nuvens, int) and nuvens is not True else 4):
            w = rnd.uniform(260, 460)
            y = rnd.uniform(110, horizonte * 0.5)
            x = (rnd.uniform(0, W) + t * rnd.uniform(4, 10)) % (W + 600) - 300
            nuvem(c, x, y, w, L["nuvem"], seed=seed * 13 + i, depth=0.25)
    if passaros:
        rnd = random.Random(seed + 99)
        for i in range(passaros if isinstance(passaros, int) and passaros is not True else 5):
            x = (rnd.uniform(0, W) + t * rnd.uniform(30, 60)) % (W + 200) - 100
            y = rnd.uniform(120, 360) + math.sin(t * 0.8 + i) * 12
            f = math.sin(t * 9 + i * 1.7) * 6
            c.move_to(x - 12, y - 4 - f); c.line_to(x, y); c.line_to(x + 12, y - 4 - f)
            rgb(c, dk(_L["neb"], 0.55), 0.8); c.set_line_width(2.6); c.stroke()


# ================================================================ terreno
def montanhas(c, y=640, h=300, seed=1, depth=0.75, col=(0.42, 0.46, 0.52), neve=False, picos=7, x0=-100, x1=None):
    """cordilheira chapada com face iluminada e face na sombra"""
    x1 = x1 if x1 is not None else W + 100
    rnd = random.Random(seed)
    xs = [x0 + (x1 - x0) * i / picos + rnd.uniform(-40, 40) for i in range(picos + 1)]
    base = P(col, depth)
    for i, px in enumerate(xs):
        ph = h * rnd.uniform(0.55, 1.0)
        hw = (x1 - x0) / picos * rnd.uniform(0.75, 1.15)
        top = (px, y - ph)
        pg(c, [(px - hw, y + 4), top, (px + hw, y + 4)])
        rgb(c, base); c.fill()
        # face na sombra (do lado oposto à luz)
        side = -_L["dir"]
        pg(c, [top, (px + side * hw, y + 4), (px + side * hw * 0.15, y + 4)])
        rgb(c, dk(base, 0.12)); c.fill()
        if neve:
            k = 0.28
            sn = [(px - hw * k, y - ph * (1 - k)), top, (px + hw * k, y - ph * (1 - k)),
                  (px + hw * k * 0.4, y - ph * (1 - k) + 18), (px, y - ph * (1 - k) + 4), (px - hw * k * 0.5, y - ph * (1 - k) + 22)]
            pg(c, sn); rgb(c, P(NEVE_C, depth * 0.6)); c.fill()
    c.rectangle(x0, y, x1 - x0, 6); rgb(c, base); c.fill()


def colinas(c, y=720, amp=40, seed=1, col=GRAMA, depth=0.4, ate=H):
    rnd = random.Random(seed)
    ks = [(rnd.uniform(0.002, 0.006), rnd.uniform(0, 6.28), rnd.uniform(0.4, 1.0)) for _ in range(3)]
    c.move_to(-20, ate)
    for x in range(-20, W + 41, 20):
        yy = y - amp * sum(a * math.sin(x * f + p) for f, p, a in ks) / 2
        c.line_to(x, yy)
    c.line_to(W + 40, ate); c.close_path()
    rgb(c, P(col, depth)); c.fill()


def chao(c, t=0, y=860, tipo="grama", seed=1, ate=H):
    """faixa de chão do primeiro plano: grama, terra, pedra (calçamento), areia, neve, madeira (convés/assoalho)"""
    cols = dict(grama=GRAMA, terra=TERRA, pedra=(0.60, 0.57, 0.52), areia=AREIA, neve=NEVE_C, madeira=MADEIRA)
    base = cols.get(tipo, TERRA)
    lgrad(c, 0, y, 0, ate, [(0, P(lt(base, 0.06)), 1), (1, P(dk(base, 0.18)), 1)])
    c.rectangle(-20, y, W + 40, ate - y); c.fill()
    rnd = random.Random(seed)
    if tipo == "pedra":
        rows = 7
        for r in range(rows):
            k = r / rows
            yy = y + (ate - y) * (k ** 1.4)
            hh = (ate - y) * (((r + 1) / rows) ** 1.4 - k ** 1.4)
            sw = 60 + 120 * k
            off = (r % 2) * sw / 2
            x = -off
            while x < W + 20:
                rr(c, x + 3, yy + 2, sw - 6, hh - 4, 6 + 6 * k)
                rgb(c, P(dk(base, rnd.uniform(0.0, 0.12)))); c.fill()
                x += sw
    elif tipo == "madeira":
        for i in range(-12, 13):
            x0 = W / 2 + i * 70
            c.move_to(W / 2 + i * 36, y); c.line_to(x0 + i * 60, ate)
            rgb(c, P(dk(base, 0.25)), 0.6); c.set_line_width(3); c.stroke()
    else:
        for i in range(70):
            x = rnd.uniform(0, W)
            k = rnd.uniform(0, 1) ** 1.6
            yy = y + 8 + (ate - y - 8) * k
            sz = 6 + 22 * k
            if tipo == "grama":
                sway = math.sin(t * 1.5 + x * 0.01) * 3
                for j in (-1, 0, 1):
                    c.move_to(x + j * sz * 0.4, yy); c.line_to(x + j * sz * 0.7 + sway, yy - sz * 1.4); c.line_to(x + j * sz * 0.4 + 4, yy)
                rgb(c, P(dk(base, 0.15))); c.fill()
            elif tipo == "terra":
                ellipse(c, x, yy, sz * 0.8, sz * 0.35); rgb(c, P(dk(base, 0.12))); c.fill()
            elif tipo == "areia":
                c.move_to(x - sz * 3, yy); c.curve_to(x - sz, yy - sz * 0.4, x + sz, yy - sz * 0.4, x + sz * 3, yy)
                rgb(c, P(dk(base, 0.10)), 0.7); c.set_line_width(2.5); c.stroke()
            elif tipo == "neve":
                ellipse(c, x, yy, sz * 2, sz * 0.3); rgb(c, P(dk(base, 0.06))); c.fill()
    # borda
    c.rectangle(-20, y, W + 40, 5); rgb(c, P(dk(base, 0.22)), 0.5); c.fill()


# ================================================================ vegetação
def arvore(c, t, x, y, h=300, tipo="redonda", col=FOLHA, seed=1, depth=0.0, seca=False):
    """árvore chapada: redonda, pinheiro, palmeira, cipreste"""
    rnd = random.Random(seed)
    sway = math.sin(t * 0.9 + seed) * 0.012
    c.save(); c.translate(x, y); c.rotate(sway)
    tr = P(MADEIRA_ESC, depth)
    leaf = P(mix(col, (rnd.uniform(0.2, 0.4), rnd.uniform(0.4, 0.55), 0.25), 0.25), depth)
    if tipo == "palmeira":
        c.move_to(-12, 0); c.curve_to(-12, -h * 0.5, 6, -h * 0.8, 2, -h); c.line_to(18, -h); c.curve_to(24, -h * 0.8, 10, -h * 0.5, 14, 0)
        c.close_path(); rgb(c, P((0.50, 0.38, 0.24), depth)); c.fill()
        for i in range(9):
            a = -math.pi / 2 + (i - 4) * 0.42 + math.sin(t + i) * 0.04
            L_ = h * 0.42
            ex, ey = 10 + math.cos(a) * L_, -h + math.sin(a) * L_ + L_ * 0.35
            c.move_to(10, -h); c.curve_to(10 + math.cos(a) * L_ * 0.5, -h + math.sin(a) * L_ * 0.6 - 20, ex, ey - 10, ex, ey)
            c.curve_to(ex - 10, ey - 40, 10 + math.cos(a) * L_ * 0.4, -h + math.sin(a) * L_ * 0.4 - 46, 10, -h)
            rgb(c, leaf if i % 2 else dk(leaf, 0.12)); c.fill()
        c.restore(); return
    c.rectangle(-h * 0.035, -h * 0.45, h * 0.07, h * 0.45); rgb(c, tr); c.fill()
    if seca:
        for i in range(5):
            a = -math.pi / 2 + (i - 2) * 0.45
            c.move_to(0, -h * 0.4); c.line_to(math.cos(a) * h * 0.4, -h * 0.4 + math.sin(a) * h * 0.45)
            rgb(c, tr); c.set_line_width(h * 0.02); c.stroke()
        c.restore(); return
    if tipo == "pinheiro":
        for i in range(4):
            yy = -h * 0.25 - i * h * 0.2
            ww = h * (0.32 - i * 0.06)
            pg(c, [(-ww, yy), (0, yy - h * 0.34), (ww, yy)]); rgb(c, leaf); c.fill()
            pg(c, [(0, yy - h * 0.34), (ww * -_L["dir"], yy), (0, yy)]); rgb(c, dk(leaf, 0.14)); c.fill()
    elif tipo == "cipreste":
        ellipse(c, 0, -h * 0.55, h * 0.12, h * 0.48); rgb(c, leaf); c.fill()
    else:
        blobs = [(0, -h * 0.72, h * 0.30), (-h * 0.2, -h * 0.55, h * 0.22), (h * 0.2, -h * 0.56, h * 0.23), (0, -h * 0.5, h * 0.24)]
        for bx, by, br in blobs:
            c.new_sub_path(); c.arc(bx, by, br, 0, 6.283)
        rgb(c, leaf); c.fill()
        side = -_L["dir"]
        c.new_sub_path(); c.arc(side * h * 0.16, -h * 0.5, h * 0.2, 0, 6.283); rgb(c, dk(leaf, 0.12)); c.fill()
        c.new_sub_path(); c.arc(-side * h * 0.08, -h * 0.78, h * 0.12, 0, 6.283); rgb(c, lt(leaf, 0.10)); c.fill()
    c.restore()


def floresta(c, t, y=760, n=14, h=(220, 360), tipos=("redonda", "pinheiro"), col=FOLHA, seed=3, depth=0.4):
    rnd = random.Random(seed)
    items = []
    for i in range(n):
        x = -80 + (W + 160) * i / (n - 1) + rnd.uniform(-50, 50)
        items.append((x, rnd.uniform(*h), rnd.choice(tipos), seed * 31 + i))
    for x, hh, tp, sd in items:
        arvore(c, t, x, y, hh, tp, col, sd, depth)


# ================================================================ construções
def janela_i(c, x, y, w, h, estilo="reta", acesa=None, persiana=None, depth=0.0):
    """janela; acesa=None segue a luz da cena (acesa à noite)"""
    if acesa is None:
        acesa = _L["noite"]
    moldura = P(dk(REBOCO, 0.35), depth)
    vid = JANELA_ACESA if acesa else mix(_L["fora"], (0.2, 0.24, 0.3), 0.55)

    def forma(px, py, pw, ph):
        if estilo == "arco":
            c.move_to(px, py + ph); c.line_to(px, py + pw / 2); c.arc(px + pw / 2, py + pw / 2, pw / 2, math.pi, 2 * math.pi)
            c.line_to(px + pw, py + ph); c.close_path()
        elif estilo == "gotica":
            c.move_to(px, py + ph); c.line_to(px, py + pw * 0.6)
            c.curve_to(px, py + pw * 0.2, px + pw * 0.3, py, px + pw / 2, py - pw * 0.15)
            c.curve_to(px + pw * 0.7, py, px + pw, py + pw * 0.2, px + pw, py + pw * 0.6)
            c.line_to(px + pw, py + ph); c.close_path()
        else:
            c.rectangle(px, py, pw, ph)
    forma(x - 6, y - 6, w + 12, h + 12); rgb(c, moldura); c.fill()
    forma(x, y, w, h)
    rgb(c, P(vid, depth) if not acesa else vid); c.fill()
    if acesa:
        rglow(c, x + w / 2, y + h / 2, max(w, h) * 1.1, JANELA_ACESA, 0.22)
    c.move_to(x + w / 2, y + 4); c.line_to(x + w / 2, y + h); rgb(c, moldura); c.set_line_width(4); c.stroke()
    c.move_to(x, y + h * 0.5); c.line_to(x + w, y + h * 0.5); c.stroke()
    if persiana is not None:
        for sx in (-1, 1):
            px = x - w * 0.5 - 6 if sx < 0 else x + w + 6
            c.rectangle(px, y - 4, w * 0.5, h + 8); rgb(c, P(persiana, depth)); c.fill()
            for k in range(1, 6):
                c.move_to(px + 3, y + (h + 8) * k / 6); c.line_to(px + w * 0.5 - 3, y + (h + 8) * k / 6)
                rgb(c, P(dk(persiana, 0.2), depth)); c.set_line_width(2); c.stroke()
    c.rectangle(x - 10, y + h + 4, w + 20, 8); rgb(c, moldura); c.fill()


def predio(c, x, y, w, h, estilo="medieval", col=None, seed=1, depth=0.0, telhado=True, porta=True):
    """fachada: medieval (enxaimel + telhado íngreme), pedra, colonial (pastel, sacadas), moderno"""
    rnd = random.Random(seed)
    if col is None:
        col = {"medieval": rnd.choice([(0.90, 0.84, 0.70), (0.86, 0.78, 0.62), (0.80, 0.74, 0.64)]),
               "pedra": rnd.choice([(0.70, 0.66, 0.58), (0.64, 0.60, 0.54)]),
               "colonial": rnd.choice([(0.92, 0.80, 0.62), (0.86, 0.66, 0.58), (0.70, 0.78, 0.74), (0.90, 0.86, 0.72), (0.66, 0.72, 0.80)]),
               "moderno": rnd.choice([(0.62, 0.62, 0.64), (0.70, 0.66, 0.60)])}[estilo]
    base = P(col, depth)
    top = y - h
    # telhado
    if telhado and estilo == "medieval":
        rh = w * rnd.uniform(0.45, 0.65)
        pg(c, [(x - 14, top + 6), (x + w / 2, top - rh), (x + w + 14, top + 6)])
        rgb(c, P(TELHA, depth)); c.fill()
        for k in range(1, 6):
            yy = top - rh + rh * k / 6 + 6
            hw = (w / 2 + 14) * k / 6
            c.move_to(x + w / 2 - hw, yy); c.line_to(x + w / 2 + hw, yy)
            rgb(c, P(dk(TELHA, 0.18), depth)); c.set_line_width(3); c.stroke()
    elif telhado and estilo in ("colonial", "pedra"):
        c.rectangle(x - 10, top - 26, w + 20, 26); rgb(c, P(TELHA, depth)); c.fill()
        for k in range(0, int(w / 18) + 2):
            c.move_to(x - 10 + k * 18, top - 26); c.line_to(x - 10 + k * 18, top)
            rgb(c, P(dk(TELHA, 0.2), depth)); c.set_line_width(2); c.stroke()
    c.rectangle(x, top, w, h); rgb(c, base); c.fill()
    if estilo == "pedra":
        rows = int(h / 34)
        for r in range(rows):
            yy = top + r * 34
            off = (r % 2) * 30
            xx = x - off
            while xx < x + w:
                c.rectangle(max(x, xx) + 2, yy + 2, min(60, x + w - xx) - 4, 30)
                rgb(c, dk(base, rnd.uniform(0.0, 0.10))); c.fill()
                xx += 60
    if estilo == "colonial":
        c.rectangle(x - 6, top, w + 12, 16); rgb(c, lt(base, 0.25)); c.fill()  # cornija
        c.rectangle(x - 4, y - 70, w + 8, 70); rgb(c, dk(base, 0.10)); c.fill()  # barrado
    floors = max(1, int((h - 60) / 150))
    fh = (h - 30) / floors
    cols_ = max(1, int(w / 110))
    for f in range(floors):
        fy = top + 30 + f * fh
        if estilo == "medieval" and f < floors:
            c.rectangle(x, fy - 8, w, 9); rgb(c, P(MADEIRA_ESC, depth)); c.fill()
            if f > 0 or rnd.random() < 0.5:
                for k in range(cols_ + 1):
                    xx = x + w * k / cols_
                    c.rectangle(xx - 4, fy - 8, 8, fh); rgb(c, P(MADEIRA_ESC, depth)); c.fill()
                    if k < cols_ and rnd.random() < 0.5:
                        c.move_to(xx + 4, fy + fh - 8); c.line_to(xx + w / cols_ * 0.28, fy)
                        rgb(c, P(MADEIRA_ESC, depth)); c.set_line_width(7); c.stroke()
        is_ground = f == floors - 1
        for k in range(cols_):
            cx = x + w * (k + 0.5) / cols_
            if is_ground and porta and k == cols_ // 2:
                continue
            ww, wh = min(46, w / cols_ * 0.42), fh * 0.45
            est = {"colonial": "arco", "pedra": "reta", "medieval": "reta", "moderno": "reta"}[estilo]
            pers = (0.24, 0.38, 0.30) if estilo == "colonial" else (MADEIRA if estilo == "medieval" and rnd.random() < 0.4 else None)
            acesa = None if rnd.random() < 0.6 else False
            janela_i(c, cx - ww / 2, fy + fh * 0.22, ww, wh, est, acesa, pers, depth)
            if estilo == "colonial" and not is_ground:
                c.rectangle(cx - ww, fy + fh * 0.22 + wh + 6, ww * 2, 6); rgb(c, P((0.18, 0.18, 0.2), depth)); c.fill()
                for b in range(7):
                    c.rectangle(cx - ww + b * ww * 2 / 6 - 1, fy + fh * 0.22 + wh + 12, 3, 26); c.fill()
    if porta:
        pw, ph = min(70, w * 0.3), min(130, fh * 0.8)
        px = x + w * ((cols_ // 2) + 0.5) / cols_ - pw / 2
        c.move_to(px, y); c.line_to(px, y - ph + pw / 2); c.arc(px + pw / 2, y - ph + pw / 2, pw / 2, math.pi, 2 * math.pi)
        c.line_to(px + pw, y); c.close_path()
        rgb(c, P(MADEIRA_ESC, depth)); c.fill()
        c.move_to(px + pw / 2, y - ph); c.line_to(px + pw / 2, y); rgb(c, P(dk(MADEIRA_ESC, 0.3), depth)); c.set_line_width(3); c.stroke()
    # sombra lateral (volume)
    side = -_L["dir"]
    sx = x + w - 22 if side > 0 else x
    c.rectangle(sx, top, 22, h); rgb(c, (0, 0, 0), 0.10); c.fill()


def casario(c, t, y=820, estilo="medieval", seed=3, depth=0.0, h=(320, 520), w=(220, 330), escala=1.0, x0=-60, x1=None):
    x1 = x1 if x1 is not None else W + 60
    rnd = random.Random(seed)
    x = x0
    i = 0
    while x < x1:
        ww = rnd.uniform(*w) * escala
        hh = rnd.uniform(*h) * escala
        predio(c, x, y, ww, hh, estilo, seed=seed * 17 + i, depth=depth)
        x += ww + rnd.choice([0, 0, 10]) * escala
        i += 1


def igreja(c, x, y, s=1.0, depth=0.0, col=(0.62, 0.62, 0.66), porta_acesa=None):
    """fachada gótica com torre central (origem = centro da base)"""
    c.save(); c.translate(x, y); c.scale(s, s)
    base = P(col, depth)
    pg(c, [(-260, 0), (-260, -420), (0, -620), (260, -420), (260, 0)]); rgb(c, base); c.fill()
    pg(c, [(0, -620), (260, -420), (260, 0), (0, 0)]); rgb(c, dk(base, 0.08)); c.fill()
    c.rectangle(-70, -760, 140, 400); rgb(c, lt(base, 0.04)); c.fill()
    pg(c, [(-80, -760), (0, -980), (80, -760)]); rgb(c, dk(base, 0.15)); c.fill()
    c.rectangle(-3, -1040, 6, 70); rgb(c, P(OURO, depth)); c.fill(); c.rectangle(-22, -1020, 44, 6); c.fill()
    acesa = _L["noite"] if porta_acesa is None else porta_acesa
    janela_i(c, -24, -720, 48, 110, "gotica", acesa, None, depth)
    c.new_sub_path(); c.arc(0, -470, 56, 0, 6.283); rgb(c, dk(base, 0.25)); c.fill()
    c.new_sub_path(); c.arc(0, -470, 44, 0, 6.283); rgb(c, JANELA_ACESA if acesa else P(_L["fora"], depth)); c.fill()
    for i in range(8):
        a = i * math.pi / 4
        c.move_to(0, -470); c.line_to(math.cos(a) * 44, -470 + math.sin(a) * 44)
        rgb(c, dk(base, 0.25)); c.set_line_width(4); c.stroke()
    for sx in (-170, 130):
        janela_i(c, sx, -330, 40, 150, "gotica", acesa, None, depth)
    c.move_to(-70, 0); c.line_to(-70, -150); c.curve_to(-70, -210, -30, -240, 0, -260); c.curve_to(30, -240, 70, -210, 70, -150)
    c.line_to(70, 0); c.close_path(); rgb(c, dk(base, 0.3)); c.fill()
    c.move_to(-54, 0); c.line_to(-54, -146); c.curve_to(-54, -196, -24, -222, 0, -238); c.curve_to(24, -222, 54, -196, 54, -146)
    c.line_to(54, 0); c.close_path()
    if acesa:
        lgrad(c, 0, -238, 0, 0, [(0, (1.0, 0.80, 0.45), 1), (1, (0.98, 0.62, 0.30), 1)]); c.fill()
        rglow(c, 0, -60, 300, JANELA_ACESA, 0.25)
    else:
        rgb(c, P(MADEIRA_ESC, depth)); c.fill()
    c.restore()


def torre_castelo(c, x, y, w=160, h=420, depth=0.0, col=PEDRA):
    base = P(col, depth)
    c.rectangle(x - w / 2, y - h, w, h); rgb(c, base); c.fill()
    for k in range(4):
        c.rectangle(x - w / 2 + k * w / 3.5 - 4, y - h - 30, w / 7, 32); c.fill()
    c.rectangle(x + w / 2 - 26, y - h, 26, h); rgb(c, dk(base, 0.1)); c.fill()
    janela_i(c, x - 12, y - h * 0.7, 24, 60, "arco", None, None, depth)


def piramide(c, x, y, w=420, h=280, depth=0.3):
    base = P(AREIA, depth)
    pg(c, [(x - w / 2, y), (x, y - h), (x + w / 2, y)]); rgb(c, base); c.fill()
    side = -_L["dir"]
    pg(c, [(x, y - h), (x + side * w / 2, y), (x + side * w * 0.08, y)]); rgb(c, dk(base, 0.2)); c.fill()
    for k in range(1, 9):
        yy = y - h * k / 9
        hw = w / 2 * (1 - k / 9)
        c.move_to(x - hw, yy); c.line_to(x + hw, yy); rgb(c, dk(base, 0.08), 0.6); c.set_line_width(2); c.stroke()


def dunas(c, y=780, seed=1, depth=0.3, col=AREIA, amp=60):
    rnd = random.Random(seed)
    pts = []
    x = -100
    while x < W + 200:
        pts.append((x, y - rnd.uniform(0.2, 1.0) * amp))
        x += rnd.uniform(240, 420)
    base = P(col, depth)
    c.move_to(-100, H)
    for i, (px, py) in enumerate(pts):
        if i == 0:
            c.line_to(px, py)
        else:
            qx, qy = pts[i - 1]
            c.curve_to(qx + (px - qx) * 0.5, qy, qx + (px - qx) * 0.5, py, px, py)
    c.line_to(W + 200, H); c.close_path(); rgb(c, base); c.fill()
    for i in range(1, len(pts)):
        px, py = pts[i]
        pg(c, [(px, py), (px + 140 * -_L["dir"], py + 60), (px + 10, py + 80)]); rgb(c, dk(base, 0.10), 0.7); c.fill()


# ================================================================ água e navios
def mar_i(c, t, y=700, col=AGUA, reflexo=True):
    L = _L
    top = mix(P(col), L["ceu"][1], 0.35)
    lgrad(c, 0, y, 0, H, [(0, top, 1), (1, dk(P(col), 0.35), 1)])
    c.rectangle(-20, y, W + 40, H - y); c.fill()
    rnd = random.Random(5)
    for i in range(60):
        k = rnd.uniform(0, 1) ** 1.7
        yy = y + 6 + (H - y) * k
        x = (rnd.uniform(0, W) + math.sin(t * 0.6 + i) * 30)
        w_ = 20 + 90 * k
        rr(c, x, yy, w_, 3 + 3 * k, 2); rgb(c, lt(top, 0.25), 0.45); c.fill()
    if reflexo and L["astro"]:
        kind, ax, ay, acol = L["astro"]
        for i in range(14):
            yy = y + 10 + i * (H - y) / 14
            ww = 30 + i * 9 + math.sin(t * 2 + i) * 12
            rr(c, ax - ww / 2 + math.sin(t * 1.3 + i * 0.7) * 10, yy, ww, 4 + i * 0.3, 2)
            rgb(c, lt(acol, 0.1), 0.5 * (1 - i / 16)); c.fill()


def nau(c, t, s=1.0, vela=(0.92, 0.88, 0.78), casco=(0.38, 0.25, 0.16), cruz=True, depth=0.0, balanco=True):
    """veleiro antigo (galé/nau medieval ou do séc. XIX); origem = linha d'água no centro"""
    c.save(); c.scale(s, s)
    if balanco:
        c.rotate(math.sin(t * 0.8) * 0.02); c.translate(0, math.sin(t * 1.1) * 3)
    hc = P(casco, depth)
    c.move_to(-260, -70); c.line_to(250, -80); c.curve_to(230, -20, 180, 10, 120, 12); c.line_to(-180, 12)
    c.curve_to(-230, 0, -255, -40, -260, -70); c.close_path(); rgb(c, hc); c.fill()
    c.rectangle(-240, -70, 480, 12); rgb(c, dk(hc, 0.3)); c.fill()
    c.rectangle(-200, -40, 400, 8); rgb(c, lt(hc, 0.15)); c.fill()
    for mx, mh, sw in ((-90, 360, 170), (80, 400, 190)):
        c.rectangle(mx - 5, -70 - mh, 10, mh); rgb(c, P(MADEIRA_ESC, depth)); c.fill()
        for k, (yy, ww) in enumerate(((-70 - mh + 40, sw * 0.8), (-70 - mh * 0.55, sw))):
            hh = mh * 0.36
            c.move_to(mx - ww / 2, yy); c.line_to(mx + ww / 2, yy)
            c.curve_to(mx + ww / 2 + 10, yy + hh * 0.5, mx + ww / 2 + 6, yy + hh, mx + ww / 2, yy + hh)
            c.curve_to(mx, yy + hh + 18, mx, yy + hh + 18, mx - ww / 2, yy + hh)
            c.curve_to(mx - ww / 2 + 6, yy + hh * 0.5, mx - ww / 2 + 2, yy + hh * 0.3, mx - ww / 2, yy)
            c.close_path(); rgb(c, P(vela, depth)); c.fill()
            c.move_to(mx + ww * 0.1, yy); c.curve_to(mx + ww * 0.3, yy + hh * 0.5, mx + ww * 0.3, yy + hh * 0.7, mx + ww * 0.2, yy + hh + 10)
            c.line_to(mx + ww / 2, yy + hh); c.curve_to(mx + ww / 2 + 6, yy + hh * 0.5, mx + ww / 2 + 10, yy + hh * 0.3, mx + ww / 2, yy)
            c.close_path(); rgb(c, P(dk(vela, 0.10), depth)); c.fill()
            if cruz and k == 1:
                c.rectangle(mx - 8, yy + hh * 0.2, 16, hh * 0.6); rgb(c, P((0.70, 0.16, 0.14), depth)); c.fill()
                c.rectangle(mx - ww * 0.22, yy + hh * 0.42, ww * 0.44, 16); c.fill()
        wav = math.sin(t * 3 + mx) * 6
        pg(c, [(mx, -70 - mh), (mx + 50, -70 - mh + 10 + wav), (mx, -70 - mh + 22)]); rgb(c, P((0.75, 0.16, 0.14), depth)); c.fill()
    for a, b in (((-90, -430), (-250, -72)), ((80, -470), (248, -82)), ((-90, -430), (80, -470))):
        c.move_to(*a); c.line_to(*b); rgb(c, P(MADEIRA_ESC, depth), 0.8); c.set_line_width(2); c.stroke()
    c.restore()


def vapor(c, t, s=1.0, casco=(0.12, 0.12, 0.13), depth=0.0, fumaca=True):
    """navio a vapor (séc. XIX/XX); origem = linha d'água no centro"""
    c.save(); c.scale(s, s); c.translate(0, math.sin(t * 1.1) * 2)
    hc = P(casco, depth)
    c.move_to(-340, -90); c.line_to(360, -100); c.line_to(320, 6); c.line_to(-300, 6); c.close_path(); rgb(c, hc); c.fill()
    c.rectangle(-310, -8, 640, 14); rgb(c, P((0.62, 0.16, 0.14), depth)); c.fill()
    for i in range(16):
        c.new_sub_path(); c.arc(-260 + i * 36, -52, 5, 0, 6.283); rgb(c, P((0.85, 0.82, 0.7), depth)); c.fill()
    c.rectangle(-180, -160, 300, 70); rgb(c, P((0.92, 0.90, 0.84), depth)); c.fill()
    c.rectangle(-120, -200, 180, 40); c.fill()
    for i in range(10):
        c.rectangle(-170 + i * 29, -140, 16, 16); rgb(c, JANELA_ACESA if _L["noite"] else P((0.25, 0.3, 0.35), depth)); c.fill()
    c.rectangle(-20, -330, 56, 140); rgb(c, hc); c.fill()
    c.rectangle(-20, -300, 56, 22); rgb(c, P((0.62, 0.16, 0.14), depth)); c.fill()
    for mx in (-250, 250):
        c.rectangle(mx - 3, -400, 6, 310); rgb(c, hc); c.fill()
        c.move_to(mx, -400); c.line_to(-330 if mx < 0 else 350, -95); rgb(c, hc, 0.7); c.set_line_width(2); c.stroke()
    if fumaca:
        for i in range(6):
            k = ((t * 0.25 + i / 6) % 1)
            c.new_sub_path(); c.arc(8 - k * 220, -350 - k * 200, 22 + k * 50, 0, 6.283)
            rgb(c, P((0.35, 0.33, 0.32), depth), 0.55 * (1 - k)); c.fill()
    c.restore()


def cais(c, y=860, x0=-20, x1=None, depth=0.0):
    x1 = x1 if x1 is not None else W + 20
    c.rectangle(x0, y, x1 - x0, 40); rgb(c, P(MADEIRA, depth)); c.fill()
    c.rectangle(x0, y + 40, x1 - x0, 10); rgb(c, P(dk(MADEIRA, 0.4), depth)); c.fill()
    x = x0 + 40
    while x < x1:
        c.rectangle(x, y + 30, 22, 120); rgb(c, P(MADEIRA_ESC, depth)); c.fill()
        x += 180


# ================================================================ interiores
def interior(c, t, parede="pedra", piso="madeira", janela="gotica", jx=1380, piso_y=820, cor=None, raio=True):
    """sala: parede (pedra, reboco, madeira, tijolo), piso e uma janela com feixe de luz"""
    cols = dict(pedra=(0.66, 0.66, 0.68), reboco=(0.84, 0.76, 0.64), madeira=(0.48, 0.34, 0.22), tijolo=(0.66, 0.40, 0.30))
    base = P(cor or cols[parede])
    c.rectangle(0, 0, W, piso_y); rgb(c, base); c.fill()
    rnd = random.Random(4)
    if parede in ("pedra", "tijolo"):
        bh = 46 if parede == "pedra" else 26
        bw = 120 if parede == "pedra" else 64
        for r in range(int(piso_y / bh) + 1):
            off = (r % 2) * bw / 2
            for k in range(-1, int(W / bw) + 2):
                rr(c, k * bw - off + 3, r * bh + 3, bw - 6, bh - 6, 3)
                rgb(c, dk(base, rnd.uniform(0.02, 0.10))); c.fill()
    elif parede == "madeira":
        for k in range(0, W, 64):
            c.rectangle(k, 0, 3, piso_y); rgb(c, dk(base, 0.25)); c.fill()
    else:
        for i in range(8):
            ellipse(c, rnd.uniform(0, W), rnd.uniform(0, piso_y), rnd.uniform(80, 200), rnd.uniform(40, 90))
            rgb(c, dk(base, 0.05), 0.5); c.fill()
    c.rectangle(0, piso_y - 30, W, 30); rgb(c, dk(base, 0.25)); c.fill()
    pcol = P(dict(madeira=MADEIRA, pedra=(0.56, 0.54, 0.52), terra=TERRA).get(piso, MADEIRA))
    lgrad(c, 0, piso_y, 0, H, [(0, dk(pcol, 0.1), 1), (1, dk(pcol, 0.35), 1)])
    c.rectangle(0, piso_y, W, H - piso_y); c.fill()
    for i in range(-14, 15):
        c.move_to(W / 2 + i * 60, piso_y); c.line_to(W / 2 + i * 150, H)
        rgb(c, dk(pcol, 0.4), 0.5); c.set_line_width(2.5); c.stroke()
    if janela:
        jw, jh, jy = 170, 300, 170
        dia = not _L["noite"]
        c.save()
        janela_i(c, jx - jw / 2, jy, jw, jh, janela, False, None)
        c.restore()
        if dia:
            c.move_to(jx - jw / 2, jy + 60); c.line_to(jx + jw / 2, jy + 60); c.line_to(jx + jw / 2 - 420, H); c.line_to(jx - jw / 2 - 700, H)
            c.close_path()
            lgrad(c, jx, jy, jx - 500, H, [(0, (1, 0.98, 0.9), 0.30), (1, (1, 0.98, 0.9), 0.0)]); c.fill()
            if raio:
                rnd2 = random.Random(9)
                for i in range(26):
                    k = rnd2.uniform(0, 1)
                    px = jx - k * 500 + rnd2.uniform(-120, 120) + math.sin(t * 0.5 + i) * 20
                    py = jy + 80 + k * (H - jy - 100) + math.cos(t * 0.4 + i) * 20
                    c.new_sub_path(); c.arc(px, py, rnd2.uniform(1.2, 2.6), 0, 6.283); rgb(c, (1, 0.97, 0.85), 0.5); c.fill()
        else:
            rglow(c, jx, jy + jh / 2, 260, (0.5, 0.6, 0.9), 0.10)


def estante(c, x, y, w=520, h=560, seed=2, depth=0.0):
    """estante de livros; origem = canto inferior esquerdo"""
    rnd = random.Random(seed)
    mc = P(MADEIRA_ESC, depth)
    c.rectangle(x, y - h, w, h); rgb(c, dk(mc, 0.35)); c.fill()
    shelves = 4
    sh = h / shelves
    cores = [(0.55, 0.18, 0.16), (0.24, 0.36, 0.28), (0.26, 0.30, 0.46), (0.62, 0.46, 0.22), (0.45, 0.28, 0.38), (0.36, 0.24, 0.16)]
    for s_ in range(shelves):
        by = y - s_ * sh - 14
        bx = x + 14
        while bx < x + w - 40:
            bw = rnd.uniform(18, 34)
            bh = sh * rnd.uniform(0.55, 0.85)
            col = P(rnd.choice(cores), depth)
            if rnd.random() < 0.12:
                bx += bw; continue
            c.rectangle(bx, by - bh, bw - 2, bh); rgb(c, col); c.fill()
            c.rectangle(bx + 3, by - bh * 0.7, bw - 8, bh * 0.22); rgb(c, P((0.86, 0.80, 0.64), depth)); c.fill()
            bx += bw
        c.rectangle(x, by, w, 14); rgb(c, mc); c.fill()
    c.rectangle(x - 10, y - h - 16, w + 20, 18); rgb(c, mc); c.fill()
    c.rectangle(x - 10, y - h, 14, h); c.fill(); c.rectangle(x + w - 4, y - h, 14, h); c.fill()


def mesa_i(c, x, y, w=520, toalha=None, depth=0.0):
    """mesa; origem = centro do tampo (y = altura do tampo)"""
    mc = P(MADEIRA, depth)
    for lx in (-w / 2 + 30, w / 2 - 50):
        c.rectangle(x + lx, y, 20, 170); rgb(c, dk(mc, 0.25)); c.fill()
    c.rectangle(x - w / 2, y - 16, w, 22); rgb(c, mc); c.fill()
    if toalha:
        c.rectangle(x - w / 2 - 6, y - 18, w + 12, 90); rgb(c, P(toalha, depth)); c.fill()
        c.rectangle(x - w / 2 - 6, y + 64, w + 12, 8); rgb(c, P(dk(toalha, 0.2), depth)); c.fill()


def vela_i(c, t, x, y, s=1.0):
    """vela acesa com brilho; origem = base"""
    c.save(); c.translate(x, y); c.scale(s, s)
    rglow(c, 0, -110, 420, (1.0, 0.75, 0.40), 0.22)
    ellipse(c, 0, 0, 30, 8); rgb(c, P((0.55, 0.45, 0.3))); c.fill()
    c.rectangle(-9, -80, 18, 80); rgb(c, (0.95, 0.92, 0.82)); c.fill()
    c.rectangle(3, -80, 6, 80); rgb(c, (0.85, 0.80, 0.68)); c.fill()
    fl = 1 + 0.12 * math.sin(t * 13) * math.sin(t * 7.1)
    c.save(); c.translate(0, -84); c.scale(1, fl)
    c.move_to(0, 0); c.curve_to(-9, -8, -5, -26, 0, -36); c.curve_to(5, -26, 9, -8, 0, 0)
    rgb(c, (1.0, 0.82, 0.40)); c.fill()
    ellipse(c, 0, -8, 3, 7); rgb(c, (1, 0.97, 0.85)); c.fill()
    c.restore()
    rglow(c, 0, -100, 60, (1, 0.9, 0.6), 0.5)
    c.restore()


def livro_aberto(c, w=260, depth=0.0):
    pg(c, [(-w / 2, 0), (0, 8), (w / 2, 0), (w / 2 - 10, -40), (0, -34), (-w / 2 + 10, -40)])
    rgb(c, P((0.93, 0.89, 0.78), depth)); c.fill()
    for k in range(4):
        for sx in (-1, 1):
            c.move_to(sx * 20, -28 + k * 7); c.line_to(sx * (w / 2 - 22), -32 + k * 7)
            rgb(c, P((0.4, 0.3, 0.2), depth), 0.6); c.set_line_width(1.5); c.stroke()


def cruz_parede(c, s=1.0):
    c.save(); c.scale(s, s)
    c.rectangle(-8, -70, 16, 140); rgb(c, P(MADEIRA_ESC)); c.fill()
    c.rectangle(-42, -40, 84, 16); c.fill()
    c.restore()


# ================================================================ personagens
def lanterna_i(c, t=0, s=0.9, acesa=True):
    """lanterna a óleo chapada; origem = argola (na mão)"""
    c.save(); c.scale(s, s)
    if acesa:
        noite = _L["noite"]
        rglow(c, 0, 90, 460 if noite else 330, (1.0, 0.72, 0.36), 0.42 if noite else 0.30)
    metal = P((0.24, 0.20, 0.17))
    c.arc(0, 14, 16, math.pi, 2 * math.pi); rgb(c, metal); c.set_line_width(5); c.stroke()
    pg(c, [(-26, 34), (0, 14), (26, 34)]); rgb(c, metal); c.fill()
    c.rectangle(-28, 34, 56, 10); c.fill()
    c.rectangle(-22, 44, 44, 70)
    rgb(c, (1.0, 0.80, 0.45) if acesa else P((0.4, 0.42, 0.45))); c.fill()
    if acesa:
        fl = 1 + 0.15 * math.sin(t * 11) * math.sin(t * 6.3)
        c.save(); c.translate(0, 98); c.scale(1, fl)
        c.move_to(0, 0); c.curve_to(-8, -8, -4, -22, 0, -30); c.curve_to(4, -22, 8, -8, 0, 0)
        rgb(c, (1.0, 0.97, 0.80)); c.fill(); c.restore()
    for xx in (-22, 0, 20):
        c.rectangle(xx - 1, 44, 3, 70); rgb(c, metal); c.fill()
    c.rectangle(-28, 112, 56, 12); rgb(c, metal); c.fill()
    c.restore()


def _limb(c, o, tgt, l1, l2, bend, w1, w2, col):
    (ex, ey), (hx, hy) = engine._ik(o[0], o[1], tgt[0], tgt[1], l1, l2, bend)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.move_to(*o); c.line_to(ex, ey); rgb(c, col); c.set_line_width(w1); c.stroke()
    c.move_to(ex, ey); c.line_to(hx, hy); c.set_line_width(w2); c.stroke()
    c.new_sub_path(); c.arc(ex, ey, (w1 + w2) / 4, 0, 6.283); c.fill()
    return (ex, ey), (hx, hy)


def boneco(c, t, x, y, s=1.0, poses=((0, "stand"),), exprs=((0, "neutral"),), look=0.0,
           pele="clara", cabelo="curto", cor_cabelo=None, barba=None, bigode=False, idade=0.0,
           chapeu=None, cor_chapeu=None, roupa="camisa", cor_roupa=(0.30, 0.40, 0.55), cor_calca=(0.28, 0.24, 0.20),
           cor_sapato=(0.16, 0.11, 0.08), camisa=(0.92, 0.90, 0.84), gravata=None, oculos=False, cinto=None,
           capa=None, prop=None, fid=0, appear=None, alpha=1.0, andar=False, mulher=False, largura=1.0):
    """
    Personagem ilustrado (chapado, sem contorno), pés em (x, y), altura ~470 px em s=1.
    poses / exprs: as mesmas do boneco de giz (stand, point_r, think, shocked...).
    roupa: camisa | casaco (sobretudo até o joelho) | tunica (até o pé) | batina | vestido | jaqueta | armadura
    cabelo: curto | longo | calvo | careca | tonsura | coque | cacheado | None
    barba: cheia | curta | cavanhaque | longa | None    chapeu: fedora cartola quepe gorro capuz tiara palha
    turbante solideu touca explorador boina coroa elmo
    prop: ("r"|"l", fn(c, t)) desenha algo preso à mão (origem = mão).
    """
    a_scale = 1.0
    if appear is not None:
        if t < appear:
            return
        a_scale = ease_out_back(prog(t, appear, 0.45))
        if a_scale < 0.02:
            return
    Pz = engine.pose_at(t, list(poses))
    expr = engine.val_at(t, list(exprs))
    if callable(look):
        look = look(t)
    skin = P(PELES.get(pele, pele) if isinstance(pele, str) else pele)
    hcol = cor_cabelo if cor_cabelo is not None else CABELOS["castanho"]
    if isinstance(hcol, str):
        hcol = CABELOS[hcol]
    hcol = P(mix(hcol, CABELOS["grisalho"], idade))
    roupa_c = P(cor_roupa)
    calca = P(cor_calca)
    shade = lambda col, k=0.16: dk(col, k)
    ld = _L["dir"]  # luz vem deste lado; sombra no oposto

    c.save()
    c.translate(x, y)
    c.scale(s * a_scale, s * a_scale)
    if alpha < 1:
        c.push_group()
    bob = math.sin(t * 2.0 + fid) * 1.8
    # sombra no chão
    ellipse(c, -ld * 14, 2, 78, 11); rgb(c, (0, 0, 0), 0.20); c.fill()

    hipy = -190
    shy = -326 + bob
    rf, lf = Pz["rf"], Pz["lf"]
    running = Pz.get("run")
    if andar or running:
        sp = 11 if running else 6.5
        ph = t * sp + fid * 1.3
        amp = 60 if running else 34
        rf = (16 + amp * math.sin(ph), 186 - 22 * max(0, math.cos(ph)))
        lf = (-16 - amp * math.sin(ph), 186 - 22 * max(0, -math.cos(ph)))
        hipy -= abs(math.sin(ph)) * 5
        shy -= abs(math.sin(ph)) * 5
    longa = roupa in ("tunica", "batina", "vestido")
    # pernas
    feet = []
    for side, tgt, bend in ((-1, lf, 1), (1, rf, -1)):
        o = (side * 20, hipy)
        (kx, ky), (fx_, fy_) = engine._ik(o[0], o[1], tgt[0], hipy + tgt[1] + 4, 96, 94, bend)
        col = calca if side == ld else shade(calca, 0.12)
        if not longa:
            c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(*o); c.line_to(kx, ky); c.line_to(fx_, fy_); rgb(c, col); c.set_line_width(36); c.stroke()
        feet.append((side, fx_, fy_))
    for side, fx_, fy_ in feet:
        c.save(); c.translate(fx_ + side * 10, fy_ - 4)
        c.move_to(-22, 6); c.curve_to(-22, -14, 22, -14, 26 * (1 if side > 0 else 1), 2); c.line_to(26, 8); c.line_to(-22, 8); c.close_path()
        c.restore()
        rgb(c, P(cor_sapato)); c.fill()
    # capa (atrás do corpo)
    if capa:
        pg(c, [(-50, shy - 4), (50, shy - 4), (86, -20), (-86, -20)]); rgb(c, shade(P(capa), 0.2)); c.fill()
    # tronco
    sw = 48 * largura
    if roupa == "casaco":
        hem, hw = -96, 66
    elif longa:
        hem, hw = -14, 74 if roupa != "vestido" else 84
    elif roupa == "armadura":
        hem, hw = hipy + 30, 54
    else:
        hem, hw = hipy + 24, 52
    hw *= largura

    def tronco_path():
        c.move_to(-sw, shy + 16)
        c.curve_to(-sw, shy - 6, -sw + 16, shy - 10, -20, shy - 10)
        c.line_to(20, shy - 10)
        c.curve_to(sw - 16, shy - 10, sw, shy - 6, sw, shy + 16)
        c.line_to(hw, hem); c.curve_to(hw * 0.4, hem + 6, -hw * 0.4, hem + 6, -hw, hem)
        c.close_path()
    if not longa and roupa != "casaco":
        # calça até a cintura
        c.rectangle(-46, hipy - 12, 92, 30); rgb(c, calca); c.fill()
    tronco_path(); rgb(c, roupa_c); c.fill()
    c.save(); tronco_path(); c.clip()
    if ld < 0:
        c.rectangle(16, shy - 20, 200, 600)
    else:
        c.rectangle(-216, shy - 20, 200, 600)
    rgb(c, (0, 0, 0), 0.13); c.fill()
    if roupa == "casaco":
        # camisa + gravata no V
        pg(c, [(-20, shy - 10), (20, shy - 10), (0, shy + 70)]); rgb(c, P(camisa)); c.fill()
        if gravata:
            pg(c, [(-6, shy - 4), (6, shy - 4), (8, shy + 50), (0, shy + 64), (-8, shy + 50)]); rgb(c, P(gravata)); c.fill()
        pg(c, [(-22, shy - 10), (-4, shy + 74), (-24, shy + 40), (-36, shy + 4)]); rgb(c, shade(roupa_c, 0.12)); c.fill()
        pg(c, [(22, shy - 10), (4, shy + 74), (24, shy + 40), (36, shy + 4)]); c.fill()
        c.move_to(0, shy + 74); c.line_to(4, hem); rgb(c, shade(roupa_c, 0.3)); c.set_line_width(3); c.stroke()
        c.rectangle(-80, -226, 160, 16); rgb(c, shade(roupa_c, 0.22)); c.fill()
        rr(c, -12, -230, 24, 24, 4); rgb(c, P((0.70, 0.58, 0.32))); c.fill()
        for by in (shy + 100, shy + 160):
            c.new_sub_path(); c.arc(-14, by, 4.5, 0, 6.283); rgb(c, shade(roupa_c, 0.45)); c.fill()
    elif roupa in ("tunica", "batina", "vestido"):
        if roupa == "batina":
            c.rectangle(-10, shy - 10, 20, 12); rgb(c, (0.95, 0.95, 0.92)); c.fill()
            for k in range(9):
                c.new_sub_path(); c.arc(0, shy + 14 + k * 30, 3.5, 0, 6.283); rgb(c, shade(roupa_c, 0.4)); c.fill()
        else:
            c.new_sub_path(); c.arc(0, shy - 8, 20, 0, math.pi); rgb(c, shade(roupa_c, 0.25)); c.fill()
            c.rectangle(-80, -214, 160, 12); rgb(c, P(cinto or (0.55, 0.42, 0.26))); c.fill()
            if roupa == "vestido":
                rr(c, -44, -200, 88, 170, 10); rgb(c, P((0.90, 0.87, 0.78))); c.fill()
    elif roupa == "jaqueta":
        c.rectangle(-4, shy, 8, hem - shy); rgb(c, shade(roupa_c, 0.3)); c.fill()
        for k in range(5):
            c.new_sub_path(); c.arc(-14, shy + 24 + k * 30, 4, 0, 6.283); c.new_sub_path(); c.arc(14, shy + 24 + k * 30, 4, 0, 6.283)
            rgb(c, P(OURO)); c.fill()
        pg(c, [(-20, shy - 10), (0, shy + 20), (20, shy - 10)]); rgb(c, P(camisa)); c.fill()
    elif roupa == "armadura":
        for k in range(4):
            c.rectangle(-60, shy + 20 + k * 30, 120, 3); rgb(c, lt(roupa_c, 0.3)); c.fill()
    else:  # camisa
        pg(c, [(-18, shy - 10), (0, shy + 14), (18, shy - 10)]); rgb(c, shade(roupa_c, 0.2)); c.fill()
        c.rectangle(-2, shy + 10, 4, hem - shy - 14); rgb(c, shade(roupa_c, 0.18)); c.fill()
        if gravata:
            pg(c, [(-20, shy - 10), (-4, shy + 8), (-14, shy + 14)]); pg(c, [(20, shy - 10), (4, shy + 8), (14, shy + 14)])
            rgb(c, lt(roupa_c, 0.15)); c.fill()
            pg(c, [(-7, shy - 6), (7, shy - 6), (9, shy + 70), (0, shy + 84), (-9, shy + 70)]); rgb(c, P(gravata)); c.fill()
        c.rectangle(-60, hem - 10, 120, 10); rgb(c, P(cinto or (0.30, 0.20, 0.13))); c.fill()
    c.restore()
    # pescoço
    rr(c, -13, shy - 30, 26, 26, 6); rgb(c, dk(skin, 0.12)); c.fill()
    # braços
    for side, key, bk, fk in ((-1, "lh", "lb", "lf_"), (1, "rh", "rb", "rf_")):
        o = (side * (sw - 10), shy + 10)
        tgt = (Pz[key][0], shy + Pz[key][1])
        if andar and Pz[key][1] > 100:
            tgt = (tgt[0] + math.sin(t * 6.5 + fid * 1.3 + (math.pi if side > 0 else 0)) * 26, tgt[1])
        col = roupa_c if side == ld else shade(roupa_c, 0.12)
        (ex, ey), (hx, hy) = _limb(c, o, tgt, 74, 70, Pz.get(bk, -side), 32, 27, col)
        a = math.atan2(hy - ey, hx - ex)
        cx_, cy_ = hx - math.cos(a) * 6, hy - math.sin(a) * 6
        c.move_to(ex + (cx_ - ex) * 0.85, ey + (cy_ - ey) * 0.85); c.line_to(cx_, cy_)
        rgb(c, shade(col, 0.25)); c.set_line_width(29); c.stroke()  # punho
        c.new_sub_path(); c.arc(hx, hy, 13.5, 0, 6.283); rgb(c, skin); c.fill()
        fing = Pz.get(fk)
        if fing == "point":
            c.move_to(hx, hy); c.line_to(hx + 24 * math.cos(a), hy + 24 * math.sin(a)); rgb(c, skin); c.set_line_width(8); c.stroke()
        elif fing == "thumb":
            c.move_to(hx, hy); c.line_to(hx, hy - 24); rgb(c, skin); c.set_line_width(9); c.stroke()
        elif fing == "point_up":
            c.move_to(hx, hy); c.line_to(hx, hy - 26); rgb(c, skin); c.set_line_width(8); c.stroke()
        if prop and prop[0] == ("l" if side < 0 else "r"):
            c.save(); c.translate(hx, hy); prop[1](c, t); c.restore()
    # cabeça
    _cabeca(c, t, expr, look, fid, skin, hcol, cabelo, barba, bigode, chapeu, cor_chapeu, oculos, shy, ld,
            roupa_c, mulher)
    if alpha < 1:
        c.pop_group_to_source(); c.paint_with_alpha(alpha)
    c.restore()


def _cabeca(c, t, expr, look, fid, skin, hcol, cabelo, barba, bigode, chapeu, cor_chapeu, oculos, shy, ld, roupa_c, mulher):
    hy = shy - 82
    c.save()
    c.translate(look * 5, hy)
    c.rotate(math.sin(t * 0.8 + fid) * 0.025 + look * 0.03)
    fx = look * 9
    sg = 1 if look >= 0 else -1
    ink = (0.16, 0.11, 0.09)
    chap = P(cor_chapeu) if cor_chapeu else None
    # capuz/cabelo de trás
    if chapeu == "capuz":
        ellipse(c, 0, 8, 70, 82); rgb(c, dk(roupa_c, 0.18)); c.fill()
    if cabelo in ("longo",) or (mulher and cabelo not in ("coque", None, "careca")):
        c.move_to(-52, -10); c.curve_to(-62, 40, -60, 80, -40, 96); c.line_to(40, 96); c.curve_to(60, 80, 62, 40, 52, -10); c.close_path()
        rgb(c, dk(hcol, 0.12)); c.fill()
    # orelhas
    for sx in (-1, 1):
        ellipse(c, sx * 46 + fx * 0.3, 6, 9, 14); rgb(c, dk(skin, 0.10)); c.fill()
    # rosto
    ellipse(c, 0, 0, 47, 57); rgb(c, skin); c.fill()
    c.save(); ellipse(c, 0, 0, 47, 57); c.clip()
    ellipse(c, -ld * 52, 6, 34, 70); rgb(c, (0, 0, 0), 0.08); c.fill()
    c.restore()
    # bochechas
    for sx in (-1, 1):
        c.new_sub_path(); c.arc(sx * 25 + fx, 20, 9, 0, 6.283); rgb(c, (0.85, 0.35, 0.30), 0.16); c.fill()
    # barba (antes da boca)
    if barba in ("cheia", "longa"):
        L_ = 78 if barba == "longa" else 64
        c.move_to(-47, 2); c.curve_to(-46, 40, -28, L_, fx * 0.5, L_ + 4); c.curve_to(28, L_, 46, 40, 47, 2)
        c.curve_to(36, 18, 28, 22, 18 + fx, 20); c.curve_to(10, 34, -10, 34, -18 + fx, 20); c.curve_to(-28, 22, -36, 18, -47, 2)
        c.close_path(); rgb(c, hcol); c.fill()
    elif barba == "curta":
        c.move_to(-46, 4); c.curve_to(-44, 40, -26, 58, fx * 0.5, 60); c.curve_to(26, 58, 44, 40, 46, 4)
        c.curve_to(30, 30, -30, 30, -46, 4); c.close_path(); rgb(c, hcol, 0.45); c.fill()
    elif barba == "cavanhaque":
        ellipse(c, fx * 0.6, 48, 16, 12); rgb(c, hcol); c.fill()
    # olhos
    blink = ((t * 1000 + fid * 1777) % 4300) < 120
    ey_ = -2
    big = expr in ("shocked", "desperate")
    for sx in (-1, 1):
        ex = sx * 17 + fx
        if blink:
            c.move_to(ex - 6, ey_); c.line_to(ex + 6, ey_); rgb(c, ink); c.set_line_width(3); c.stroke()
        elif big:
            c.new_sub_path(); c.arc(ex, ey_, 9, 0, 6.283); rgb(c, (0.98, 0.97, 0.94)); c.fill()
            c.new_sub_path(); c.arc(ex + look * 2, ey_, 4.5, 0, 6.283); rgb(c, ink); c.fill()
        else:
            ellipse(c, ex + look * 1.5, ey_, 4.6, 6.2); rgb(c, ink); c.fill()
            c.new_sub_path(); c.arc(ex + look * 1.5 + 1.5, ey_ - 2, 1.4, 0, 6.283); rgb(c, (1, 1, 1), 0.8); c.fill()
    # sobrancelhas
    by = -20 if not big else -27
    ang = dict(worried=0.32, sad=0.32, desperate=0.35, angry=-0.38, shocked=0.0, think=0.18, confident=-0.08)
    a = ang.get(expr, 0.0)
    bc = dk(hcol, 0.2) if cabelo not in ("careca",) else dk(skin, 0.45)
    for sx in (-1, 1):
        aa = a if sx < 0 else -a
        if expr == "think" and sx > 0:
            aa, yy = -0.2, by - 6
        else:
            yy = by
        cx_ = sx * 18 + fx
        c.move_to(cx_ - 9 * math.cos(aa), yy + sx * 9 * math.sin(aa) * -1)
        c.line_to(cx_ + 9 * math.cos(aa), yy - sx * 9 * math.sin(aa) * -1)
        rgb(c, bc); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    # nariz
    nx = fx * 1.4
    c.move_to(nx - 2, 0); c.curve_to(nx + sg * 4, 10, nx + sg * 9, 16, nx + sg * 4, 19); c.curve_to(nx, 21, nx - 4, 19, nx - 4, 16)
    c.close_path(); rgb(c, dk(skin, 0.16)); c.fill()
    # bigode
    if bigode or barba in ("cheia", "longa"):
        c.move_to(fx, 24); c.curve_to(fx - 10, 18, fx - 24, 22, fx - 26, 32); c.curve_to(fx - 14, 28, fx - 6, 30, fx, 28)
        c.curve_to(fx + 6, 30, fx + 14, 28, fx + 26, 32); c.curve_to(fx + 24, 22, fx + 10, 18, fx, 24); c.close_path()
        rgb(c, dk(hcol, 0.1)); c.fill()
    # boca
    mx, my = fx * 1.1, 34
    mc_ = (0.45, 0.20, 0.18)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if expr in ("happy", "confident"):
        c.move_to(mx - 10, my - 2); c.curve_to(mx - 4, my + 6, mx + 4, my + 6, mx + 10, my - 2 - (4 if expr == "confident" else 0))
        rgb(c, mc_); c.set_line_width(4); c.stroke()
    elif expr == "grin":
        c.move_to(mx - 13, my - 3); c.curve_to(mx - 8, my + 12, mx + 8, my + 12, mx + 13, my - 3); c.close_path()
        rgb(c, (0.35, 0.12, 0.12)); c.fill()
        c.rectangle(mx - 10, my - 3, 20, 4); rgb(c, (0.98, 0.97, 0.94)); c.fill()
    elif expr in ("shocked", "desperate"):
        ellipse(c, mx, my + 2, 7 if expr == "shocked" else 10, 9 if expr == "shocked" else 12); rgb(c, (0.30, 0.10, 0.10)); c.fill()
    elif expr in ("sad", "worried"):
        c.move_to(mx - 9, my + 4); c.curve_to(mx - 4, my - 2, mx + 4, my - 2, mx + 9, my + 4)
        rgb(c, mc_); c.set_line_width(4); c.stroke()
    elif expr == "angry":
        c.move_to(mx - 10, my + 3); c.line_to(mx - 4, my); c.line_to(mx + 4, my); c.line_to(mx + 10, my + 3)
        rgb(c, mc_); c.set_line_width(4); c.stroke()
    elif expr == "think":
        c.move_to(mx - 2, my + 1); c.line_to(mx + 10, my - 2); rgb(c, mc_); c.set_line_width(4); c.stroke()
    else:
        c.move_to(mx - 8, my); c.line_to(mx + 8, my); rgb(c, mc_); c.set_line_width(4); c.stroke()
    # óculos
    if oculos:
        gc = (0.30, 0.22, 0.14) if oculos is True else (0.12, 0.12, 0.14)
        for sx in (-1, 1):
            ex = sx * 17 + fx
            if oculos == "ret":
                rr(c, ex - 14, -12, 28, 20, 5)
            else:
                c.new_sub_path(); c.arc(ex, -2, 13, 0, 6.283)
            rgb(c, (1, 1, 1), 0.12); c.fill_preserve()
            rgb(c, gc); c.set_line_width(3.4); c.stroke()
        c.move_to(-4 + fx, -4); c.curve_to(-2 + fx, -8, 2 + fx, -8, 4 + fx, -4); c.stroke()
        for sx in (-1, 1):
            c.move_to(sx * 30 + fx, -4); c.line_to(sx * 46 + fx * 0.3, -6); c.stroke()
    # cabelo (frente)
    if cabelo in ("curto", "longo", "cacheado", "coque") or (cabelo and mulher):
        c.move_to(-49, 8); c.curve_to(-54, -40, -30, -64, 0, -63); c.curve_to(32, -64, 54, -40, 49, 8)
        c.curve_to(46, -10, 42, -20, 34, -28)
        c.curve_to(14, -20, -10 + fx, -34, -20 + fx, -40) if sg > 0 else c.curve_to(10 + fx, -34, -14, -20, -34, -28)
        c.curve_to(-30, -30, -42, -20, -49, 8) if sg > 0 else c.curve_to(-42, -20, -46, -10, -49, 8)
        c.close_path(); rgb(c, hcol); c.fill()
        if cabelo == "cacheado":
            for k in range(9):
                a_ = math.pi + k * math.pi / 8
                c.new_sub_path(); c.arc(math.cos(a_) * 46, -10 + math.sin(a_) * 54, 12, 0, 6.283)
            rgb(c, hcol); c.fill()
        if cabelo == "coque":
            c.new_sub_path(); c.arc(0, -70, 20, 0, 6.283); rgb(c, hcol); c.fill()
    elif cabelo in ("calvo", "tonsura"):
        for sx in (-1, 1):
            c.move_to(sx * 49, 8); c.curve_to(sx * 52, -20, sx * 44, -40, sx * 30, -46); c.line_to(sx * 40, -10); c.close_path()
            rgb(c, hcol); c.fill()
        if cabelo == "tonsura":
            c.move_to(-46, -24); c.curve_to(-30, -40, 30, -40, 46, -24); c.curve_to(30, -32, -30, -32, -46, -24)
            rgb(c, hcol); c.fill()
    # chapéus
    if chapeu:
        _chapeu(c, t, chapeu, chap, roupa_c, hcol)
    c.restore()


def _chapeu(c, t, kind, col, roupa_c, hcol):
    col = col or P((0.30, 0.22, 0.16))
    if kind in ("fedora", "explorador", "palha"):
        if kind == "palha":
            col = P((0.86, 0.74, 0.46)) if col is None else col
        bw = {"fedora": 82, "explorador": 78, "palha": 104}[kind]
        ellipse(c, 0, -40, bw, 14); rgb(c, dk(col, 0.12)); c.fill()
        if kind == "explorador":
            c.move_to(-50, -40); c.curve_to(-50, -96, 50, -96, 50, -40); c.close_path()
        else:
            c.move_to(-44, -40); c.curve_to(-46, -70, -40, -94, -20, -94); c.curve_to(-8, -94, -6, -86, 0, -86)
            c.curve_to(6, -86, 8, -94, 20, -94); c.curve_to(40, -94, 46, -70, 44, -40); c.close_path()
        rgb(c, col); c.fill()
        c.rectangle(-46, -56, 92, 14); rgb(c, dk(col, 0.45) if kind != "palha" else P((0.55, 0.20, 0.16))); c.fill()
        c.move_to(-bw, -40); c.curve_to(-bw + 10, -26, bw - 10, -26, bw, -40); c.curve_to(bw - 20, -34, -bw + 20, -34, -bw, -40)
        rgb(c, col); c.fill()
    elif kind == "cartola":
        ellipse(c, 0, -44, 66, 11); rgb(c, col); c.fill()
        c.rectangle(-38, -150, 76, 106); c.fill()
        c.rectangle(-38, -66, 76, 14); rgb(c, lt(col, 0.15)); c.fill()
    elif kind == "quepe":
        c.move_to(-50, -30); c.curve_to(-54, -70, 54, -70, 50, -30); c.close_path(); rgb(c, col); c.fill()
        ellipse(c, 0, -74, 58, 14); rgb(c, lt(col, 0.05)); c.fill()
        c.rectangle(-50, -44, 100, 12); rgb(c, dk(col, 0.4)); c.fill()
        c.move_to(-46, -32); c.curve_to(-20, -18, 30, -18, 52, -30); c.line_to(48, -36); c.close_path(); rgb(c, (0.1, 0.1, 0.1)); c.fill()
        c.new_sub_path(); c.arc(0, -50, 8, 0, 6.283); rgb(c, P(OURO)); c.fill()
    elif kind == "gorro":
        c.move_to(-50, -18); c.curve_to(-58, -70, -20, -96, 10, -90); c.curve_to(48, -84, 58, -50, 50, -18); c.close_path()
        rgb(c, col); c.fill()
        rr(c, -54, -34, 108, 22, 10); rgb(c, dk(col, 0.15)); c.fill()
    elif kind == "boina":
        ellipse(c, 6, -50, 60, 22); rgb(c, col); c.fill()
    elif kind == "solideu":
        c.move_to(-34, -44); c.curve_to(-30, -66, 30, -66, 34, -44); c.close_path(); rgb(c, col); c.fill()
    elif kind == "capuz":
        c.move_to(-62, 40); c.curve_to(-70, -70, 70, -70, 62, 40); c.curve_to(54, -20, 30, -52, 0, -52)
        c.curve_to(-30, -52, -54, -20, -62, 40); c.close_path(); rgb(c, roupa_c); c.fill()
    elif kind == "touca":
        c.move_to(-60, 60); c.curve_to(-68, -76, 68, -76, 60, 60); c.curve_to(52, -10, 40, -50, 0, -52)
        c.curve_to(-40, -50, -52, -10, -60, 60); c.close_path(); rgb(c, P((0.95, 0.94, 0.90))); c.fill()
    elif kind == "tiara":
        c.move_to(-40, -40); c.curve_to(-46, -120, -20, -150, 0, -150); c.curve_to(20, -150, 46, -120, 40, -40); c.close_path()
        rgb(c, P((0.96, 0.94, 0.88))); c.fill()
        for yy in (-50, -84, -114):
            c.rectangle(-46, yy, 92, 10); rgb(c, P(OURO)); c.fill()
        c.new_sub_path(); c.arc(0, -156, 8, 0, 6.283); c.fill()
    elif kind == "turbante":
        ellipse(c, 0, -52, 58, 32); rgb(c, col); c.fill()
        for k in range(3):
            c.move_to(-54, -40 - k * 14); c.curve_to(-20, -60 - k * 14, 20, -36 - k * 14, 54, -54 - k * 10)
            rgb(c, dk(col, 0.15)); c.set_line_width(3); c.stroke()
    elif kind == "coroa":
        pg(c, [(-40, -40), (-44, -90), (-22, -66), (0, -96), (22, -66), (44, -90), (40, -40)]); rgb(c, P(OURO)); c.fill()
    elif kind == "elmo":
        c.move_to(-52, 10); c.curve_to(-56, -70, 56, -70, 52, 10); c.line_to(40, 10); c.line_to(40, -14); c.line_to(-40, -14)
        c.line_to(-40, 10); c.close_path(); rgb(c, P((0.62, 0.64, 0.68))); c.fill()
        c.rectangle(-4, -14, 8, 40); c.fill()


# figurinos prontos (passe com **)
FIGURINO = dict(
    campones=dict(roupa="tunica", cor_roupa=(0.42, 0.50, 0.40), cabelo="curto", barba="cheia", chapeu="gorro", cor_chapeu=(0.55, 0.20, 0.16)),
    camponesa=dict(roupa="vestido", cor_roupa=(0.55, 0.30, 0.26), cabelo="longo", mulher=True, chapeu="touca"),
    monge=dict(roupa="tunica", cor_roupa=(0.34, 0.25, 0.18), cabelo="tonsura", cinto=(0.80, 0.72, 0.52)),
    padre=dict(roupa="batina", cor_roupa=(0.12, 0.12, 0.14), cabelo="calvo", idade=0.5),
    papa=dict(roupa="tunica", cor_roupa=(0.82, 0.24, 0.20), chapeu="tiara", cabelo="calvo", idade=0.7, capa=(0.86, 0.68, 0.28)),
    nobre=dict(roupa="tunica", cor_roupa=(0.30, 0.20, 0.42), capa=(0.62, 0.14, 0.14), chapeu="coroa", barba="cheia"),
    marinheiro=dict(roupa="camisa", cor_roupa=(0.86, 0.84, 0.78), cor_calca=(0.22, 0.28, 0.42), chapeu="gorro", cor_chapeu=(0.24, 0.30, 0.46), barba="curta"),
    capitao=dict(roupa="jaqueta", cor_roupa=(0.14, 0.18, 0.30), cor_calca=(0.14, 0.18, 0.30), chapeu="quepe", cor_chapeu=(0.14, 0.18, 0.30), barba="cheia"),
    cavalheiro=dict(roupa="casaco", cor_roupa=(0.16, 0.16, 0.18), chapeu="cartola", cor_chapeu=(0.12, 0.12, 0.13), bigode=True, gravata=(0.15, 0.15, 0.15)),
    dama=dict(roupa="vestido", cor_roupa=(0.30, 0.36, 0.54), cabelo="coque", mulher=True),
    explorador=dict(roupa="camisa", cor_roupa=(0.76, 0.68, 0.50), cor_calca=(0.50, 0.42, 0.30), chapeu="explorador", cor_chapeu=(0.82, 0.76, 0.60), bigode=True),
    medico=dict(roupa="casaco", cor_roupa=(0.95, 0.94, 0.90), cabelo="curto", bigode=True, gravata=(0.15, 0.15, 0.2)),
    soldado=dict(roupa="armadura", cor_roupa=(0.58, 0.60, 0.64), chapeu="elmo", barba="curta"),
    escriba=dict(roupa="tunica", cor_roupa=(0.86, 0.82, 0.70), chapeu="turbante", cor_chapeu=(0.92, 0.90, 0.84), pele="morena", barba="longa"),
)


def figurantes(c, t, y=900, n=8, s=0.32, seed=1, x0=200, x1=1700, andando=True, figurinos=None, depth=0.0):
    """gente pequena no fundo andando (ou parada)"""
    rnd = random.Random(seed)
    figs = figurinos or ["campones", "camponesa", "monge", "marinheiro"]
    for i in range(n):
        fig = dict(FIGURINO[rnd.choice(figs)])
        fig["pele"] = rnd.choice(list(PELES))
        fig["cor_cabelo"] = rnd.choice(list(CABELOS)[:4])
        vel = rnd.uniform(30, 60) * rnd.choice([-1, 1]) if andando else 0
        x = x0 + ((rnd.uniform(0, 1) * (x1 - x0) + t * vel) % (x1 - x0))
        boneco(c, t, x, y + rnd.uniform(-10, 10), s * rnd.uniform(0.9, 1.08), look=0.8 if vel > 0 else -0.8,
               andar=andando, fid=10 + i, **fig)


# ================================================================ textos do estilo
def _bold(c, font):
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)


def rotulo(c, t, t0, titulo, sub=None, x=150, y=950, size=54, d=0.5):
    """legenda de canto (como "1903 · OSWALDO CRUZ"): título forte + linha âmbar + subtítulo"""
    if t < t0:
        return
    p = ease_out(prog(t, t0, d))
    c.save(); c.translate(x - 30 * (1 - p), y)
    _bold(c, SERIF); c.set_font_size(size)
    w = c.text_extents(titulo).x_advance
    for dx, dy, col, a in ((3, 4, (0, 0, 0), 0.55), (0, 0, (0.98, 0.96, 0.90), 1)):
        c.move_to(dx, dy); rgb(c, col, a * p); c.show_text(titulo)
    c.rectangle(0, 18, w * p, 4); rgb(c, AMBER, p); c.fill()
    if sub:
        c.select_font_face(TYPE); c.set_font_size(size * 0.48)
        for dx, dy, col, a in ((2, 3, (0, 0, 0), 0.6), (0, 0, (0.95, 0.92, 0.84), 1)):
            c.move_to(dx, 56 + dy); rgb(c, col, a * p); c.show_text(sub)
    c.restore()


def placa(c, titulo, sub=None, w=None, size=40):
    """cartão de pergaminho com título e sobretítulo (centrado na origem)"""
    _bold(c, SERIF); c.set_font_size(size)
    tw = c.text_extents(titulo).x_advance
    w = w or tw + 80
    h = size * 2.4 + (size * 0.8 if sub else 0)
    c.save(); c.rotate(-0.012)
    rr(c, -w / 2 + 6, -h / 2 + 8, w, h, 6); rgb(c, (0, 0, 0), 0.35); c.fill()
    rr(c, -w / 2, -h / 2, w, h, 6); rgb(c, (0.93, 0.88, 0.76)); c.fill()
    rr(c, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 4); rgb(c, (0.55, 0.40, 0.22), 0.6); c.set_line_width(2); c.stroke()
    yy = -h / 2 + size * 1.25
    if sub:
        c.select_font_face(TYPE); c.set_font_size(size * 0.5)
        sw_ = c.text_extents(sub).x_advance
        c.move_to(-sw_ / 2, yy - size * 0.2); rgb(c, (0.55, 0.40, 0.22)); c.show_text(sub)
        yy += size * 0.9
    _bold(c, SERIF); c.set_font_size(size)
    c.move_to(-tw / 2, yy + size * 0.2); rgb(c, (0.20, 0.13, 0.08)); c.show_text(titulo)
    c.restore()


def titulo_i(c, s, x=960, y=200, size=96, col=(0.98, 0.95, 0.88), sombra=0.6):
    """título grande com sombra (legível sobre céu claro)"""
    _bold(c, SERIF); c.set_font_size(size)
    w = c.text_extents(s).x_advance
    for k in range(6, 0, -1):
        c.move_to(x - w / 2 + k * 0.8, y + k); rgb(c, (0, 0, 0), sombra / 6); c.show_text(s)
    c.move_to(x - w / 2, y); rgb(c, col); c.show_text(s)


# ================================================================ cenários prontos
def cena_vila(c, t, hora="tarde", estilo="medieval", seed=1, chao_y=880, igreja_x=None, passaros=True):
    """rua de vila/cidade: céu, montanhas, casario de fundo, casario da frente e calçamento"""
    luz(hora)
    ceu(c, t, passaros=passaros and not _L["noite"], seed=seed)
    montanhas(c, 560, 260, seed=seed, depth=0.8, neve=True)
    colinas(c, 650, 40, seed=seed, col=GRAMA, depth=0.55)
    casario(c, t, 690, estilo, seed=seed + 5, depth=0.45, escala=0.55)
    if igreja_x is not None:
        igreja(c, igreja_x, 700, 0.55, depth=0.35)
    casario(c, t, chao_y, estilo, seed=seed + 1, depth=0.0, h=(300, 430))
    chao(c, t, chao_y, "pedra", seed=seed)


def cena_porto(c, t, hora="dia", seed=2):
    luz(hora)
    ceu(c, t, passaros=True, seed=seed)
    montanhas(c, 520, 200, seed=seed, depth=0.85, col=(0.45, 0.52, 0.50))
    mar_i(c, t, 520)
    casario(c, t, 600, "pedra", seed=seed + 3, depth=0.5, escala=0.42, x0=-60, x1=700)
    igreja(c, 330, 600, 0.32, depth=0.5)
    for i, (xx, yy, ss) in enumerate(((900, 640, 0.42), (1250, 610, 0.32), (1560, 660, 0.48))):
        c.save(); c.translate(xx, yy); nau(c, t + i * 2, ss, depth=0.25); c.restore()
    cais(c, 860)
    chao(c, t, 900, "pedra", seed=seed)


def cena_floresta(c, t, hora="dia", seed=3, densa=True):
    luz(hora)
    ceu(c, t, seed=seed)
    montanhas(c, 600, 220, seed=seed, depth=0.85, col=(0.36, 0.48, 0.44))
    colinas(c, 650, 30, seed=seed, col=(0.28, 0.44, 0.30), depth=0.6)
    floresta(c, t, 680, 22, (180, 280), ("redonda",), seed=seed, depth=0.6)
    colinas(c, 740, 20, seed=seed + 2, col=(0.30, 0.46, 0.28), depth=0.35)
    floresta(c, t, 760, 14, (260, 400), ("redonda", "palmeira"), seed=seed + 1, depth=0.3)
    chao(c, t, 860, "grama", seed=seed)
    if densa:
        for i, xx in enumerate((-40, 1880)):
            arvore(c, t, xx, 1080, 900, "redonda", (0.22, 0.36, 0.24), seed + 50 + i)


def cena_deserto(c, t, hora="tarde", seed=4, piramides=True):
    luz(hora)
    ceu(c, t, nuvens=2, seed=seed)
    dunas(c, 700, seed=seed, depth=0.6, amp=50)
    if piramides:
        piramide(c, 1250, 720, 520, 340, depth=0.45)
        piramide(c, 1620, 730, 340, 220, depth=0.5)
    dunas(c, 840, seed=seed + 1, depth=0.15, amp=70)
    arvore(c, t, 1780, 900, 360, "palmeira", seed=seed)
    chao(c, t, 930, "areia", seed=seed)


def cena_neve(c, t, hora="noite", seed=5, nevando=True):
    luz(hora)
    ceu(c, t, nuvens=2, seed=seed)
    montanhas(c, 700, 460, seed=seed, depth=0.6, neve=True, col=(0.44, 0.48, 0.56))
    montanhas(c, 800, 260, seed=seed + 1, depth=0.3, neve=True, col=(0.40, 0.44, 0.52), picos=5)
    floresta(c, t, 840, 12, (160, 260), ("pinheiro",), (0.20, 0.32, 0.30), seed=seed, depth=0.35)
    chao(c, t, 860, "neve", seed=seed)
    if nevando:
        rnd = random.Random(11)
        for i in range(160):
            x0, y0, sp, r = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(60, 160), rnd.uniform(2, 5)
            yy = (y0 + t * sp) % (H + 20) - 10; xx = (x0 + t * 50 + math.sin(t * 1.5 + i) * 15) % W
            rgb(c, (0.95, 0.96, 0.99), 0.7 * r / 5); c.new_sub_path(); c.arc(xx, yy, r, 0, 6.283); c.fill()


def cena_mar(c, t, hora="noite", seed=6, navio="nau"):
    luz(hora)
    ceu(c, t, seed=seed)
    mar_i(c, t, 640)
    c.save(); c.translate(1150, 760)
    (vapor if navio == "vapor" else nau)(c, t, 0.9)
    c.restore()


def cena_campo(c, t, hora="dia", seed=7):
    luz(hora)
    ceu(c, t, passaros=True, seed=seed)
    montanhas(c, 620, 280, seed=seed, depth=0.8, neve=True)
    colinas(c, 700, 50, seed=seed, depth=0.45)
    floresta(c, t, 720, 9, (120, 200), ("redonda", "cipreste"), seed=seed, depth=0.4)
    colinas(c, 830, 30, seed=seed + 1, depth=0.1)
    chao(c, t, 880, "grama", seed=seed)


def cena_interior(c, t, hora="vela", tipo="biblioteca", seed=8):
    """interiores: biblioteca, cela (monge escrevendo), salao (mesa posta), escritorio"""
    luz(hora)
    if tipo == "biblioteca":
        interior(c, t, "madeira", "madeira", None, piso_y=860)
        estante(c, 60, 860, 560, 620, seed)
        estante(c, 700, 860, 560, 620, seed + 1)
        estante(c, 1340, 860, 560, 620, seed + 2)
    elif tipo == "cela":
        interior(c, t, "pedra", "pedra", "gotica", jx=1450)
        c.save(); c.translate(1000, 300); cruz_parede(c, 0.9); c.restore()
    elif tipo == "salao":
        interior(c, t, "reboco", "pedra", "gotica", jx=1500)
        mesa_i(c, 960, 800, 1200, toalha=(0.92, 0.90, 0.84))
    else:
        interior(c, t, "reboco", "madeira", "retangular", jx=1500)
        mesa_i(c, 1250, 790, 560)
    if _L["noite"]:
        c.rectangle(0, 0, W, H); rgb(c, (0.05, 0.03, 0.02), 0.25); c.fill()


def particulas(c, t, tipo="poeira", n=40, seed=1):
    """partículas no ar: poeira (luz quente), brasas (incêndio, sobem), cinzas (caem), vagalumes (noite)"""
    rnd = random.Random(seed)
    for i in range(n):
        x0, y0, sp, ph = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(10, 40), rnd.uniform(0, 6.28)
        if tipo == "brasas":
            x = (x0 + math.sin(t * 1.3 + ph) * 40) % W; y = (y0 - t * sp * 3) % H
            col, r, a = (1.0, 0.55, 0.20), rnd.uniform(2, 4), 0.8
        elif tipo == "cinzas":
            x = (x0 + t * 20 + math.sin(t + ph) * 30) % W; y = (y0 + t * sp) % H
            col, r, a = (0.55, 0.52, 0.50), rnd.uniform(2, 4), 0.6
        elif tipo == "vagalumes":
            x = (x0 + math.sin(t * 0.4 + ph) * 60) % W; y = 500 + (y0 % 500) + math.cos(t * 0.5 + ph) * 30
            col, r, a = (0.95, 1.0, 0.55), 3, 0.5 + 0.5 * math.sin(t * 3 + ph)
            rglow(c, x, y, 16, col, 0.35 * a)
        else:
            x = (x0 + math.sin(t * 0.3 + ph) * 50) % W; y = (y0 - t * sp * 0.4) % H
            col, r, a = (1.0, 0.95, 0.80), rnd.uniform(1.2, 2.8), 0.35 + 0.3 * math.sin(t * 1.5 + ph)
        c.new_sub_path(); c.arc(x, y, r, 0, 6.283); rgb(c, col, max(0, a)); c.fill()


# ================================================================ THUMBNAILS (1280x720, desenhadas em 1920x1080)
# Fórmula: 1 rosto grande com emoção forte (o Historiador em close) + 2 a 4 palavras enormes + 1 objeto/cenário
# central + contraste alto. Nada de texto pequeno. O tom do vídeo vale aqui também.
def thumb_texto(c, linhas, x=1300, y=430, size=170, cores=None, inclina=-0.03, alinhamento="c"):
    """texto de thumbnail: Cinzel Bold enorme, contorno preto grosso e sombra. linhas = ["ONDE", "ESTÁ?"]"""
    cores = cores or [(0.98, 0.96, 0.90), (1.0, 0.80, 0.30)]
    c.save(); c.translate(x, y); c.rotate(inclina)
    _bold(c, SERIF)
    yy = 0
    for i, s_ in enumerate(linhas):
        sz = size * (1.0 if i == len(linhas) - 1 else 0.72) if len(linhas) > 1 else size
        c.set_font_size(sz)
        w_ = c.text_extents(s_).x_advance
        tx = -w_ / 2 if alinhamento == "c" else 0
        yy += sz * 0.95
        c.move_to(tx + 8, yy + 10); c.text_path(s_); rgb(c, (0, 0, 0), 0.6); c.fill()
        c.move_to(tx, yy); c.text_path(s_)
        rgb(c, (0.05, 0.03, 0.03)); c.set_line_width(sz * 0.14); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
        rgb(c, cores[min(i, len(cores) - 1)] if i < len(linhas) - 1 or len(cores) == 1 else cores[-1]); c.fill()
    c.restore()


def thumb_selo(c, s, x, y, size=58, col=(0.80, 0.16, 0.12), inclina=-0.05):
    """faixa/selo vermelho com texto curto (ex.: "NUNCA ENCONTRADO", "1959")"""
    _bold(c, SERIF); c.set_font_size(size)
    w_ = c.text_extents(s).x_advance
    c.save(); c.translate(x, y); c.rotate(inclina)
    rr(c, -w_ / 2 - 34 + 6, -size * 0.85 + 8, w_ + 68, size * 1.6, 8); rgb(c, (0, 0, 0), 0.45); c.fill()
    rr(c, -w_ / 2 - 34, -size * 0.85, w_ + 68, size * 1.6, 8); rgb(c, col); c.fill()
    c.move_to(-w_ / 2, size * 0.32); rgb(c, (1, 0.97, 0.92)); c.show_text(s)
    c.restore()


def thumb_versus(c, t, esq, dir_, cor_esq=None, cor_dir=None, fn_esq=None, fn_dir=None, meio="OU", y_rot=250, size=170, y_meio=None):
    """thumbnail de dilema "X ou Y?": tela dividida na diagonal em duas cores, um rótulo enorme em cada lado,
    um objeto opcional em cada lado (fn_esq/fn_dir desenham centrados na origem) e o selo "OU" no meio.
    Combine com thumb_close (o Consultor embaixo, no centro ou num lado) ou com dois personagens em close.
    Deixe o canto inferior direito livre (o YouTube põe a duração ali)."""
    cor_esq = cor_esq or (0.16, 0.44, 0.30)
    cor_dir = cor_dir or (0.62, 0.18, 0.16)
    for pts, col in (([(0, 0), (W / 2 + 90, 0), (W / 2 - 90, H), (0, H)], cor_esq),
                     ([(W / 2 + 90, 0), (W, 0), (W, H), (W / 2 - 90, H)], cor_dir)):
        pg(c, pts); rgb(c, col); c.fill()
    for cx_, col in ((W * 0.25, cor_esq), (W * 0.75, cor_dir)):
        rglow(c, cx_, H * 0.45, 520, lt(col, 0.5), 0.35)
    pg(c, [(W / 2 + 90, 0), (W / 2 + 104, 0), (W / 2 - 76, H), (W / 2 - 90, H)]); rgb(c, (0.98, 0.94, 0.82)); c.fill()
    for fn, cx_ in ((fn_esq, W * 0.25), (fn_dir, W * 0.75)):
        if fn:
            c.save(); c.translate(cx_, H * 0.47); fn(c); c.restore()
    _bold(c, SERIF)
    sz = size
    while sz > 60:
        c.set_font_size(sz)
        if max(c.text_extents(s_).x_advance for s_ in (esq, dir_)) * 1.08 <= W * 0.40:
            break
        sz -= 4
    for txt_, cx_ in ((esq, W * 0.25), (dir_, W * 0.75)):
        thumb_texto(c, [txt_], cx_, y_rot - sz, sz, cores=[(0.98, 0.96, 0.90)], inclina=0)
    if meio:
        c.save(); c.translate(W / 2, y_meio or H * 0.47)
        c.new_sub_path(); c.arc(6, 10, 118, 0, 6.283); rgb(c, (0, 0, 0), 0.45); c.fill()
        c.new_sub_path(); c.arc(0, 0, 118, 0, 6.283); rgb(c, GOLD); c.fill()
        c.new_sub_path(); c.arc(0, 0, 118, 0, 6.283); rgb(c, TINTA); c.set_line_width(12); c.stroke()
        numero_i(c, meio, 0, 4, 96, TINTA, contorno=GOLD)
        c.restore()


LUZES["chave"] = dict(LUZES["dia"], tinta=(1.0, 0.93, 0.84), tk=0.6, dir=1)  # luz de rosto para thumbnails


def thumb_close(c, t, x=420, y=1500, s=2.3, expr="shocked", pose="point_r", look=0.7, lanterna=False, quem=None, **kw):
    """o Historiador em close (cintura para cima), iluminado de frente e com contorno claro para destacar do fundo"""
    global _L
    antes = _L
    _L = LUZES["chave"]
    c.push_group()
    boneco(c, t, x, y, s, poses=((0, pose),), exprs=((0, expr),), look=look, **dict(quem or CONSULTOR_I, **kw))
    pat = c.pop_group()
    _L = antes
    # contorno (halo) deslocando a silhueta em volta
    for dx, dy in ((-10, 0), (10, 0), (0, -10), (0, 10), (-7, -7), (7, 7), (-7, 7), (7, -7)):
        c.save(); c.translate(dx, dy); c.set_source(pat); c.restore()
        c.save(); c.translate(dx, dy); rgb(c, (0.98, 0.94, 0.82)); c.mask(pat); c.restore()
    c.set_source(pat); c.paint()


def salvar_thumb(fn, caminho, tom="normal", t=1.0):
    """renderiza fn(c, t) em 1920x1080 com vinheta suave e salva PNG 1280x720"""
    import os, subprocess
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H); c = cairo.Context(surf)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    fn(c, t)
    vinheta(c, 0.35)
    # contraste extra para miniatura pequena
    c.set_operator(cairo.OPERATOR_SOFT_LIGHT); c.set_source_rgba(0.5, 0.5, 0.5, 0.0); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
    big = caminho.replace(".png", "_1080.png")
    surf.write_to_png(big)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", big, "-vf", "scale=1280:720:flags=lanczos,eq=contrast=1.08:saturation=1.12",
                    caminho], check=True)
    os.remove(big)
    return caminho


# ================================================================ FAZ A CONTA: personagem, números, telas e cenários
V = VERTICAL
CHAO = 1300 if V else 880          # linha do chão padrão (pés dos personagens um pouco abaixo)
CX = W / 2
VERDE = (0.18, 0.62, 0.36)
VERMELHO = (0.86, 0.26, 0.22)
CREME = (0.98, 0.95, 0.88)
TINTA = (0.07, 0.08, 0.12)

CONSULTOR_I = dict(roupa="camisa", cor_roupa=NAVY, cor_calca=(0.20, 0.20, 0.24), gravata=GOLD, oculos="ret",
                   cabelo="curto", cor_cabelo=(0.30, 0.20, 0.13), pele="clara", fid=0)

# segundo personagem e figurantes modernos (passe com **PESSOAS["ana"])
PESSOAS = dict(
    ana=dict(roupa="camisa", cor_roupa=PURPLE, cor_calca=(0.22, 0.24, 0.36), cabelo="longo", mulher=True, cor_cabelo="castanho", pele="media", fid=3),
    bruno=dict(roupa="camisa", cor_roupa=BLUE, cor_calca=(0.26, 0.24, 0.22), cabelo="curto", cor_cabelo="preto", pele="morena", fid=4),
    carla=dict(roupa="camisa", cor_roupa=(0.86, 0.40, 0.36), cor_calca=(0.20, 0.22, 0.30), cabelo="coque", mulher=True, cor_cabelo="ruivo", fid=5),
    diego=dict(roupa="jaqueta", cor_roupa=(0.30, 0.46, 0.34), cor_calca=(0.22, 0.22, 0.26), cabelo="curto", cor_cabelo="preto", pele="escura", barba="curta", fid=6),
    lucas=dict(roupa="camisa", cor_roupa=ORANGE, cor_calca=(0.24, 0.28, 0.40), cabelo="cacheado", cor_cabelo="castanho", pele="media", fid=7),
    aposentado=dict(roupa="camisa", cor_roupa=(0.62, 0.58, 0.50), cor_calca=(0.36, 0.32, 0.28), cabelo="calvo", idade=0.9, oculos=True, bigode=True, fid=8),
    gerente=dict(roupa="casaco", cor_roupa=(0.22, 0.22, 0.26), gravata=(0.62, 0.14, 0.14), cabelo="curto", cor_cabelo="preto", fid=9),
    vendedor=dict(roupa="camisa", cor_roupa=(0.86, 0.24, 0.20), cor_calca=(0.20, 0.20, 0.24), cabelo="curto", cor_cabelo="loiro", fid=10),
)


def consultor_i(c, t, x, y, s=1.0, poses=((0, "stand"),), exprs=((0, "neutral"),), look=0.4, prop=None, **kw):
    """O Consultor ilustrado: camisa azul-marinho, gravata dourada, óculos retangulares, cabelo de lado.
    prop: None ou ("l"|"r", prop_tablet_i | prop_calc_i | prop_moeda_i | prop_celular_i)"""
    o = dict(CONSULTOR_I)
    o.update(kw)
    if prop:
        o["prop"] = prop
    boneco(c, t, x, y, s, poses=poses, exprs=exprs, look=look, **o)


def pessoa(c, t, x, y, s=1.0, quem="ana", poses=((0, "stand"),), exprs=((0, "neutral"),), look=-0.4, **kw):
    o = dict(PESSOAS[quem]) if isinstance(quem, str) else dict(quem)
    o.update(kw)
    boneco(c, t, x, y, s, poses=poses, exprs=exprs, look=look, **o)


# ---------------------------------------------------------------- objetos na mão (origem = mão)
def prop_calc_i(c, t=0):
    c.save(); c.translate(10, -30)
    rr(c, -28, -44, 56, 88, 8); rgb(c, P(NAVY)); c.fill()
    rr(c, -20, -36, 40, 20, 3); rgb(c, (0.70, 0.88, 0.70)); c.fill()
    for i in range(3):
        for j in range(3):
            rr(c, -20 + i * 14, -8 + j * 14, 11, 10, 2); rgb(c, (0.92, 0.92, 0.9) if (i, j) != (2, 2) else GOLD); c.fill()
    c.restore()


def prop_tablet_i(c, t=0):
    c.save(); c.translate(14, -46); c.rotate(-0.12)
    rr(c, -50, -66, 100, 132, 10); rgb(c, (0.12, 0.12, 0.14)); c.fill()
    rr(c, -42, -56, 84, 112, 5); rgb(c, (0.97, 0.97, 0.95)); c.fill()
    c.move_to(-34, 40)
    for i in range(21):
        k = i / 20; c.line_to(-34 + 68 * k, 40 - 80 * k ** 2.2)
    rgb(c, VERDE); c.set_line_width(5); c.stroke()
    c.restore()


def prop_moeda_i(c, t=0):
    c.save(); c.translate(0, -26); moeda_i(c, 26); c.restore()


def prop_celular_i(c, t=0):
    c.save(); c.translate(8, -40)
    rr(c, -24, -46, 48, 92, 8); rgb(c, (0.10, 0.10, 0.12)); c.fill()
    rr(c, -19, -38, 38, 74, 4); rgb(c, (0.85, 0.92, 1.0)); c.fill()
    c.rectangle(-19, -38, 38, 16); rgb(c, NAVY); c.fill()
    c.restore()


# ---------------------------------------------------------------- números
def brl(v, casas=0, prefixo="R$ "):
    """formata em reais: brl(1234567) -> 'R$ 1.234.567'"""
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("- " if v < 0 else "") + prefixo + s


def numero_i(c, s, x, y, size=120, col=GOLD, contorno=TINTA, alinhamento="c", alpha=1.0, inclina=0.0, font=None):
    """número/texto de impacto: Permanent Marker com contorno grosso e sombra"""
    c.save(); c.translate(x, y); c.rotate(inclina)
    c.select_font_face(font or MARKER); c.set_font_size(size)
    e = c.text_extents(s)
    tx = -e.x_advance / 2 if alinhamento == "c" else (-e.x_advance if alinhamento == "r" else 0)
    ty = size * 0.36
    if alpha < 1:
        c.push_group()
    c.move_to(tx + size * 0.04, ty + size * 0.06); c.text_path(s); rgb(c, (0, 0, 0), 0.30); c.fill()
    c.move_to(tx, ty); c.text_path(s)
    rgb(c, contorno); c.set_line_width(size * 0.13); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke_preserve()
    rgb(c, col); c.fill()
    if alpha < 1:
        c.pop_group_to_source(); c.paint_with_alpha(alpha)
    c.restore()
    return e.x_advance


def contador(c, t, t0, v0, v1, x, y, size=140, d=1.6, col=VERDE, fmt=None, casas=0, prefixo="R$ ", sufixo=""):
    """número que conta de v0 até v1 a partir de t0 (com pulo no fim)"""
    if t < t0:
        return
    p = ease_out(prog(t, t0, d))
    v = v0 + (v1 - v0) * p
    s = fmt(v) if fmt else brl(v, casas, prefixo) + sufixo
    pop = 1 + 0.10 * math.sin(clamp01((t - t0 - d) / 0.25) * math.pi) if t > t0 + d else 1
    c.save(); c.translate(x, y); c.scale(pop, pop)
    numero_i(c, s, 0, 0, size, col)
    c.restore()


def entra(c, t, t0, x, y, fn, d=0.45, anim="pop", t1=None):
    """atalho para show() do engine: fn(c) desenhado em (x, y) a partir de t0"""
    show(c, t, t0, x, y, fn, anim=anim, d=d, t1=t1)


# ---------------------------------------------------------------- dinheiro
NOTAS = {"2": (0.42, 0.58, 0.76), "5": (0.62, 0.46, 0.66), "10": (0.80, 0.36, 0.30), "20": (0.92, 0.74, 0.30),
         "50": (0.80, 0.56, 0.32), "100": (0.40, 0.62, 0.78), "200": (0.62, 0.62, 0.60)}


def moeda_i(c, r=40, depth=0.0):
    c.new_sub_path(); c.arc(0, 4, r, 0, 6.283); rgb(c, P(dk(GOLD, 0.3), depth)); c.fill()
    c.new_sub_path(); c.arc(0, 0, r, 0, 6.283); rgb(c, P(GOLD, depth)); c.fill()
    c.new_sub_path(); c.arc(0, 0, r * 0.76, 0, 6.283); rgb(c, P(dk(GOLD, 0.12), depth)); c.set_line_width(r * 0.08); c.stroke()
    c.select_font_face(MARKER); c.set_font_size(r * 0.8)
    w_ = c.text_extents("R$").x_advance
    c.move_to(-w_ / 2, r * 0.28); rgb(c, P(dk(GOLD, 0.35), depth)); c.show_text("R$")


def pilha_moedas(c, n=6, r=40, t=None, t0=0, d=0.08):
    """pilha de moedas (origem = base). Com t, as moedas caem uma a uma a partir de t0"""
    for i in range(n):
        y = -i * r * 0.32
        if t is not None:
            ti = t0 + i * d
            if t < ti:
                break
            y -= (1 - ease_out(prog(t, ti, 0.25))) * 160
        c.save(); c.translate(0, y); c.scale(1, 0.32)
        c.new_sub_path(); c.arc(0, 10, r, 0, 6.283); rgb(c, P(dk(GOLD, 0.35))); c.fill()
        c.new_sub_path(); c.arc(0, 0, r, 0, 6.283); rgb(c, P(GOLD)); c.fill()
        c.restore()


def nota_i(c, valor="100", w=240, depth=0.0):
    col = P(NOTAS.get(str(valor), NOTAS["100"]), depth)
    h = w * 0.5
    rr(c, -w / 2, -h / 2, w, h, 8); rgb(c, col); c.fill()
    rr(c, -w / 2 + 10, -h / 2 + 10, w - 20, h - 20, 5); rgb(c, lt(col, 0.35)); c.set_line_width(3); c.stroke()
    c.new_sub_path(); c.arc(-w * 0.18, 0, h * 0.28, 0, 6.283); rgb(c, lt(col, 0.3)); c.fill()
    c.select_font_face(MARKER); c.set_font_size(h * 0.42)
    w_ = c.text_extents(str(valor)).x_advance
    c.move_to(w * 0.30 - w_ / 2, h * 0.16); rgb(c, dk(col, 0.45)); c.show_text(str(valor))


def maco(c, valor="100", n=6, w=240):
    """maço de notas empilhadas (origem = centro da de cima)"""
    for i in range(n - 1, -1, -1):
        c.save(); c.translate(i * 3, i * 6); c.rotate((i % 3 - 1) * 0.02); nota_i(c, valor, w); c.restore()
    c.rectangle(-16, -w * 0.25, 32, w * 0.5); rgb(c, (0.92, 0.88, 0.78)); c.fill()


def chuva_dinheiro(c, t, t0, n=24, seed=1, area=None, area_y=None):
    """notas e moedas caindo pela tela a partir de t0 (comemoração). area=(x0, x1); area_y = de onde caem"""
    if t < t0:
        return
    rnd = random.Random(seed)
    x0, x1 = area or (0, W)
    for i in range(n):
        x = rnd.uniform(x0, x1); sp = rnd.uniform(260, 460); ph = rnd.uniform(0, 6.28)
        y = (area_y or -120) + (t - t0 - rnd.uniform(0, 1.2)) * sp
        if y < -120 or y > H + 100:
            continue
        c.save(); c.translate(x + math.sin(t * 2 + ph) * 30, y); c.rotate(math.sin(t * 3 + ph) * 0.6)
        if i % 3:
            nota_i(c, rnd.choice(["50", "100", "200"]), 150)
        else:
            moeda_i(c, 26)
        c.restore()


# ---------------------------------------------------------------- telas e papéis
def celular_app(c, t, x, y, s=1.0, titulo="Saldo investido", valor="R$ 1 MILHÃO", sub="", curva=None, linhas=None,
                cor=NAVY, t0=None, d=1.8):
    """celular com app de banco: cabeçalho (titulo + valor), gráfico que cresce (curva = função 0..1 -> 0..1)
    ou linhas de extrato [("Mercado", "- R$ 640", VERMELHO), ...]. Com t0, o gráfico/linhas se desenham a partir dele."""
    p = 1.0 if t0 is None else ease_io(prog(t, t0, d))
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -160 + 12, -310 + 16, 320, 620, 44); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, -160, -310, 320, 620, 44); rgb(c, (0.10, 0.10, 0.12)); c.fill()
    rr(c, -144, -282, 288, 564, 28); rgb(c, (0.97, 0.97, 0.95)); c.fill()
    c.save(); rr(c, -144, -282, 288, 564, 28); c.clip()
    c.rectangle(-144, -282, 288, 160); rgb(c, cor); c.fill()
    c.select_font_face(HAND); c.set_font_size(28); c.move_to(-118, -226); rgb(c, (1, 1, 1), 0.8); c.show_text(titulo)
    c.select_font_face(MARKER)
    fs_ = 52
    c.set_font_size(fs_)
    while c.text_extents(valor).x_advance > 250 and fs_ > 22:
        fs_ -= 2; c.set_font_size(fs_)
    c.move_to(-118, -158); rgb(c, (1, 1, 1)); c.show_text(valor)
    if linhas:
        for i, (lab, val, col) in enumerate(linhas):
            if (i + 1) / len(linhas) > p + 1e-6:
                break
            yy = -80 + i * 62
            c.new_sub_path(); c.arc(-106, yy - 8, 15, 0, 6.283); rgb(c, lt(col, 0.6)); c.fill()
            c.select_font_face(HAND); c.set_font_size(25); c.move_to(-78, yy); rgb(c, (0.2, 0.2, 0.24)); c.show_text(lab)
            c.select_font_face(MARKER); c.set_font_size(21)
            ww = c.text_extents(val).x_advance
            c.move_to(122 - ww, yy); rgb(c, col); c.show_text(val)
            c.rectangle(-122, yy + 20, 244, 1.5); rgb(c, (0.85, 0.85, 0.85)); c.fill()
    else:
        f = curva or (lambda k: k ** 2.6)
        n = max(2, int(60 * p))
        pts = [(-118 + 236 * (i / 60), 170 - 250 * f(i / 60)) for i in range(n + 1)]
        c.move_to(pts[0][0], 180)
        for px, py in pts:
            c.line_to(px, py)
        c.line_to(pts[-1][0], 180); c.close_path()
        lgrad(c, 0, -80, 0, 180, [(0, VERDE, 0.35), (1, VERDE, 0.02)]); c.fill()
        c.move_to(*pts[0])
        for px, py in pts[1:]:
            c.line_to(px, py)
        rgb(c, VERDE); c.set_line_width(7); c.stroke()
        c.new_sub_path(); c.arc(*pts[-1], 10, 0, 6.283); rgb(c, VERDE); c.fill()
        if sub:
            c.select_font_face(HAND); c.set_font_size(28)
            ww = c.text_extents(sub).x_advance
            c.move_to(-ww / 2, 236); rgb(c, (0.35, 0.35, 0.4)); c.show_text(sub)
    c.restore()
    rr(c, -40, -300, 80, 14, 7); rgb(c, (0.10, 0.10, 0.12)); c.fill()
    c.restore()


def notificacao(c, x, y, s=1.0, titulo="Consignado liberado!", texto="toque para aceitar", cor=VERDE, app="BANCO"):
    c.save(); c.translate(x, y); c.scale(s, s)
    rr(c, -300 + 8, -70 + 10, 600, 140, 26); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, -300, -70, 600, 140, 26); rgb(c, (0.99, 0.99, 0.98)); c.fill()
    rr(c, -276, -46, 92, 92, 20); rgb(c, cor); c.fill()
    c.select_font_face(MARKER); c.set_font_size(52); c.move_to(-252, 18); rgb(c, (1, 1, 1)); c.show_text("$")
    c.select_font_face(HAND); c.set_font_size(24); c.move_to(-164, -28); rgb(c, (0.5, 0.5, 0.55)); c.show_text(app + " · agora")
    c.select_font_face(MARKER); c.set_font_size(34); c.move_to(-164, 12); rgb(c, TINTA); c.show_text(titulo)
    c.select_font_face(HAND); c.set_font_size(26); c.move_to(-164, 46); rgb(c, (0.4, 0.4, 0.45)); c.show_text(texto)
    c.restore()


def papel(c, w, h, cor=(0.99, 0.98, 0.95), rot=-0.02):
    c.rotate(rot)
    rr(c, -w / 2 + 10, -h / 2 + 14, w, h, 10); rgb(c, (0, 0, 0), 0.22); c.fill()
    rr(c, -w / 2, -h / 2, w, h, 10); rgb(c, cor); c.fill()


def fatura(c, t, x, y, s=1.0, itens=(("Mercado", "R$ 640"), ("Delivery", "R$ 310"), ("Parcela TV", "R$ 290")),
           total="R$ 2.380", vence="Vence dia 10", minimo=None, t0=None):
    """fatura do cartão: itens entram um a um a partir de t0; total em vermelho"""
    c.save(); c.translate(x, y); c.scale(s, s)
    h = 200 + len(itens) * 60 + (70 if minimo else 0)
    papel(c, 520, h)
    c.rectangle(-260, -h / 2, 520, 86); rgb(c, NAVY); c.fill()
    c.select_font_face(MARKER); c.set_font_size(36); c.move_to(-230, -h / 2 + 56); rgb(c, (1, 1, 1)); c.show_text("FATURA DO CARTÃO")
    for i, (lab, val) in enumerate(itens):
        if t0 is not None and t < t0 + i * 0.35:
            break
        yy = -h / 2 + 140 + i * 60
        c.select_font_face(HAND); c.set_font_size(34); c.move_to(-220, yy); rgb(c, (0.25, 0.25, 0.3)); c.show_text(lab)
        ww = c.text_extents(val).x_advance; c.move_to(220 - ww, yy); c.show_text(val)
        c.rectangle(-220, yy + 16, 440, 2); rgb(c, (0.85, 0.85, 0.85)); c.fill()
    yy = h / 2 - (110 if minimo else 46)
    c.select_font_face(HAND); c.set_font_size(30); c.move_to(-220, yy); rgb(c, (0.4, 0.4, 0.45)); c.show_text(vence)
    c.select_font_face(MARKER); c.set_font_size(54); ww = c.text_extents(total).x_advance
    c.move_to(220 - ww, yy + 6); rgb(c, VERMELHO); c.show_text(total)
    if minimo:
        rr(c, -220, h / 2 - 80, 440, 56, 10); rgb(c, (1.0, 0.92, 0.70)); c.fill()
        c.select_font_face(HAND); c.set_font_size(30); c.move_to(-200, h / 2 - 42); rgb(c, (0.45, 0.3, 0.1)); c.show_text("Pagamento mínimo: " + minimo)
    c.restore()


def contracheque(c, x, y, s=1.0, bruto="R$ 3.000", descontos=(("INSS", "- R$ 253"), ("IR", "- R$ 41")), liquido="R$ 2.706"):
    c.save(); c.translate(x, y); c.scale(s, s)
    h = 260 + len(descontos) * 56
    papel(c, 500, h, rot=0.02)
    c.select_font_face(MARKER); c.set_font_size(34); c.move_to(-210, -h / 2 + 60); rgb(c, NAVY); c.show_text("CONTRACHEQUE")
    rows = [("Salário bruto", bruto, (0.25, 0.25, 0.3))] + [(a, b, VERMELHO) for a, b in descontos]
    for i, (a, b, col) in enumerate(rows):
        yy = -h / 2 + 120 + i * 56
        c.select_font_face(HAND); c.set_font_size(32); c.move_to(-210, yy); rgb(c, (0.3, 0.3, 0.35)); c.show_text(a)
        ww = c.text_extents(b).x_advance; c.move_to(210 - ww, yy); rgb(c, col); c.show_text(b)
    c.rectangle(-210, h / 2 - 90, 420, 3); rgb(c, NAVY); c.fill()
    c.select_font_face(HAND); c.set_font_size(32); c.move_to(-210, h / 2 - 40); rgb(c, (0.3, 0.3, 0.35)); c.show_text("Líquido")
    c.select_font_face(MARKER); c.set_font_size(46); ww = c.text_extents(liquido).x_advance
    c.move_to(210 - ww, h / 2 - 36); rgb(c, VERDE); c.show_text(liquido)
    c.restore()


def etiqueta_preco(c, valor, cor=GOLD, size=46, riscado=None):
    """etiqueta de preço pendurada (origem = furo)"""
    c.select_font_face(MARKER); c.set_font_size(size)
    w_ = c.text_extents(valor).x_advance + 60
    h = size * 1.5 + (size * 1.0 if riscado else 0)
    pg(c, [(0, 0), (w_ * 0.18, -h / 2), (w_, -h / 2), (w_, h / 2), (w_ * 0.18, h / 2)])
    rgb(c, (0, 0, 0), 0.2); c.save(); c.translate(6, 8); c.fill(); c.restore()
    pg(c, [(0, 0), (w_ * 0.18, -h / 2), (w_, -h / 2), (w_, h / 2), (w_ * 0.18, h / 2)]); rgb(c, cor); c.fill()
    c.new_sub_path(); c.arc(w_ * 0.14, 0, 7, 0, 6.283); rgb(c, (1, 1, 1)); c.fill()
    if riscado:
        c.set_font_size(size * 0.5); c.move_to(w_ * 0.26, -h / 2 + size * 0.62); rgb(c, (0.3, 0.2, 0.1)); c.show_text(riscado)
        rw = c.text_extents(riscado).x_advance
        c.rectangle(w_ * 0.25, -h / 2 + size * 0.45, rw + 4, 4); rgb(c, TINTA); c.fill()
    c.set_font_size(size); c.move_to(w_ * 0.26, h / 2 - size * 0.30); rgb(c, TINTA); c.show_text(valor)


# ---------------------------------------------------------------- gráficos animados
def grafico_curva(c, t, t0, x, y, w=900, h=480, f=None, d=2.4, cor=VERDE, eixo_x=("hoje", "35 anos"), marcas=(),
                  valor_fim=None, fundo=True):
    """curva de juros compostos que se desenha (origem = canto inferior esquerdo). marcas = [(k, "texto"), ...]"""
    f = f or (lambda k: k ** 2.6)
    p = ease_io(prog(t, t0, d)) if t >= t0 else 0
    if fundo:
        rr(c, x - 50, y - h - 50, w + 100, h + 120, 24); rgb(c, (1, 1, 1), 0.85); c.fill()
    for k in range(1, 5):
        c.rectangle(x, y - h * k / 4, w, 2); rgb(c, (0.85, 0.86, 0.88)); c.fill()
    c.rectangle(x, y, w, 4); rgb(c, (0.4, 0.4, 0.45)); c.fill()
    c.select_font_face(HAND); c.set_font_size(30); rgb(c, (0.4, 0.4, 0.45))
    c.move_to(x, y + 40); c.show_text(eixo_x[0])
    ww = c.text_extents(eixo_x[1]).x_advance; c.move_to(x + w - ww, y + 40); c.show_text(eixo_x[1])
    if p <= 0:
        return
    n = max(2, int(120 * p))
    pts = [(x + w * (i / 120), y - h * f(i / 120)) for i in range(n + 1)]
    c.move_to(x, y)
    for px, py in pts:
        c.line_to(px, py)
    c.line_to(pts[-1][0], y); c.close_path()
    lgrad(c, 0, y - h, 0, y, [(0, cor, 0.40), (1, cor, 0.04)]); c.fill()
    c.move_to(*pts[0])
    for px, py in pts[1:]:
        c.line_to(px, py)
    rgb(c, cor); c.set_line_width(9); c.stroke()
    c.new_sub_path(); c.arc(*pts[-1], 14, 0, 6.283); rgb(c, cor); c.fill()
    c.new_sub_path(); c.arc(*pts[-1], 6, 0, 6.283); rgb(c, (1, 1, 1)); c.fill()
    for k, s_ in marcas:
        if p >= k:
            mx, my = x + w * k, y - h * f(k)
            c.new_sub_path(); c.arc(mx, my, 10, 0, 6.283); rgb(c, GOLD); c.fill()
            c.select_font_face(MARKER); c.set_font_size(32); ww = c.text_extents(s_).x_advance
            c.move_to(mx - ww / 2, my - 26); rgb(c, TINTA); c.show_text(s_)
    if valor_fim and p >= 0.999:
        numero_i(c, valor_fim, x + w, y - h - 70, 64, cor, alinhamento="r")


def barras_i(c, t, t0, x, y, w=800, h=460, dados=(("Ana", 372000, PURPLE), ("Bruno", 228000, BLUE)), fmt=brl,
             d=1.4, maxv=None, intervalo=0.5, size_val=54):
    """barras que crescem com o valor contando em cima (origem = canto inferior esquerdo)"""
    maxv = maxv or max(v for _, v, _ in dados)
    n = len(dados)
    bw = w / n * 0.62
    c.rectangle(x - 20, y, w + 40, 5); rgb(c, (0.3, 0.3, 0.35)); c.fill()
    for i, (lab, v, col) in enumerate(dados):
        ti = t0 + i * intervalo
        cx_ = x + w * (i + 0.5) / n
        c.select_font_face(MARKER); c.set_font_size(40); ww = c.text_extents(lab).x_advance
        c.move_to(cx_ - ww / 2, y + 56); rgb(c, dk(col, 0.2)); c.show_text(lab)
        if t < ti:
            continue
        p = ease_out(prog(t, ti, d))
        bh = h * v / maxv * p
        rr(c, cx_ - bw / 2, y - bh, bw, bh + 4, 12); rgb(c, P(col)); c.fill()
        c.rectangle(cx_ + bw * 0.18, y - bh + 10, bw * 0.32 - 12, max(0, bh - 10)); rgb(c, (0, 0, 0), 0.10); c.fill()
        numero_i(c, fmt(v * p), cx_, y - bh - size_val * 0.75, size_val, col if col != NAVY else GOLD)


def rosca_i(c, t, t0, x, y, r=200, pct=0.35, cor=VERMELHO, fundo=(0.88, 0.88, 0.86), texto=None, d=1.2):
    """rosca (donut) que se preenche até pct, com a porcentagem no centro"""
    p = ease_out(prog(t, t0, d)) if t >= t0 else 0
    c.set_line_cap(cairo.LINE_CAP_BUTT)
    c.new_sub_path(); c.arc(x, y, r, 0, 6.283); rgb(c, fundo); c.set_line_width(r * 0.36); c.stroke()
    if p > 0:
        c.new_sub_path(); c.arc(x, y, r, -math.pi / 2, -math.pi / 2 + 6.283 * pct * p); rgb(c, cor); c.stroke()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    numero_i(c, texto or f"{round(pct * 100 * p)}%", x, y, r * 0.55, cor)


# ---------------------------------------------------------------- fundos de marca (cenas de número e gráfico)
def fundo_marca(c, t, cor="creme", padrao=True, holofote=None):
    """fundo limpo para cenas de número/gráfico: creme (padrão), navy, verde (ganho) ou vermelho (perda).
    holofote=(x, y): luz clara atrás do personagem (use no navy, onde a camisa do Consultor some)"""
    cores = {"creme": ((0.99, 0.96, 0.89), (0.95, 0.88, 0.76)), "navy": ((0.18, 0.26, 0.46), (0.08, 0.12, 0.24)),
             "verde": ((0.22, 0.58, 0.40), (0.10, 0.34, 0.24)), "vermelho": ((0.76, 0.28, 0.24), (0.42, 0.12, 0.12))}
    a, b = cores[cor]
    g = cairo.RadialGradient(W / 2, H * 0.4, 50, W / 2, H * 0.5, max(W, H) * 0.8)
    g.add_color_stop_rgb(0, *a); g.add_color_stop_rgb(1, *b); c.set_source(g); c.paint()
    if padrao:
        rnd = random.Random(3)
        escuro = cor != "creme"
        for i in range(18):
            x0, y0, rr_, ph = rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(18, 46), rnd.uniform(0, 6.28)
            yy = (y0 - t * 12) % (H + 100) - 50
            xx = x0 + math.sin(t * 0.4 + ph) * 20
            c.new_sub_path(); c.arc(xx, yy, rr_, 0, 6.283)
            rgb(c, (1, 1, 1) if escuro else (0.85, 0.66, 0.30), 0.06 if escuro else 0.10); c.fill()
    if holofote:
        hx, hy = holofote
        rglow(c, hx, hy, 520, (1.0, 0.94, 0.80), 0.55)
        ellipse(c, hx, hy + 330, 220, 34); rgb(c, (1, 1, 1), 0.18); c.fill()


# ---------------------------------------------------------------- móveis e objetos de cenário (origem = base no centro)
def planta_vaso(c, h=180, depth=0.0):
    rr(c, -34, -70, 68, 70, 8); rgb(c, P((0.80, 0.46, 0.30), depth)); c.fill()
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * 0.32
        c.save(); c.translate(0, -70); c.rotate(a + math.pi / 2)
        ellipse(c, 0, -h * 0.35, 18, h * 0.38); rgb(c, P((0.26, 0.52, 0.32) if i % 2 else (0.20, 0.44, 0.28), depth)); c.fill()
        c.restore()


def sofa_i(c, w=520, cor=(0.36, 0.48, 0.62)):
    col = P(cor)
    rr(c, -w / 2, -260, w, 150, 30); rgb(c, dk(col, 0.1)); c.fill()
    rr(c, -w / 2 + 20, -150, w - 40, 90, 18); rgb(c, col); c.fill()
    for sx in (-1, 1):
        rr(c, sx * w / 2 - (60 if sx > 0 else 0), -200, 60, 150, 24); rgb(c, dk(col, 0.05)); c.fill()
    c.move_to(0, -150); c.line_to(0, -64); rgb(c, dk(col, 0.25)); c.set_line_width(3); c.stroke()
    for sx in (-1, 1):
        c.rectangle(sx * (w / 2 - 40) - 6, -60, 12, 60); rgb(c, P(MADEIRA_ESC)); c.fill()


def tv_i(c, w=420, ligada=True, t=0):
    rr(c, -w / 2, -w * 0.62 - 120, w, w * 0.6, 10); rgb(c, (0.08, 0.08, 0.09)); c.fill()
    rr(c, -w / 2 + 10, -w * 0.62 - 110, w - 20, w * 0.6 - 20, 4)
    rgb(c, (0.30, 0.52, 0.78) if ligada else (0.16, 0.18, 0.20)); c.fill()
    rr(c, -w * 0.6, -110, w * 1.2, 30, 6); rgb(c, P(MADEIRA)); c.fill()
    c.rectangle(-w * 0.55, -80, w * 1.1, 80); rgb(c, P(dk(MADEIRA, 0.15))); c.fill()


def geladeira_i(c, h=520):
    w = h * 0.5
    rr(c, -w / 2, -h, w, h, 18); rgb(c, P((0.90, 0.91, 0.92))); c.fill()
    c.rectangle(-w / 2, -h * 0.64, w, 4); rgb(c, P((0.70, 0.72, 0.74))); c.fill()
    for yy in (-h * 0.86, -h * 0.5):
        rr(c, w / 2 - 34, yy, 10, 70, 5); rgb(c, P((0.55, 0.57, 0.60))); c.fill()
    c.rectangle(w / 2 - 20, -h, 20, h); rgb(c, (0, 0, 0), 0.07); c.fill()


def bancada_i(c, w=900, h=300, cor=(0.92, 0.90, 0.86), tampo=(0.30, 0.30, 0.32), fogao=True):
    c.rectangle(-w / 2, -h, w, h); rgb(c, P(cor)); c.fill()
    for k in range(1, 4):
        c.rectangle(-w / 2 + w * k / 4 - 2, -h + 30, 4, h - 30); rgb(c, P(dk(cor, 0.15))); c.fill()
        rr(c, -w / 2 + w * (k - 0.5) / 4 - 30, -h + 60, 60, 8, 4); rgb(c, P((0.55, 0.55, 0.58))); c.fill()
    c.rectangle(-w / 2 - 14, -h - 26, w + 28, 30); rgb(c, P(tampo)); c.fill()
    if fogao:
        for i in range(2):
            ellipse(c, w * 0.22 + i * 90, -h - 30, 34, 8); rgb(c, P((0.12, 0.12, 0.13))); c.fill()


def armarios_altos(c, w=900, h=220, cor=(0.92, 0.90, 0.86)):
    c.rectangle(-w / 2, -h, w, h); rgb(c, P(cor)); c.fill()
    for k in range(4):
        rr(c, -w / 2 + w * k / 4 + 8, -h + 8, w / 4 - 16, h - 16, 6); rgb(c, P(lt(cor, 0.25))); c.fill()
        rr(c, -w / 2 + w * (k + 0.5) / 4 - 4, -40, 8, 30, 4); rgb(c, P((0.55, 0.55, 0.58))); c.fill()


def prateleira_mercado(c, w=700, h=560, seed=1):
    rnd = random.Random(seed)
    c.rectangle(-w / 2, -h, w, h); rgb(c, P((0.82, 0.84, 0.86))); c.fill()
    cores = [(0.86, 0.26, 0.22), (0.98, 0.76, 0.24), (0.26, 0.52, 0.80), (0.30, 0.66, 0.40), (0.95, 0.55, 0.20),
             (0.62, 0.38, 0.70), (0.96, 0.96, 0.94)]
    rows = 4
    for r in range(rows):
        by = -h + (r + 1) * h / rows - 14
        x = -w / 2 + 12
        while x < w / 2 - 50:
            bw = rnd.uniform(36, 70); bh = rnd.uniform(0.45, 0.75) * h / rows
            col = P(rnd.choice(cores))
            if rnd.random() < 0.3:
                rr(c, x, by - bh, bw - 4, bh, bw * 0.3); rgb(c, col); c.fill()  # garrafa/pote
            else:
                c.rectangle(x, by - bh, bw - 4, bh); rgb(c, col); c.fill()
                c.rectangle(x + 4, by - bh * 0.6, bw - 12, bh * 0.25); rgb(c, lt(col, 0.5)); c.fill()
            x += bw
        c.rectangle(-w / 2, by, w, 14); rgb(c, P((0.62, 0.64, 0.68))); c.fill()
        for k in range(3):
            c.rectangle(-w / 2 + 40 + k * w / 3, by + 2, 50, 12); rgb(c, P(GOLD)); c.fill()


def carrinho_i(c, cheio=0.6):
    col = P((0.62, 0.64, 0.68))
    rnd = random.Random(2)
    for i in range(int(cheio * 9)):
        c.rectangle(-120 + (i % 5) * 46, -230 - (i // 5) * 40 + rnd.uniform(-8, 8), 42, 60)
        rgb(c, P(rnd.choice([(0.86, 0.26, 0.22), (0.98, 0.76, 0.24), (0.26, 0.52, 0.80), (0.30, 0.66, 0.40)]))); c.fill()
    pg(c, [(-150, -260), (140, -260), (110, -110), (-120, -110)])
    rgb(c, col); c.set_line_width(8); c.stroke()
    for k in range(1, 5):
        c.move_to(-150 + k * 58, -260); c.line_to(-120 + k * 46, -110); c.set_line_width(3); c.stroke()
    c.move_to(140, -260); c.line_to(190, -300); c.set_line_width(8); c.stroke()
    c.move_to(-120, -110); c.line_to(-110, -60); c.line_to(110, -60); c.stroke()
    for xx in (-90, 90):
        c.new_sub_path(); c.arc(xx, -26, 24, 0, 6.283); rgb(c, (0.15, 0.15, 0.16)); c.fill()


def carro_i(c, t=0, cor=(0.86, 0.26, 0.22), anda=False):
    """carro moderno de lado (origem = chão no centro)"""
    col = P(cor)
    c.move_to(-230, -50); c.line_to(-230, -110); c.curve_to(-220, -130, -170, -134, -130, -136)
    c.line_to(-80, -196); c.curve_to(-60, -210, 70, -210, 100, -196); c.line_to(160, -140)
    c.curve_to(210, -136, 236, -120, 236, -90); c.line_to(236, -50); c.close_path(); rgb(c, col); c.fill()
    pg(c, [(-110, -138), (-70, -186), (10, -186), (10, -138)]); rgb(c, P((0.70, 0.84, 0.94))); c.fill()
    pg(c, [(26, -138), (26, -186), (90, -186), (136, -138)]); c.fill()
    c.rectangle(-230, -84, 466, 8); rgb(c, dk(col, 0.25)); c.fill()
    rr(c, 210, -110, 26, 16, 5); rgb(c, (1.0, 0.92, 0.6)); c.fill()
    for xx in (-140, 140):
        c.new_sub_path(); c.arc(xx, -46, 46, 0, 6.283); rgb(c, (0.12, 0.12, 0.13)); c.fill()
        c.new_sub_path(); c.arc(xx, -46, 20, 0, 6.283); rgb(c, (0.70, 0.72, 0.74)); c.fill()
        if anda:
            a = t * 12
            c.move_to(xx + math.cos(a) * 20, -46 + math.sin(a) * 20); c.line_to(xx - math.cos(a) * 20, -46 - math.sin(a) * 20)
            rgb(c, (0.4, 0.4, 0.42)); c.set_line_width(4); c.stroke()


def predio_moderno(c, x, y, w=300, h=700, cor=(0.62, 0.66, 0.72), depth=0.0, seed=1):
    rnd = random.Random(seed)
    base = P(cor, depth)
    c.rectangle(x, y - h, w, h); rgb(c, base); c.fill()
    cols, rows = max(2, int(w / 60)), max(3, int(h / 70))
    for i in range(cols):
        for j in range(rows):
            acesa = _L["noite"] and rnd.random() < 0.45
            c.rectangle(x + 16 + i * (w - 32) / cols, y - h + 20 + j * (h - 40) / rows, (w - 32) / cols - 12, (h - 40) / rows - 16)
            rgb(c, JANELA_ACESA if acesa else P(mix((0.55, 0.70, 0.84), _L["fora"], 0.3), depth)); c.fill()
    c.rectangle(x + w - 26, y - h, 26, h); rgb(c, (0, 0, 0), 0.10); c.fill()


def poste_i(c, h=420):
    c.rectangle(-6, -h, 12, h); rgb(c, P((0.24, 0.24, 0.26))); c.fill()
    c.move_to(0, -h); c.curve_to(0, -h - 40, 60, -h - 40, 70, -h - 20); rgb(c, P((0.24, 0.24, 0.26))); c.set_line_width(10); c.stroke()
    ellipse(c, 70, -h - 12, 26, 10); rgb(c, JANELA_ACESA if _L["noite"] else P((0.85, 0.85, 0.8))); c.fill()
    if _L["noite"]:
        rglow(c, 70, -h, 260, JANELA_ACESA, 0.25)


def janela_cidade(c, x, y, w=420, h=360, seed=4):
    """janela com vista da cidade (dia/noite segue a luz)"""
    c.rectangle(x - 14, y - 14, w + 28, h + 28); rgb(c, P((0.95, 0.95, 0.94))); c.fill()
    c.save(); c.rectangle(x, y, w, h); c.clip()
    lgrad(c, 0, y, 0, y + h, [(0, _L["ceu"][0], 1), (1, _L["ceu"][1], 1)]); c.paint()
    rnd = random.Random(seed)
    xx = x - 20
    while xx < x + w:
        bw = rnd.uniform(50, 110); bh = rnd.uniform(0.3, 0.8) * h
        c.rectangle(xx, y + h - bh, bw - 6, bh); rgb(c, P((0.52, 0.58, 0.68), 0.4)); c.fill()
        for k in range(int(bh / 26)):
            if _L["noite"] and rnd.random() < 0.5:
                c.rectangle(xx + 8, y + h - bh + 10 + k * 26, 10, 12); rgb(c, JANELA_ACESA); c.fill()
        xx += bw
    c.restore()
    c.rectangle(x + w / 2 - 5, y, 10, h); rgb(c, P((0.95, 0.95, 0.94))); c.fill()


def balcao_i(c, w=900, h=260, cor=(0.55, 0.38, 0.24), vidro=False, seed=1):
    """balcão de padaria/loja; vidro=True vira vitrine com doces e pães"""
    col = P(cor)
    if vidro:
        rr(c, -w / 2, -h - 170, w, 170, 14); rgb(c, (0.85, 0.93, 0.98), 0.55); c.fill()
        rnd = random.Random(seed)
        for i in range(10):
            xx = -w / 2 + 50 + i * (w - 100) / 9
            ellipse(c, xx, -h - 40, 34, 18)
            rgb(c, P(rnd.choice([(0.82, 0.56, 0.28), (0.92, 0.80, 0.56), (0.62, 0.36, 0.22), (0.96, 0.70, 0.70)]))); c.fill()
        c.rectangle(-w / 2, -h - 100, w, 4); rgb(c, (1, 1, 1), 0.6); c.fill()
    c.rectangle(-w / 2, -h, w, h); rgb(c, col); c.fill()
    c.rectangle(-w / 2 - 10, -h - 10, w + 20, 18); rgb(c, dk(col, 0.25)); c.fill()
    for k in range(5):
        c.rectangle(-w / 2 + 20 + k * (w - 40) / 5, -h + 30, (w - 40) / 5 - 20, h - 60); rgb(c, dk(col, 0.10)); c.fill()


def placa_preco(c, linhas=(("CAFÉ", "R$ 6"), ("PÃO", "R$ 4")), w=420):
    """quadro-negro de cardápio (origem = centro)"""
    h = 90 + len(linhas) * 66
    rr(c, -w / 2 - 14, -h / 2 - 14, w + 28, h + 28, 10); rgb(c, P(MADEIRA)); c.fill()
    c.rectangle(-w / 2, -h / 2, w, h); rgb(c, (0.16, 0.20, 0.18)); c.fill()
    for i, (a, b) in enumerate(linhas):
        yy = -h / 2 + 76 + i * 66
        c.select_font_face(MARKER); fz = 42; c.set_font_size(fz)
        while c.text_extents(a + b).x_advance > w - 100 and fz > 20:
            fz -= 2; c.set_font_size(fz)
        c.move_to(-w / 2 + 30, yy); rgb(c, (0.95, 0.95, 0.9)); c.show_text(a)
        ww = c.text_extents(b).x_advance; c.move_to(w / 2 - 30 - ww, yy); rgb(c, GOLD); c.show_text(b)


def luminaria(c, x, y_teto=0, L=200, acesa=True):
    c.rectangle(x - 2, y_teto, 4, L); rgb(c, P((0.2, 0.2, 0.22))); c.fill()
    pg(c, [(x - 50, y_teto + L + 40), (x - 18, y_teto + L), (x + 18, y_teto + L), (x + 50, y_teto + L + 40)])
    rgb(c, P((0.18, 0.30, 0.26))); c.fill()
    if acesa:
        rglow(c, x, y_teto + L + 50, 220, JANELA_ACESA, 0.22)


def caixa_eletronico(c):
    rr(c, -110, -420, 220, 420, 14); rgb(c, P((0.70, 0.72, 0.76))); c.fill()
    rr(c, -80, -380, 160, 120, 8); rgb(c, (0.20, 0.42, 0.66)); c.fill()
    c.rectangle(-60, -230, 120, 70); rgb(c, P((0.55, 0.57, 0.60))); c.fill()
    c.rectangle(-50, -130, 100, 10); rgb(c, (0.15, 0.15, 0.16)); c.fill()


def mesa_trabalho(c, w=520, monitor=True, t=0):
    c.rectangle(-w / 2, -190, w, 20); rgb(c, P((0.90, 0.88, 0.84))); c.fill()
    for sx in (-1, 1):
        c.rectangle(sx * (w / 2 - 20) - 5, -170, 10, 170); rgb(c, P((0.35, 0.35, 0.38))); c.fill()
    if monitor:
        rr(c, -130, -400, 260, 170, 8); rgb(c, (0.12, 0.12, 0.14)); c.fill()
        rr(c, -120, -390, 240, 150, 4); rgb(c, (0.88, 0.94, 0.98)); c.fill()
        for k in range(4):
            c.rectangle(-100, -370 + k * 32, 120 + 40 * ((k * 3) % 2), 12); rgb(c, (0.55, 0.65, 0.80)); c.fill()
        c.rectangle(-8, -230, 16, 40); rgb(c, (0.2, 0.2, 0.22)); c.fill()


# ---------------------------------------------------------------- paredes e chão
def _sala(c, parede=(0.90, 0.86, 0.78), piso=(0.62, 0.46, 0.32), chao=None, rodape=True, tipo_piso="madeira"):
    chao = chao or CHAO
    c.rectangle(0, 0, W, chao); rgb(c, P(parede)); c.fill()
    lgrad(c, 0, 0, 0, chao, [(0, (1, 1, 1), 0.10), (1, (0, 0, 0), 0.06)]); c.rectangle(0, 0, W, chao); c.fill()
    pcol = P(piso)
    lgrad(c, 0, chao, 0, H, [(0, pcol, 1), (1, dk(pcol, 0.25), 1)]); c.rectangle(0, chao, W, H - chao); c.fill()
    if tipo_piso == "madeira":
        for i in range(-16, 17):
            c.move_to(W / 2 + i * 50, chao); c.line_to(W / 2 + i * 130, H); rgb(c, dk(pcol, 0.25), 0.5); c.set_line_width(2.5); c.stroke()
    elif tipo_piso == "ladrilho":
        for r in range(8):
            yy = chao + (H - chao) * (r / 8) ** 1.3
            c.rectangle(0, yy, W, 2); rgb(c, dk(pcol, 0.18), 0.6); c.fill()
        for i in range(-16, 17):
            c.move_to(W / 2 + i * 70, chao); c.line_to(W / 2 + i * 160, H); rgb(c, dk(pcol, 0.18), 0.6); c.set_line_width(2); c.stroke()
    if rodape:
        c.rectangle(0, chao - 22, W, 22); rgb(c, P(dk(parede, 0.3))); c.fill()
    return chao


# ---------------------------------------------------------------- cenários de vida real (full-bleed)
def cena_cozinha(c, t, hora="dia", chao=None):
    luz(hora)
    chao = _sala(c, (0.86, 0.90, 0.88), (0.80, 0.78, 0.74), chao, tipo_piso="ladrilho")
    # azulejo na meia parede
    for r in range(6):
        for k in range(0, int(W / 50) + 1):
            c.rectangle(k * 50 + 2, chao - 330 + r * 50 + 2, 46, 46); rgb(c, P((0.80, 0.88, 0.90))); c.fill()
    janela_cidade(c, W * 0.66, chao - 760 if not V else chao - 1020, 380 if not V else 340, 300)
    c.save(); c.translate(W * 0.30, chao - 560 if not V else chao - 760); armarios_altos(c, W * 0.48, 200); c.restore()
    c.save(); c.translate(W * 0.30, chao); bancada_i(c, W * 0.48, 280); c.restore()
    c.save(); c.translate(W * 0.88, chao); geladeira_i(c, 560); c.restore()
    c.save(); c.translate(W * 0.18, chao - 306); planta_vaso(c, 140); c.restore()


def cena_padaria(c, t, hora="dia", chao=None, cardapio=(("CAFÉ", "R$ 6"), ("PÃO", "R$ 4"))):
    luz(hora)
    chao = _sala(c, (0.96, 0.86, 0.66), (0.70, 0.40, 0.30), chao, tipo_piso="ladrilho")
    # prateleiras de pão no fundo
    for r in range(3):
        yy = chao - 620 + r * 120 if not V else chao - 900 + r * 140
        c.rectangle(W * 0.05, yy, W * 0.5, 14); rgb(c, P(MADEIRA)); c.fill()
        for k in range(int(W * 0.5 / 70)):
            ellipse(c, W * 0.05 + 40 + k * 70, yy - 22, 30, 22); rgb(c, P((0.82, 0.56, 0.28) if (k + r) % 2 else (0.90, 0.72, 0.42))); c.fill()
    if cardapio and not V:  # no vertical o quadro bate no título
        c.save(); c.translate(W * 0.76, chao - 520); placa_preco(c, cardapio, 380); c.restore()
    for xx in (W * 0.3, W * 0.7):
        luminaria(c, xx, 0, 120)
    c.save(); c.translate(W * 0.5, chao + 10); balcao_i(c, W * 0.92, 230, vidro=True); c.restore()


def cena_mercado(c, t, hora="interior", chao=None, carrinho=True):
    luz(hora)
    chao = _sala(c, (0.94, 0.94, 0.92), (0.86, 0.86, 0.84), chao, tipo_piso="ladrilho")
    for i in range(3 if not V else 2):
        c.save(); c.translate(W * (0.2 + i * 0.3) if not V else W * (0.27 + i * 0.46), chao - 10)
        prateleira_mercado(c, W * 0.27 if not V else W * 0.44, 560 if not V else 760, seed=i + 2); c.restore()
    for k in range(4):
        c.rectangle(0, 40 + k * 4, W, 2); rgb(c, (1, 1, 1), 0.5); c.fill()
    if carrinho:
        c.save(); c.translate(W * 0.78, chao + 120); c.scale(0.9, 0.9); carrinho_i(c, 0.8); c.restore()


def cena_escritorio(c, t, hora="dia", chao=None):
    luz(hora)
    chao = _sala(c, (0.90, 0.90, 0.88), (0.56, 0.56, 0.58), chao, tipo_piso="liso")
    janela_cidade(c, W * 0.08, chao - 720 if not V else chao - 1000, W * 0.84, 460 if not V else 560)
    for xx in ((0.30, 0.72) if not V else (0.5,)):
        c.save(); c.translate(W * xx, chao + 40); mesa_trabalho(c, 460 if not V else 520); c.restore()
    c.save(); c.translate(W * 0.94 if not V else W * 0.88, chao); planta_vaso(c, 220); c.restore()


def cena_sala(c, t, hora="tarde", chao=None):
    luz(hora)
    chao = _sala(c, (0.88, 0.80, 0.70), (0.58, 0.42, 0.28), chao)
    if not V:
        janela_cidade(c, W * 0.06, chao - 640, 360, 420)
        rr(c, W * 0.5 - 120, chao - 640, 240, 170, 6); rgb(c, P((0.42, 0.56, 0.48))); c.fill()
        c.save(); c.translate(W * 0.55, chao + 40); sofa_i(c, 560); c.restore()
        c.save(); c.translate(W * 0.86, chao); tv_i(c, 300); c.restore()
    else:
        janela_cidade(c, W * 0.1, chao - 1000, W * 0.8, 420)
        c.save(); c.translate(W * 0.5, chao + 40); sofa_i(c, 640); c.restore()
    ellipse(c, W * 0.5, chao + 110, W * 0.38, 40); rgb(c, P((0.70, 0.36, 0.30)), 0.8); c.fill()
    c.save(); c.translate(W * 0.08 if not V else W * 0.9, chao); planta_vaso(c, 240); c.restore()


def cena_rua(c, t, hora="dia", chao=None, carros=True, seed=2):
    luz(hora)
    chao = chao or CHAO
    ceu(c, t, passaros=not _L["noite"], seed=seed, horizonte=chao)
    rnd = random.Random(seed)
    x = -40
    while x < W:
        w_ = rnd.uniform(160, 260); h_ = rnd.uniform(0.35, 0.65) * chao
        predio_moderno(c, x, chao - 60, w_, h_, rnd.choice([(0.62, 0.66, 0.72), (0.74, 0.70, 0.64), (0.56, 0.60, 0.66)]), 0.45, seed=rnd.randint(0, 99))
        x += w_ + 10
    x = -60
    while x < W:
        w_ = rnd.uniform(240, 340); h_ = rnd.uniform(0.25, 0.42) * chao
        predio(c, x, chao - 40, w_, h_, "colonial", seed=rnd.randint(0, 99), depth=0.1)
        x += w_
    c.rectangle(0, chao - 40, W, 60); rgb(c, P((0.78, 0.76, 0.72))); c.fill()    # calçada
    c.rectangle(0, chao + 20, W, H - chao); rgb(c, P((0.34, 0.34, 0.36))); c.fill()  # rua
    for k in range(-1, int(W / 160) + 2):
        c.rectangle(k * 160 + (t * 0) % 160, chao + 110, 80, 10); rgb(c, P((0.95, 0.92, 0.80))); c.fill()
    for xx in (W * 0.12, W * 0.62):
        c.save(); c.translate(xx, chao - 20); poste_i(c, 380 if not V else 460); c.restore()
    for xx in (W * 0.36, W * 0.9):
        arvore(c, t, xx, chao - 20, 300, "redonda", seed=int(xx))
    if carros:
        for i, (cor, sp, yy) in enumerate((((0.86, 0.26, 0.22), 160, chao + 190), ((0.26, 0.50, 0.80), -120, chao + 90))):
            xx = (t * sp + i * 900) % (W + 600) - 300
            c.save(); c.translate(xx, yy); c.scale(0.8 * (1 if sp > 0 else -1), 0.8); carro_i(c, t, cor, anda=True); c.restore()


def cena_agencia(c, t, hora="interior", chao=None, banco="BANCO"):
    luz(hora)
    chao = _sala(c, (0.86, 0.88, 0.92), (0.78, 0.78, 0.80), chao, tipo_piso="ladrilho")
    rr(c, W * 0.5 - 220, 90, 440, 110, 14); rgb(c, P(NAVY)); c.fill()
    c.select_font_face(MARKER); c.set_font_size(64); ww = c.text_extents(banco).x_advance
    c.move_to(W * 0.5 - ww / 2, 168); rgb(c, GOLD); c.show_text(banco)
    c.save(); c.translate(W * 0.5, chao + 10); balcao_i(c, W * 0.6 if not V else W * 0.9, 240, cor=(0.70, 0.72, 0.78)); c.restore()
    for xx in ((W * 0.08, W * 0.92) if not V else (W * 0.12,)):
        c.save(); c.translate(xx, chao); caixa_eletronico(c); c.restore()
    for xx in (W * 0.3, W * 0.7):
        luminaria(c, xx, 0, 60)


def vinheta(c, a=0.30):
    g = cairo.RadialGradient(W / 2, H / 2, min(W, H) * 0.35, W / 2, H / 2, max(W, H) * 0.72)
    g.add_color_stop_rgba(0, 0, 0, 0, 0); g.add_color_stop_rgba(1, 0, 0, 0, a)
    c.set_source(g); c.paint()


# ---------------------------------------------------------------- encerramento (Tela final do YouTube)
def tela_final_i(c, t, t0=0):
    """Tela final do YouTube (cauda de 5 s sem narração). Áreas livres: vídeo sugerido à esquerda (x 170-950, y 300-740)
    e botão inscrever-se à direita (círculo em ~1450, 520). Logo em cima, O Consultor pequeno embaixo no centro."""
    fundo_marca(c, t, "navy", holofote=(960, 900))
    entra(c, t, t0 + 0.1, 960, 140, lambda c: numero_i(c, "FAZ A CONTA", 0, 0, 90, GOLD), anim="fade")
    for x, s_ in ((560, "assista também"), (1450, "inscreva-se")):
        entra(c, t, t0 + 0.3, x, 800, lambda c, s_=s_: numero_i(c, s_, 0, 0, 44, CREME, contorno=NAVY), anim="fade")
    consultor_i(c, t, 960, 1070, 0.62, poses=((0, "wave"), (t0 + 2.4, "relax")), exprs=((0, "happy"),), look=0.0, appear=t0 + 0.1)
