"""Vídeo SÓ para TikTok/Shorts/Reels (vertical nativo, sem versão longa): queima as legendas palavra por palavra
no MP4 1080x1920 gerado pelo render.py (scenes.py com VERTICAL = True).

    python tiktok.py videos/<slug> out/<slug>_base.mp4 out/<slug>_tiktok.mp4 [--cap-y 1460]

Tempos das palavras: videos/<slug>/palavras.json ([{"w": "...", "t0": s, "t1": s}, ...], word_timestamps do HeyGen).
Estilo e cor de destaque vêm do tema dos cortes (tema_cortes.json): palavra falada em dourado, resto em branco
com contorno preto. As legendas ficam entre os pés dos bonecos e a área da descrição do TikTok.
"""
import argparse
import json
import os
import subprocess

import cortes

ROOT = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vdir"); ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--cap-y", type=int, default=1460)
    a = ap.parse_args()
    words = json.load(open(os.path.join(a.vdir, "palavras.json"), encoding="utf-8"))
    dur = cortes.probe_dur(a.video)
    cortes.CAP_Y = a.cap_y
    ev = cortes.caption_events(words, 0.0, dur)
    # no fundo claro o contorno grosso "come" os espaços: usa espaço duro duplo entre as palavras
    ev = [e.split("}", 1)[0] + "}" + e.split("}", 1)[1].replace(" ", "\\h\\h") for e in ev]
    head = cortes.ass_head()
    head = "\n".join(l.replace(",78,", ",92,").replace(",7,3,5,", ",8,0,5,") if l.startswith("Style: Cap,") else l
                     for l in head.split("\n"))
    ass = os.path.splitext(a.out)[0] + ".ass"
    open(ass, "w", encoding="utf-8").write(head + "\n".join(ev) + "\n")
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", a.video,
                    "-vf", f"ass={ass}:fontsdir={cortes.FONTS}", "-c:v", "libx264", "-preset", "slow", "-crf", "24",
                    "-tune", "animation", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", a.out],
                   check=True)
    print(a.out, round(os.path.getsize(a.out) / 1e6, 1), "MB", round(dur, 1), "s")


if __name__ == "__main__":
    main()
