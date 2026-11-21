"""Roda DENTRO da GitHub Action `tts`: gera a narração de um vídeo pela API do HeyGen (HeyGen Voice 1, com tempos)
e deixa tudo pronto para as cenas e a fila do TikTok.

Pedido (feito pelo Claude e enviado com push): tts_in/<slug>.json
  {"slug": "<slug>", "voice": "5ad4530af205483a88f32eb317d5328a", "blocos": ["texto do bloco 1", ...]}

Saída (commit da Action):
  audio_narracao/<slug>/bloco1.mp3 ...            (áudio, 44,1 kHz 192 kbps)
  videos/<slug>/palavras.json                       ([{"w","t0","t1"}], tempo absoluto, 0,4 s entre blocos)
  videos/<slug>/narracao.json                       ({"audio_blocos": [URLs raw do GitHub], "duracoes": [...]})
Erros: tts_out/erros_*.txt (a Action termina com falha).
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

KEY = os.environ['HEYGEN_API_KEY']
API = 'https://api.heygen.com/v3/models/audio/tts'
RAW = 'https://raw.githubusercontent.com/matheuspdias/stickfigure-videos/main'
PAUSA = 0.4
PONT = re.compile(r'^[^\wÀ-ÿ]+|[^\wÀ-ÿ]+$')


def tts(voice, text):
    body = json.dumps({'text': text, 'voice_id': voice, 'model': 'heygen-voice-1', 'language': 'pt',
                       'with_timestamps': True,
                       'output_format': {'encoding': 'mp3', 'sample_rate_hertz': 44100, 'bitrate_bps': 192000}}).encode()
    for attempt in range(5):
        req = urllib.request.Request(API, data=body, method='POST',
                                     headers={'X-Api-Key': KEY, 'Content-Type': 'application/json', 'Accept': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                j = json.load(r)
                return j.get('data', j)
        except urllib.error.HTTPError as e:
            msg = e.read().decode(errors='replace')[:400]
            if e.code in (429, 500, 502, 503, 504) and attempt < 4:
                time.sleep(5 * (attempt + 1)); continue
            raise RuntimeError(f'HTTP {e.code}: {msg}')
        except urllib.error.URLError:
            if attempt < 4:
                time.sleep(5); continue
            raise


def palavras(chars, offset):
    """original_characters ([{text,start_time,end_time}]) -> palavras sem pontuação, em tempo absoluto."""
    out, cur = [], []

    def fecha():
        if cur:
            w = PONT.sub('', ''.join(c['text'] for c in cur))
            if w:
                out.append({'w': w, 't0': round(cur[0]['start_time'] + offset, 3), 't1': round(cur[-1]['end_time'] + offset, 3)})
        cur.clear()
    for c in chars:
        if c['text'].isspace() or c['text'] in ('—', '–'):
            fecha()
        else:
            cur.append(c)
    fecha()
    return out


def main():
    erros = []
    if not os.path.isdir('tts_in'):
        return 0
    for f in sorted(os.listdir('tts_in')):
        if not f.endswith('.json'):
            continue
        spec = json.load(open(f'tts_in/{f}', encoding='utf-8'))
        slug, voice = spec['slug'], spec.get('voice', '5ad4530af205483a88f32eb317d5328a')
        adir = f'audio_narracao/{slug}'
        os.makedirs(adir, exist_ok=True)
        os.makedirs(f'videos/{slug}', exist_ok=True)
        try:
            todas, urls, durs, t = [], [], [], 0.0
            for n, texto in enumerate(spec['blocos'], 1):
                d = tts(voice, texto)
                dest = f'{adir}/bloco{n}.mp3'
                for attempt in range(4):
                    try:
                        urllib.request.urlretrieve(d['audio_url'], dest); break
                    except Exception:
                        time.sleep(3)
                dur = float(d['duration'])
                chars = d.get('original_characters') or d.get('normalized_characters') or []
                if not chars:
                    raise RuntimeError('a resposta veio sem tempos (original_characters)')
                todas += palavras(chars, t)
                urls.append(f'{RAW}/{dest}')
                durs.append(round(dur, 3))
                t += dur + PAUSA
                print('ok', slug, f'bloco {n}', round(dur, 2), 's', flush=True)
            json.dump(todas, open(f'videos/{slug}/palavras.json', 'w', encoding='utf-8'), ensure_ascii=False)
            json.dump({'audio_blocos': urls, 'duracoes': durs}, open(f'videos/{slug}/narracao.json', 'w'), indent=1)
            os.remove(f'tts_in/{f}')
        except Exception as e:
            erros.append(f'{slug}: {e}')
            print('ERRO', erros[-1], flush=True)
    if erros:
        os.makedirs('tts_out', exist_ok=True)
        open(f'tts_out/erros_{int(time.time())}.txt', 'w').write('\n'.join(erros) + '\n')
    return 1 if erros else 0


if __name__ == '__main__':
    sys.exit(main())
