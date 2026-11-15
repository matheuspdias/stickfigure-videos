"""Trilha própria do Faz a Conta (formato "E se..." das 10h). Composta por código, 100% original:
sem sample, sem música de terceiros, para os vídeos entrarem no programa de recompensas do TikTok
(música protegida tocando mais de 1 minuto deixa o vídeo inelegível).

Clima: chill "slowed + reverb" em lá menor, 76 BPM, progressão Am - F - C - G, pad largo, baixo redondo,
arpejo com eco, batida macia e uma melodia curta que volta de tempos em tempos.
Gera musica/trilha_faz_a_conta.mp3 (~2 min 40 s, loudness -13 LUFS).

    python musica_fonte/trilha_faz_a_conta.py
"""
import os
import subprocess
import numpy as np
from scipy.signal import lfilter, butter

SR = 44100
BPM = 76
BEAT = 60 / BPM
BAR = 4 * BEAT
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def hz(n):  # nota MIDI -> Hz
    return 440.0 * 2 ** ((n - 69) / 12)


# Am, F, C, G (notas MIDI do acorde, baixo)
ACORDES = [((57, 60, 64, 69), 45), ((53, 57, 60, 65), 41), ((48, 52, 55, 60), 36), ((55, 59, 62, 67), 43)]
N_COMPASSOS = 52  # ~2 min 44 s
DUR = N_COMPASSOS * BAR
N = int(SR * (DUR + 4))


def env_adsr(n, a, d, s, r, sus_len):
    out = np.zeros(n)
    ia, idd, isus, ir = int(a * SR), int(d * SR), int(sus_len * SR), int(r * SR)
    seg = np.concatenate([np.linspace(0, 1, max(ia, 1)), np.linspace(1, s, max(idd, 1)), np.full(max(isus, 0), s),
                          np.linspace(s, 0, max(ir, 1))])
    out[:min(n, len(seg))] = seg[:n]
    return out


def lp(x, fc, ordem=2):
    b, a = butter(ordem, fc / (SR / 2))
    return lfilter(b, a, x)


def hp(x, fc, ordem=2):
    b, a = butter(ordem, fc / (SR / 2), "high")
    return lfilter(b, a, x)


def pad(notas, dur):
    n = int(SR * (dur + 1.6)); t = np.arange(n) / SR
    x = np.zeros(n)
    for m in notas:
        for det in (-0.08, 0.0, 0.08):  # 3 vozes levemente desafinadas (coro)
            f = hz(m + det)
            for k, a in ((1, 1.0), (2, 0.35), (3, 0.18), (4, 0.08)):
                x += a * np.sin(2 * np.pi * f * k * t + k * 0.7)
    x *= env_adsr(n, 0.9, 0.6, 0.8, 1.6, dur - 1.5)
    x *= 1 + 0.15 * np.sin(2 * np.pi * 0.25 * t)  # respiração lenta
    return lp(x, 1500)


def baixo(m, dur):
    n = int(SR * (dur + 0.3)); t = np.arange(n) / SR
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t)
    return x * env_adsr(n, 0.02, 0.3, 0.7, 0.3, dur - 0.32)


def pluck(m, dur=0.9):
    n = int(SR * dur); t = np.arange(n) / SR
    f = hz(m)
    x = (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 2 * f * t) + 0.15 * np.sin(2 * np.pi * 3 * f * t))
    return x * np.exp(-t * 4.5) * np.minimum(1, t / 0.004)


def kick():
    d = 0.45; n = int(SR * d); t = np.arange(n) / SR
    f = 42 + 80 * np.exp(-t * 28)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)


def rim():  # estalo tonal curto no lugar da caixa (sem ruído)
    d = 0.12; n = int(SR * d); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1650 * t) + 0.6 * np.sin(2 * np.pi * 2420 * t)) * np.exp(-t * 60)


def sino(m, dur=1.6):
    n = int(SR * dur); t = np.arange(n) / SR
    f = hz(m)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 3)
    return x * np.exp(-t * 2.2) * np.minimum(1, t / 0.01)


def por(trilha, x, t0, g=1.0):
    i = int(t0 * SR)
    if i >= len(trilha):
        return
    j = min(len(trilha), i + len(x))
    trilha[i:j] += x[: j - i] * g


def _comb(x, d, g):
    """y[n] = x[n] + g*y[n-d], em blocos de d amostras (rápido)"""
    y = np.array(x, dtype=float)
    for k in range(d, len(y), d):
        e = min(k + d, len(y))
        y[k:e] += g * y[k - d:e - d]
    return y


def _allpass(x, d, g):
    """y[n] = -g*x[n] + x[n-d] + g*y[n-d], em blocos"""
    y = -g * np.array(x, dtype=float)
    y[d:] += x[:-d]
    for k in range(d, len(y), d):
        e = min(k + d, len(y))
        y[k:e] += g * y[k - d:e - d]
    return y


def eco(x, atraso, fb, mix):
    d = int(atraso * SR)
    y = _comb(x, d, fb)
    out = x.copy(); out[d:] += mix * fb * y[:-d]
    return out


def reverb(x, mix=0.35):
    """Schroeder: 4 combs em paralelo + 2 all-pass (tudo determinístico, sem ruído)"""
    y = np.zeros_like(x)
    for atraso, g in ((0.0297, 0.84), (0.0371, 0.83), (0.0411, 0.82), (0.0437, 0.81)):
        y += _comb(x, int(atraso * SR * 1.6), g)
    y /= 4
    for atraso, g in ((0.005, 0.7), (0.0017, 0.7)):
        y = _allpass(y, int(atraso * SR * 1.6), g)
    y = lp(hp(y, 180), 4500)
    return x * (1 - mix) + y * mix * 0.6


def compor():
    L = np.zeros(N); R = np.zeros(N)
    pads = np.zeros(N); bass = np.zeros(N); arp = np.zeros(N); bat = np.zeros(N); mel = np.zeros(N)
    # seções: 0-3 intro (pad), 4-11 A (+baixo, arpejo), 12-27 B (+batida, melodia), 28-31 respiro, 32-47 B', 48-51 saída
    motivo = [(0, 76), (1.5, 74), (2, 72), (3, 71)]  # mi - ré - dó - si sobre o compasso
    padrao_arp = [0, 1, 2, 3, 2, 1, 2, 3]
    for b in range(N_COMPASSOS):
        t0 = b * BAR
        notas, raiz = ACORDES[b % 4]
        por(pads, pad(notas, BAR), t0, 0.55)
        tem_baixo = 4 <= b < 48
        tem_arp = 4 <= b < 50 and not (28 <= b < 30)
        tem_bat = (12 <= b < 28) or (32 <= b < 48)
        tem_mel = (16 <= b < 28 and b % 4 in (0, 2)) or (36 <= b < 48 and b % 4 in (0, 2))
        if tem_baixo:
            por(bass, baixo(raiz, 2 * BEAT), t0, 0.9)
            por(bass, baixo(raiz + (7 if b % 2 else 0), 2 * BEAT), t0 + 2 * BEAT, 0.8)
        if tem_arp:
            for k, idx in enumerate(padrao_arp):
                por(arp, pluck(notas[idx] + 12), t0 + k * BEAT / 2, 0.30 if k % 2 == 0 else 0.22)
        if tem_bat:
            por(bat, kick(), t0, 1.0); por(bat, kick(), t0 + 2.5 * BEAT, 0.7)
            por(bat, rim(), t0 + BEAT, 0.25); por(bat, rim(), t0 + 3 * BEAT, 0.25)
        if tem_mel:
            for dt, m in motivo:
                por(mel, sino(m + (0 if b % 8 < 4 else -2)), t0 + dt * BEAT, 0.32)
    arp = eco(arp, BEAT * 0.75, 0.38, 0.55)
    mel = eco(mel, BEAT * 0.75, 0.40, 0.6)
    # panorâmica leve
    L += pads * 1.0 + bass + arp * 0.75 + bat + mel * 1.0
    R += pads * 1.0 + bass + arp * 1.0 + bat + mel * 0.75
    L, R = reverb(L, 0.38), reverb(np.roll(R, 37), 0.38)
    est = np.stack([L, R], 1)[: int(SR * (DUR + 3))]
    # fade final
    fim = int(SR * 3)
    est[-fim:] *= np.linspace(1, 0, fim)[:, None]
    est /= np.max(np.abs(est)) * 1.05
    return est


def salvar(est, mp3):
    import wave
    wav = mp3.replace(".mp3", ".wav")
    pcm = (est * 32767).astype(np.int16)
    with wave.open(wav, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-13:TP=-1.5:LRA=9", "-ar", "44100",
                    "-c:a", "libmp3lame", "-b:a", "192k", mp3], check=True)
    os.remove(wav)


if __name__ == "__main__":
    os.makedirs(os.path.join(RAIZ, "musica"), exist_ok=True)
    saida = os.path.join(RAIZ, "musica", "trilha_faz_a_conta.mp3")
    salvar(compor(), saida)
    print("ok:", saida)
