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
- Personagem principal: `hero(...)`, com camiseta amarela e topete. Segundo personagem: `other(...)`, com camiseta azul e cabelo espetado.
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
`check_icon`, `x_icon`, `big_x(s)`, `qmark`, `exclaim`, `bulb`, `sparkle(r)`, `sweat`, `thought(w, h, tx, ty)`, `speech(w, h, tx, ty)`,
`clipboard(title)`, `subscribe_btn(done)`, `bell`, `cursor`, `envelope`, `donut(pct)`, `speed_lines(t)`, `neq`, `eq`.

Precisa de um objeto novo? Escreva uma função `def objeto(c): ...` no `engine.py`, centrada em (0, 0), usando
`poly / rrect / circle / ellipse` + `fs(c, cor_preenchimento, espessura)`, contorno `INK` de 5-6 px. Assim ela fica disponível para os próximos vídeos.

## Efeitos sonoros
Os efeitos são sintetizados por código (`sfx.py`), sem bancos de som, e entram **automaticamente** no `build`:
pop quando um elemento surge (`anim="pop"`), pancada nos carimbos e quedas (`stamp`, `drop`), swish nas entradas deslizantes e setas,
e whoosh na troca de cena. O volume é ajustado sozinho para ficar 12 dB abaixo do pico da narração.
- Mais alto ou mais baixo: `SFX_DB=8 python render.py build ...` (menor = mais alto).
- Sons extras no `scenes.py`: `SFX = [(t, "ding"), (t, "boom"), ...]`. Disponíveis: `pop thud swish whoosh dark_whoosh impact boom key click ding shimmer bell heartbeat gust riser`.
- Desligar os automáticos: `SFX_OFF = True` no `scenes.py`.
