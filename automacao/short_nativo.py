"""
Sobe um vídeo nativo vertical do TikTok automático (release "tiktok-<slug>") como YouTube Short,
PUBLICADO NA HORA (sem agendamento), com a marcação de conteúdo sintético (voz de IA).

Teste de 10/11/2026: os Shorts cortados do vídeo longo e enviados agendados pela API estavam com 1 a 28 views;
o nativo "carro custa mais que aluguel" postado à mão passou de 775 em poucas horas (sem a marcação de IA).
Este script isola as variáveis: formato nativo + API + publicação na hora + marcação ligada.

    python automacao/short_nativo.py <slug> [--titulo "..."]

Título: linha "TÍTULO DO YOUTUBE SHORTS" do videos/<slug>/post.txt (+ " #Shorts").
Descrição: a legenda do TikTok do mesmo post.txt. Registra em fila/shorts_nativos.json.
"""
import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publicar import FUSO, RAIZ, limpar_tags, limpar_texto, log, youtube  # noqa: E402

REPO = "matheuspdias/stickfigure-videos"


def textos(slug):
    p = os.path.join(RAIZ, "videos", slug, "post.txt")
    linhas = open(p, encoding="utf-8").read().split("\n")
    titulo, legenda, modo = None, [], None
    for ln in linhas:
        s = ln.strip()
        if s.startswith("LEGENDA DO POST"):
            modo = "leg"; continue
        if s.startswith("TÍTULO DO YOUTUBE SHORTS"):
            modo = "tit"; continue
        if s.startswith("CAPA:") or s.startswith("Lembretes:"):
            modo = None; continue
        if modo == "leg" and s:
            legenda.append(s.replace("👇", "").rstrip())
        elif modo == "tit" and s and titulo is None:
            titulo = s
    tags = [w.lstrip("#") for w in " ".join(legenda).split() if w.startswith("#")]
    return titulo, "\n".join(legenda), tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--titulo")
    a = ap.parse_args()
    slug = a.slug
    titulo, desc, tags = textos(slug)
    titulo = (a.titulo or titulo or slug).strip()
    if "#shorts" not in titulo.lower():
        titulo += " #Shorts"
    pasta = os.path.join(RAIZ, "out", "nativo", slug)
    os.makedirs(pasta, exist_ok=True)
    subprocess.run(["gh", "release", "download", f"tiktok-{slug}", "-R", REPO, "-p", "*.mp4", "-D", pasta, "--clobber"], check=True)
    mp4 = sorted(glob.glob(os.path.join(pasta, "*.mp4")))
    if not mp4:
        raise SystemExit("nenhum MP4 na release")
    arquivo = [m for m in mp4 if m.endswith("_tiktok.mp4")] or mp4
    arquivo = arquivo[0]
    log("enviando", os.path.basename(arquivo), "|", titulo)

    from googleapiclient.http import MediaFileUpload
    yt = youtube()
    corpo = {
        "snippet": {"title": limpar_texto(titulo, 100), "description": limpar_texto(desc, 5000), "tags": limpar_tags(tags),
                    "categoryId": "27", "defaultLanguage": "pt-BR", "defaultAudioLanguage": "pt-BR"},
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": True,
                   "embeddable": True},
    }
    media = MediaFileUpload(arquivo, mimetype="video/mp4", chunksize=16 * 1024 * 1024, resumable=True)
    req = yt.videos().insert(part="snippet,status", body=corpo, media_body=media, notifySubscribers=True)
    resp = None
    while resp is None:
        _, resp = req.next_chunk()
    vid = resp["id"]
    st = resp.get("status", {})
    log(f"publicado: https://youtu.be/{vid}  status={st.get('privacyStatus')}")
    reg_p = os.path.join(RAIZ, "fila", "shorts_nativos.json")
    reg = json.load(open(reg_p, encoding="utf-8")) if os.path.exists(reg_p) else []
    reg.append({"slug": slug, "titulo": titulo, "video_id": vid, "url": f"https://youtu.be/{vid}",
                "publicado_em": dt.datetime.now(FUSO).replace(microsecond=0).isoformat(), "via": "api, publicado na hora",
                "containsSyntheticMedia": True, "privacy": st.get("privacyStatus")})
    with open(reg_p, "w", encoding="utf-8") as f:
        json.dump(reg, f, ensure_ascii=False, indent=2); f.write("\n")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(f"### Short nativo publicado\n\n**{titulo}**: https://youtu.be/{vid} ({st.get('privacyStatus')})\n")


if __name__ == "__main__":
    main()
