"""Gera palavras.json, transcricao.txt e narracao_blocos.txt a partir de roteiro.txt + ts_b*.txt (word_timestamps do HeyGen)."""
import json
DUR = {1: 174.658, 2: 169.138, 3: 215.619}
PAUSA = 0.4
URL = {1: 'https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=e2f99bea655b4ee99fed851f09b87f51.wav', 2: 'https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=8653fba4a3a4466f8ef611d81da4c6fb.wav', 3: 'https://resource2.heygen.ai/text_to_speech/cdea5e656a244864a1032edcb4fae01d/3b2a59d6edb54e79a40b29726a12d1c3/id=10cd4840d4404e2aa406d365f2268d57.wav'}
off = {1: 0.0}; off[2] = DUR[1] + PAUSA; off[3] = off[2] + DUR[2] + PAUSA
BL = {int(x[0]): x.split("\n", 1)[1].strip() for x in open("roteiro.txt").read().split("[BLOCO ")[1:]}
pal, trans, lines = [], [], []
for b in (1, 2, 3):
    w = BL[b].split()
    ts = [l.rsplit(" ", 2) for l in open(f"ts_b{b}.txt").read().strip().split("\n")]
    assert len(w) == len(ts), (b, len(w), len(ts))
    for ww, (tw, _, _) in zip(w, ts):
        assert ww.strip('",.:?!').lower() == tw.strip('",.:?!').lower(), (b, ww, tw)
    t = [float(x[1]) for x in ts]; e = [float(x[2]) for x in ts]
    for k, ww in enumerate(w):
        pal.append({"w": ww, "t0": round(t[k] + off[b], 3), "t1": round(e[k] + off[b], 3)})
    st = None
    for k, ww in enumerate(w):
        if st is None: st = k
        if ww.rstrip('"').endswith(('.', '?', '!')) or k == len(w) - 1:
            words = w[st:k+1]; times = t[st:k+1]
            marks = " ".join(f"[{words[i].strip(',.:?!\"').lower()}@{times[i]:.2f}]" for i in range(7, len(words), 7))
            lines.append(f"{b}|{times[0]:.2f}|{' '.join(words)}" + (" " + marks if marks else ""))
            a = times[0] + off[b]; trans.append(f"({int(a//60)}:{a%60:05.2f}) {' '.join(words)}")
            st = None
json.dump(pal, open("palavras.json", "w"), ensure_ascii=False)
open("transcricao.txt", "w").write("\n".join(trans) + "\n")
fim = off[3] + DUR[3]
hdr = ['# Narração "R$ 10 mil há 10 anos" — voz Calm Carlos (HeyGen Voice, heygen-voice-1), voice_id 3b2a59d6edb54e79a40b29726a12d1c3']
for b in (1, 2, 3): hdr.append(f"# bloco{b} {DUR[b]:.3f}s {URL[b]}")
hdr.append(f"# pausa_blocos {PAUSA}")
hdr.append("# Junta: blocos com 0,4 s de silêncio + 5 s de cauda sem narração (tela final)")
hdr.append(f"# offsets absolutos: bloco1 0.000 | bloco2 {off[2]:.3f} | bloco3 {off[3]:.3f} | fim da fala {fim:.3f} | total {fim+5:.3f}")
hdr.append("# Formato: bloco | início local (s) | frase [palavra@t local]")
open("narracao_blocos.txt", "w").write("\n".join(hdr + lines) + "\n")
print(off, len(pal), len(lines), "fim", fim, "total", fim + 5)
