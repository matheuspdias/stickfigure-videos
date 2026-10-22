"""Junta os blocos de narração em um único .wav, com silêncio entre eles (1,0 s, ou o valor de --pausa).

    python juntar_blocos.py saida.wav bloco1.mp3 bloco2.mp3 ... [--pausa 0.4] [--cauda 5]

--pausa N silêncio entre os blocos (padrão 1,0 s; o Faz a Conta usa 0,4 s desde 26/10/2026).

--cauda N acrescenta N segundos de silêncio no fim (encerramento sem narração para a Tela final do YouTube).

IMPORTANTE: todas as entradas (inclusive o silêncio do anullsrc) são forçadas para float 44,1 kHz mono.
Sem isso o filtro concat do ffmpeg pode negociar áudio de 8 bits, o que cria um chiado que só aparece
quando o narrador fala (foi o ruído do MH370 e da 1ª versão do Mary Celeste).
No fim o script confere cada bloco contra o original e acusa se a diferença passar de -90 dB.
"""
import subprocess
import sys

import numpy as np

SR = 44100
FMT = f"aformat=sample_fmts=flt:sample_rates={SR}:channel_layouts=mono"


def decode(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32)


def join(out, blocks, gap=1.0, tail=0.0):
    args, chains, order = [], [], []
    for i, b in enumerate(blocks):
        args += ["-i", b]
        chains.append(f"[{i}:a]{FMT}[a{i}]")
    n = len(blocks)
    args += ["-f", "lavfi", "-t", str(gap), "-i", f"anullsrc=r={SR}:cl=mono"]
    if n > 1:
        chains.append(f"[{n}:a]{FMT},asplit={n - 1}" + "".join(f"[s{i}]" for i in range(n - 1)))
    for i in range(n):
        order.append(f"[a{i}]")
        if i < n - 1:
            order.append(f"[s{i}]")
    if tail > 0:
        args += ["-f", "lavfi", "-t", str(tail), "-i", f"anullsrc=r={SR}:cl=mono"]
        chains.append(f"[{n + 1}:a]{FMT}[tail]")
        order.append("[tail]")
    graph = ";".join(chains) + ";" + "".join(order) + f"concat=n={len(order)}:v=0:a=1"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", graph, "-c:a", "pcm_s16le", out], check=True)
    # conferência
    full = decode(out)
    pos = 0
    for b in blocks:
        src = decode(b)
        seg = full[pos:pos + len(src)]
        m = min(len(seg), len(src))
        diff = 20 * np.log10(np.sqrt(np.mean((seg[:m] - src[:m]) ** 2)) + 1e-12)
        flag = "ok" if diff < -90 else "ATENÇÃO: áudio alterado"
        print(f"{b}: {len(src) / SR:.3f}s, início {pos / SR:.3f}s, diferença {diff:.0f} dB -> {flag}")
        pos += len(src) + int(round(gap * SR))
    print(out, f"{len(full) / SR:.3f}s")


if __name__ == "__main__":
    a = sys.argv[1:]
    tail, gap = 0.0, 1.0
    if "--cauda" in a:
        i = a.index("--cauda"); tail = float(a[i + 1]); del a[i:i + 2]
    if "--pausa" in a:
        i = a.index("--pausa"); gap = float(a[i + 1]); del a[i:i + 2]
    join(a[0], a[1:], gap=gap, tail=tail)
