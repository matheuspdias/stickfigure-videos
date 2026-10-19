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
6. Encerramento sem narração (Tela final do YouTube): junte os blocos com `python juntar_blocos.py saida.wav b1.mp3 b2.mp3 ... --cauda 15` e deixe a última cena com áreas livres (vídeo à esquerda, inscrever-se à direita).
7. Renderizar o vídeo final:
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
`clipboard(title)`, `subscribe_btn(done)`, `bell`, `cursor`, `envelope`, `donut(pct)`, `speed_lines(t)`, `neq`, `eq`,
`beach_chair(sun)` (viver de renda), `cart` (carrinho, inflação), `finish_flag(h)` (chegada, base em y=0), `lever(k, col, label)` (alavanca),
`video_card(title, sub, icon=...)` (miniatura de vídeo) e `play_btn(r)`.
Novos (alugar-ou-comprar): `apartment(col, sign, floors)` (prédio, base em y=0; `sign="ALUGA-SE"`), `balance(tilt, lfn, rfn)` (balança de dois pratos),
`brick` (tijolo), `moving_box` (caixa de mudança) e `house_key(col)` (chave).
Novo (dez-reais-por-dia): `sandwich` (lanche/hambúrguer, gasto pequeno do dia a dia).

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
O padrão são **cortes selecionados e independentes**: 3 a 5 trechos fortes do vídeo, cada um entendido sozinho,
com um gancho no começo. Nada de "PARTE X DE N": quem chega pelo Para Você no meio de uma série pula o vídeo.

1. **Escolher os trechos** (já no roteiro): parágrafos que se entendem sem o resto do vídeo, entregam uma
   conclusão e somam de 1 a 3 min. Critério: alguém que nunca viu o canal entende o assunto nos primeiros 5 s?
   O trecho fecha com uma resposta? Tem mais de 1 min? Os melhores costumam ser as contas com número chocante.
2. **Gancho de cada corte**: uma frase de 4 a 7 s, escrita para quem não viu o vídeo ("Esse apartamento de
   trezentos mil vai te custar quase setecentos."). Todos os ganchos vão num **bloco extra no HeyGen**, um depois
   do outro com `[long pause]` entre eles; guarde os `word_timestamps` para saber onde cada um começa e termina.
3. `python cortes.py videos/<slug> --frases` lista as frases com o tempo (¶ = começo de parágrafo).
4. Crie `videos/<slug>/cortes.json` (formato completo no topo do `cortes.py`):
```json
{"serie": "ALUGAR OU COMPRAR?", "cortes": [
 {"id": "custo-real", "inicio": 74.5, "fim": 161.0, "titulo": "ALUGAR OU\\NCOMPRAR?",
  "gancho": "Esse apartamento de trezentos mil vai te custar quase setecentos.",
  "gancho_audio": [0.0, 4.1], "gancho_tela": "NÃO CUSTA\\NR$ 300 MIL", "gancho_t": 96.0,
  "titulo_post": "Título curto do Shorts/Reels",
  "capa": ["NÃO CUSTA", "R$ 300 MIL"], "post": "Gancho do post... #financas #dinheiro #fazaconta"}
]}
```
5. Gere:
```bash
python cortes.py videos/<slug> out/<slug>.mp4 --audio <mp4 com o áudio final> --ganchos <bloco_ganchos.mp3>
python capas.py videos/<slug> out/<slug>.mp4 --grade
```
- Cada corte (1080x1920): fundo desfocado, título do corte no topo, o vídeo no meio, legendas palavra por palavra.
  Abre com o gancho falado sobre o quadro `gancho_t` parado, com `gancho_tela` grande na tela; depois entra o
  trecho e, no fim, "VÍDEO COMPLETO NO YOUTUBE". Sem `--ganchos`, o texto do gancho fica nos primeiros 3,5 s.
- `inicio` e `fim` são ajustados sozinhos para o silêncio antes da frase mais próxima (até 2 s).
- Saída: `out/<slug>_corte_<id>.mp4` e `out/<slug>_cortes.txt` (duração, avisos fora de 62 s a 2:58, título do Shorts e descrição).
  `--so <id>` gera só um corte.
- **Modo antigo** (partes em sequência, "PARTE X DE N"): sem `cortes.json`, ou com `--sequencial`. Opções:
  `--partes N`, `--max 170`, `--cortes 160.5,308.2`, `--so 1`.
- Tema (cores, fontes, nome do canal) em `THEME` no `cortes.py`, sobrescrito por `tema_cortes.json` quando existir.

## Capas dos cortes
Com `cortes.json`, as capas saem dele (chave `capa` de cada corte; a cena é `gancho_t`): primeira linha grande no
topo, a cena no meio e as outras linhas embaixo, sem "PARTE X DE N". Saída `out/capas/<slug>_capa_<id>.png`.

Modo antigo: depois dos cortes, crie `videos/<slug>/capas.json` (uma entrada por parte, na mesma ordem dos cortes):
```json
{"serie": "NOME CURTO DA SÉRIE", "partes": [{"t": 155, "gancho": ["LINHA 1", "LINHA 2", "LINHA 3"]}]}
```
e rode `python capas.py videos/<slug> out/<slug>.mp4 --grade`.
- `t` é o segundo do vídeo 16:9 com a cena da capa (personagem + número ou imagem forte daquela parte); `gancho` tem 1 a 3 linhas curtas (a primeira sai na cor de destaque).
- Cada capa (1080x1920): série, "PARTE X DE N" grande, a cena e o gancho, sobre o quadro desfocado. O essencial fica entre y 240 e 1680 (a grade do TikTok corta topo e rodapé).
- Saída: `out/capas/<slug>_capa_parteN.png` e `out/capas/<slug>_capas_grade.png` (para conferir). Cores e fontes vêm do tema (`tema_cortes.json`, chave extra `capa_bg` para a cor do fundo).

## Vídeo só para TikTok (vertical nativo, sem versão longa)
Quando o vídeo é só para TikTok/Shorts/Reels, ele é desenhado direto em **1080x1920**:
1. No `scenes.py`, declare `VERTICAL = True` (logo depois do `from engine import *`). O `render.py` lê isso e liga
   `SF_VERTICAL=1`, que deixa `W, H = 1080, 1920`; `title()` centraliza em `W / 2`; as grades de prévia saem 4x2.
2. Layout vertical: título y~250, palco y 360-1290 (pés dos bonecos em ~1290), legendas em y~1460, abaixo de 1500
   fica a interface do TikTok. Nada importante em x > 930 (botões da direita). Modelo: `videos/reserva-emergencia/`.
3. `python render.py build videos/<slug>/scenes.py <narracao.wav> out/<slug>_base.mp4`
4. `python tiktok.py videos/<slug> out/<slug>_base.mp4 out/<slug>_tiktok.mp4` queima as legendas palavra por palavra
   (precisa de `videos/<slug>/palavras.json` com os word_timestamps do HeyGen).
5. Capa: um `capa.py` com `VERTICAL = True` e `SCENES = [(0, 999, capa)]`, renderizada com `render.py stills`.

## Publicação automática
O canal pode rodar sozinho no YouTube: uma tarefa agendada do Claude faz o vídeo longo de segunda e quinta e coloca em `fila/`, e o GitHub Actions renderiza, envia agendado para as 9h e agenda 3 Shorts. Configuração e uso em `automacao/README.md`; instruções da tarefa em `automacao/AUTOMATICO.md`.
