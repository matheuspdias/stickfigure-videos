"""
Prévia das thumbnails como aparecem no YouTube, para escolher a melhor (e reprovar as ilegíveis).

    python automacao/thumb_preview.py videos/<slug>/thumb/*.png -o out/thumb_preview.png [--titulo "..."]

Monta, para cada thumbnail:
  - feed da página inicial no computador (360x202, fundo branco), com o selo de duração no canto inferior direito;
  - lista de "vídeos sugeridos" (168x94, fundo escuro), onde está o maior volume de impressões do canal;
  - celular (tela cheia de largura, ~390 px).
Leia a prévia de longe: se o número/as palavras não forem lidos a 168 px, a thumbnail está reprovada.
"""
import argparse
import os
import subprocess
import tempfile

import cairo

FONTE = "Patrick Hand"


def png_surface(path, w, h):
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", path, "-vf", f"scale={w}:{h}:flags=lanczos", tmp], check=True)
    s = cairo.ImageSurface.create_from_png(tmp)
    os.remove(tmp)
    return s


def rr(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -1.5708, 0); c.arc(x + w - r, y + h - r, r, 0, 1.5708)
    c.arc(x + r, y + h - r, r, 1.5708, 3.1416); c.arc(x + r, y + r, r, 3.1416, 4.7124); c.close_path()


def thumb(c, path, x, y, w, h, dur="9:08", r=8):
    s = png_surface(path, w, h)
    c.save(); rr(c, x, y, w, h, r); c.clip(); c.set_source_surface(s, x, y); c.paint(); c.restore()
    c.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(max(10, h * 0.075))
    e = c.text_extents(dur)
    bw, bh = e.x_advance + 10, h * 0.11 + 6
    rr(c, x + w - bw - 6, y + h - bh - 6, bw, bh, 3); c.set_source_rgba(0, 0, 0, 0.8); c.fill()
    c.move_to(x + w - bw - 1, y + h - 6 - bh * 0.28); c.set_source_rgb(1, 1, 1); c.show_text(dur)


def texto(c, s, x, y, size, col, bold=False, maxw=None):
    c.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    c.set_font_size(size)
    if maxw:
        while c.text_extents(s).x_advance > maxw and len(s) > 4:
            s = s[:-4] + "..."
    c.move_to(x, y); c.set_source_rgb(*col); c.show_text(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("thumbs", nargs="+")
    ap.add_argument("-o", "--saida", default="out/thumb_preview.png")
    ap.add_argument("--titulo", default="Título do vídeo do Faz a Conta")
    ap.add_argument("--dur", default="9:08")
    a = ap.parse_args()
    n = len(a.thumbs)
    col_w = 420
    W, H = 60 + n * col_w, 1000
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf)
    c.set_source_rgb(1, 1, 1); c.paint()
    # faixa escura para os sugeridos
    c.rectangle(0, 330, W, 330); c.set_source_rgb(0.06, 0.06, 0.06); c.fill()
    texto(c, "PÁGINA INICIAL (360x202, fundo branco)", 30, 30, 18, (0.4, 0.4, 0.4), True)
    texto(c, "VÍDEOS SUGERIDOS (168x94, modo escuro): onde está o maior volume de impressões", 30, 360, 18, (0.75, 0.75, 0.75), True)
    texto(c, "CELULAR (390 px de largura)", 30, 690, 18, (0.4, 0.4, 0.4), True)
    for i, p in enumerate(a.thumbs):
        x0 = 30 + i * col_w
        thumb(c, p, x0, 50, 360, 202, a.dur)
        texto(c, a.titulo, x0, 280, 16, (0.06, 0.06, 0.06), True, 360)
        texto(c, "Faz a Conta · 120 visualizações · há 2 dias", x0, 302, 13, (0.38, 0.38, 0.38), False, 360)
        thumb(c, p, x0, 385, 168, 94, a.dur, 6)
        texto(c, a.titulo, x0 + 178, 400, 14, (0.95, 0.95, 0.95), True, 220)
        texto(c, "Faz a Conta", x0 + 178, 420, 12, (0.67, 0.67, 0.67))
        thumb(c, p, x0, 470, 168, 94, a.dur, 6)
        texto(c, os.path.basename(p), x0, 600, 14, (0.8, 0.8, 0.8), True, 380)
        thumb(c, p, x0, 710, 390, 219, a.dur, 0)
        texto(c, a.titulo, x0, 955, 16, (0.06, 0.06, 0.06), True, 390)
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    surf.write_to_png(a.saida)
    print(a.saida)


if __name__ == "__main__":
    main()
