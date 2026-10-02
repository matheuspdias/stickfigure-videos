# stickfigure-videos

Gera vídeos explicativos no estilo **bonequinho de palito (stick figure)** sincronizados com uma narração, para YouTube (1920x1080, 30 fps).

Entrada: **transcrição com tempos** + **áudio da narração**. Saída: **MP4 pronto** (~20 MB para 4 min).

Tudo é desenhado em código (pycairo): sem bancos de imagem, sem direitos autorais de terceiros.

## Instalação

```bash
./setup.sh          # pycairo, numpy e fontes (Permanent Marker, Patrick Hand). Requer ffmpeg.
```

## Fluxo de trabalho para um vídeo novo

1. Criar a pasta `videos/<slug>/` com `transcricao.txt` (formato `(m:ss) frase...`).
2. Dividir a narração em **cenas** de ~3 a 20 s, uma ideia visual por cena.
3. Escrever `videos/<slug>/scenes.py` (use `examples/carro-5000/scenes.py` como modelo):
   cada cena é uma função `sNN(c, t)` desenhada em **tempo absoluto do áudio**, e no fim vem a lista
   `SCENES = [(inicio, fim, funcao), ...]` (a última cena termina em `999.0`).
4. Para cada elemento, use o horário em que a narração **menciona** aquilo (de +0,2 a +0,5 s depois do tempo da frase).
5. Gerar prévias e conferir o layout:
   ```bash
   python render.py sheet videos/<slug>/scenes.py out/preview.png 7.5 17.5 26 33.5 ...
   ```
   Escolha tempos perto do **fim** de cada cena, quando todos os elementos já apareceram.
   Verifique sobreposições, textos cortados e elementos pequenos demais.
6. Renderizar o vídeo final:
   ```bash
   python render.py build videos/<slug>/scenes.py audio.mp3 out/<slug>.mp4
   ```

## Padrões de estilo

- Fundo papel (`PAPER`), traço preto (`INK`), cores de destaque: `GREEN` (dinheiro/positivo), `RED` (custo/erro),
  `YELLOW`, `BLUE`, `ORANGE`, `PURPLE`. Fundos de marca-texto: `LYELLOW`, `LGREEN`, `(1, 0.8, 0.76)` (rosado).
- Títulos: `MARKER` (Permanent Marker). Rótulos e frases: `HAND` (Patrick Hand).
- **Personagem fixo do canal: O Consultor** (`hero(...)`): camisa azul-marinho (`NAVY`), gravata dourada (`GOLD`), óculos retangulares e cabelo de lado. Ele aparece em todos os vídeos.
  - Objeto na mão é **opcional por cena** (padrão: nenhum): `hero(..., prop=("l", prop_tablet))`. Use o tablet com gráfico para investimento ou crescimento, `prop_calculator` para contas, `prop_coin` para economizar e `prop_pointer` para explicar. Pode trocar de objeto no meio do vídeo, por exemplo com duas chamadas por intervalo de tempo.
  - Segundo personagem: `other(...)` (camiseta azul, cabelo espetado). Boneco do vídeo piloto: `hero_classic(...)`.
  - Paleta da marca: azul-marinho + dourado, com verde só para dinheiro e positivo e vermelho para custo e erro.
- As fontes **não têm** os glifos `≠ ≈ → ↓ ✓`. Use `neq()`, `eq()`, `arrow()`, `check_icon()` ou texto por extenso.
- Área útil: título em y≈110-150, conteúdo entre y 220 e 1000, bonecos com os pés em y≈960-1060.

## Referência rápida (engine.py)

**Animação**: `show(c, t, t0, x, y, fn, s=1, anim="pop"|"fade"|"up"|"left"|"right"|"drop"|"stamp", d=0.45, t1=None, rot=0)`
desenha `fn(c)` centrado em (x, y) a partir de `t0`. `t1` faz o elemento sumir com fade.
`arrow_draw(c, t, t0, x1, y1, x2, y2)` desenha uma seta que cresce.

**Composição**: `sc(fn, *args, s=escala)`, `group(f1, f2, ...)`, `at(dx, dy, fn)`, `icon_label(fn, "rótulo", size, dy, s=escala)`,
`T("texto", size, cor)` (fonte manuscrita), `M("texto", size, cor)` (marcador), `title(c, t, t0, "texto", y, size)`,
`hl(c, "texto", x, y, size, bg)` (marca-texto), `ribbon(c, "TEXTO", col)` (faixa), `price_tag(c, "R$ 60.000")`.

**Bonecos**: `hero(c, t, x, y_pes, escala, poses=[(t, "pose"), ...], exprs=[(t, "expr"), ...], appear=t0, look=-1..1 ou função)`.
- Poses: `stand relax point_r point_ru point_l point_lu think think_l hips shrug arms_up head thumb finger_up present present_l wave hold run`
- Expressões: `happy grin neutral worried shocked desperate think confident sad angry`

**Objetos** (centrados em 0,0, cerca de 150-300 px):
`car(col, ghost)`, `bill`, `bills(n)`, `coin`, `gas_pump`, `shield`, `document(title)`, `wrench`, `tire`, `wrench_tire`,
`parking`, `toll`, `house(big)`, `card`, `bank`, `percent`, `clock(t)`, `calendar(num, top)`, `piggy(col)`, `calculator(disp)`,
`snowball(r)`, `mattress`, `tree(k)` (0 broto a 1 com frutos), `gear(r, col)`, `bar(h, w, col, label, top)` (barra com base em y=0),
`check_icon`, `x_icon`, `big_x(s)`, `qmark`, `exclaim`, `bulb`, `sparkle(r)`, `sweat`, `thought(w, h, tx, ty)`, `speech(w, h, tx, ty)`,
`clipboard(title)`, `subscribe_btn(done)`, `bell`, `cursor`, `envelope`, `donut(pct)`, `speed_lines(t)`, `neq`, `eq`.

Precisa de um objeto novo? Escreva uma função `def objeto(c): ...` no `engine.py`, centrada em (0, 0), usando
`poly / rrect / circle / ellipse` + `fs(c, cor_preenchimento, espessura)`, contorno `INK` de 5-6 px. Assim ela fica disponível para os próximos vídeos.

## Efeitos sonoros
Padrão do Faz a Conta: **nenhum som automático**. O "whoosh" de transição era feito de ruído e soava como chiado por cima da voz, então foi removido.
Use só **3 ou 4 toques por vídeo**, à mão, nos momentos-chave, com sons sem ruído:
`SFX = [(t, "tum"), (t, "soft_ding")]`. Use `tum` na revelação de um número importante e `soft_ding` num momento positivo.
Outros sons disponíveis em `sfx.py`: `pop thud ding bell click`. Evite `swish whoosh gust`, que são feitos de ruído.
O volume é ajustado sozinho para ficar 12 dB abaixo do pico da narração (`SFX_DB=...` para mudar).
O áudio final sai em AAC 256 kbps. Abaixo disso a voz ganha artefatos nos agudos.

## Cortes verticais (TikTok, YouTube Shorts, Reels)
Depois do vídeo 16:9 pronto:
```bash
python cortes.py videos/<slug> out/<slug>.mp4 --audio <mp4 com o áudio final> --titulo "LINHA 1\NLINHA 2"
```
- Divide a história em partes de 62 s a 2:50 (o TikTok só paga vídeo com mais de 1 min; o Shorts aceita até 3 min), cortando no início de uma frase e preferindo começo de bloco ou de parágrafo do `roteiro.txt`.
- Cada parte sai em 1080x1920: fundo com o próprio vídeo desfocado, título e "PARTE X DE N" no topo, o vídeo no meio e legendas grandes palavra por palavra (Montserrat ExtraBold, palavra falada em destaque). No fim entra "CONTINUA NA PARTE X" ou, na última, "HISTÓRIA COMPLETA NO YOUTUBE".
- Tempos das palavras: `videos/<slug>/palavras.json` se existir; senão são estimados pelas frases e marcas `[palavra@t]` do `narracao_blocos.txt` (quanto mais marcas, melhor a sincronia).
- Opções: `--partes N`, `--max 170`, `--cortes 160.5,308.2` (manual), `--so 1` (só uma parte, para prévia).
- Saída: `out/<slug>_parteN.mp4` (~10 MB cada) e `out/<slug>_cortes.txt` com os tempos.
- Tema (cores, fontes, nome do canal) em `THEME` no `cortes.py`, sobrescrito por `tema_cortes.json` quando existir.
