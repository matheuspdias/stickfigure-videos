"""Gera palavras.json, transcricao.txt e narracao_blocos.txt a partir de b*.txt + ts_b*.txt."""
import json
DUR = {1: 162.586, 2: 185.835, 3: 226.56}
URL = {1: "https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=904aa164-b8e2-4079-b396-5b1c3d428c05.wav",
       2: "https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=4998b9ba-e296-4a6c-ab60-cdfc244d9591.wav",
       3: "https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=5ffa3f4d-c33a-465c-b827-07e43091110d.wav"}
off = {1: 0.0}; off[2] = DUR[1] + 1; off[3] = off[2] + DUR[2] + 1
BL = {int(x[0]): x.split("\n",1)[1].strip() for x in open("roteiro.txt").read().split("### BLOCO ")[1:]}
pal, trans, lines = [], [], []
for b in (1, 2, 3):
    w = BL[b].split(); t = [float(x) for x in open(f"ts_b{b}.txt").read().split()]
    assert len(w) == len(t)
    for k, (ww, tt) in enumerate(zip(w, t)):
        t1 = (t[k+1] - 0.04) if k+1 < len(t) else DUR[b]
        pal.append({"w": ww, "t0": round(tt + off[b], 3), "t1": round(max(tt + 0.05, min(t1, tt + 1.2)) + off[b], 3)})
    # frases
    sent, st = [], None
    for k, (ww, tt) in enumerate(zip(w, t)):
        if st is None: st = k
        if ww.rstrip('"').endswith(('.', '?', '!')) or k == len(w) - 1:
            words = w[st:k+1]; times = t[st:k+1]
            marks = " ".join(f"[{words[i].strip(',.:?!\"').lower()}@{times[i]:.2f}]" for i in range(7, len(words), 7))
            lines.append(f"{b}|{times[0]:.2f}|{' '.join(words)}" + (" " + marks if marks else ""))
            a = times[0] + off[b]; trans.append(f"({int(a//60)}:{a%60:05.2f}) {' '.join(words)}")
            st = None
json.dump(pal, open("palavras.json", "w"), ensure_ascii=False)
open("transcricao.txt", "w").write("\n".join(trans) + "\n")
hdr = ['# Narração "Alugar ou comprar? A conta que quase ninguém faz" — voz Calm Carlos (HeyGen, ElevenLabs v4), voice_id 3b2a59d6edb54e79a40b29726a12d1c3']
for b in (1, 2, 3): hdr.append(f"# bloco{b} {DUR[b]:.3f}s {URL[b]}")
hdr.append("# Junta: blocos com 1 s de silêncio + 15 s de cauda sem narração (tela final)")
hdr.append(f"# offsets absolutos: bloco1 0.00 | bloco2 {off[2]:.2f} | bloco3 {off[3]:.2f} | fim da fala {off[3]+DUR[3]:.2f}")
hdr.append("# bloco|início local|frase [palavra@t local]")
open("narracao_blocos.txt", "w").write("\n".join(hdr + lines) + "\n")
print(off, len(pal), len(lines))
