# Modo automático do TikTok do Faz a Conta

Roteiro da tarefa agendada **"Faz a Conta TikTok automático"**, que roda todo dia por volta das **19h** e deixa prontos os **2 vídeos do dia seguinte** (o Matheus revisa à noite e posta às **10h** e às **18h**). Mudou de madrugada para 19h em 07/11/2026, a pedido do Matheus, para dar tempo de revisar.
O Matheus não acompanha a produção: ninguém responde perguntas. Ele só abre a conversa da tarefa, baixa os arquivos e **posta à mão** (o agendamento do TikTok trava as views; nunca tente postar).

Siga a skill `stickfigure-video` no **Modo TikTok** (ou o `README.md` + `VOZ.md` deste repo) com as diferenças abaixo. Onde conflitarem, vale este arquivo.

## Como o vídeo chega ao Matheus

```
tarefa agendada (Claude)                         GitHub Actions (.github/workflows/tiktok.yml)
temas, pesquisa, roteiros, narração no HeyGen,   baixa a narração, junta, renderiza o vertical,
cenas, prévias, capa, post.txt,          -->     queima as legendas, gera a capa e publica a
commit de fila_tiktok/<slug>.json + push         release "tiktok-<slug>" (MP4 + capa + post)
        |                                                         |
        +---- espera a release, baixa os arquivos e manda no chat <+
```

Este ambiente **não baixa** o áudio do HeyGen (quem baixa é o Actions), mas **consegue baixar da release** do GitHub (o repositório é público):
`curl -sSL -o <arquivo> https://github.com/matheuspdias/stickfigure-videos/releases/download/tiktok-<slug>/<arquivo>`.

## Regras

- **Nunca pare para perguntar.** Decida e anote na mensagem final.
- **Erro do HeyGen** (créditos, timeout): não tente de novo. Entregue o que der (se um dos dois saiu, entregue esse) e avise.
- Prefira **não entregar** um vídeo quebrado a entregar com erro de conta, legenda errada ou cena vazia.
- Entregue o quanto antes (o ideal é até umas **21h**, para o Matheus revisar à noite). O limite absoluto é **9h30** do dia da postagem. Entregue primeiro o das 10h assim que ficar pronto e depois o das 18h.
- Se o Matheus responder pedindo ajuste numa cena, corrija o `scenes.py`, rode o workflow de novo para aquele slug (aba Actions, `workflow_dispatch` com o slug, ou recoloque o JSON em `fila_tiktok/`) e reenvie.

## Passo a passo

### 1. Data e checagem
1. Data alvo (horário de Brasília): se esta execução começou depois das 9h30, a data alvo é **amanhã** (é o caso normal, rodando às 19h); se começou antes das 9h30 (execução manual de madrugada), é **hoje**.
2. Veja `fila_tiktok/` e `fila_tiktok/feitos/` (campos `data` e `horario`). Para cada horário (10:00 e 18:00) da data alvo:
   - se já existe em `feitos/` com `release`: só baixe e entregue de novo (passo 8), sem produzir;
   - se está em `fila_tiktok/` (Actions ainda rodando ou falhou): veja `fila_tiktok/ultimo_log.txt`; espere ou explique o erro;
   - se não existe: produza.

### 2. Temas (2 por dia)
- Leia `automacao/temas_tiktok.md`. Use primeiro a **"Fila do Matheus"**, na ordem. Depois, a série e as ideias.
- **Um vídeo de cada tipo por dia** (mudou em 13/11/2026, a pedido do Matheus):
  - **10h: formato "E se..."** (todo dia, com música; regras em 2c);
  - **18h**: episódio da série "O que ninguém te conta antes de..." (a cada 3 ou 4 dias, ~2 min); nos outros dias, história com dois personagens que fazem escolhas diferentes (Ana x Bruno, Carla x Diego), conta rápida com número que surpreende ou POV do dia a dia (60 a 90 s).
- Aproveite datas do mês (13º, Black Friday, IPVA, IR, férias) quando estiverem perto.
- **Não repita** tema nem ângulo de "Já feitos". Respeite "Não fazer" (principalmente: nada de meta de poupança irreal para quem ganha pouco; valores pequenos e práticos).
- Tire o tema usado da "Fila do Matheus" e acrescente os dois em "Já feitos" com o slug.

### 2b. Estilo viral (pedido do Matheus em 09/11/2026: vale para todos os vídeos)
- **Tema que divide opinião**: algo em que metade das pessoas discorda (carro x app, aluguel x financiar, casamento x apê, morar com os pais). Prefira esses a temas "neutros".
- **Gancho provocativo nos 2 primeiros segundos**, em forma de afirmação ou pergunta que incomoda: "Seu carro custa mais que um aluguel.", "Pagar aluguel é jogar dinheiro fora? A resposta vai irritar muita gente." A frase do gancho já está enorme na tela no 1º quadro.
- **Virada no meio** que contraria o senso comum ("praticamente empate", "não é burrice, mas...") e **conclusão honesta** com as condições em que cada lado ganha (nunca "um lado é burro").
- **Fecha chamando para o lado**: "Time Ana ou time Bruno? Comenta", "Defende o seu lado nos comentários".
- Continua valendo "Não fazer" (sem política, apostas, promessa de ganho, metas irreais, recomendar produto/banco) e contas conferidas em `contas.py`.

### 2c. Formato "E se..." (10h, todo dia; pedido do Matheus em 13/11/2026)
Modelo pronto: `videos/milhao-por-dia-1500/` (roteiro, cenas, capa, post). Inspirado num vídeo viral de "R$ 1 trilhão no Pix".
- **Gancho de fantasia** na 1ª frase: "E se você ganhasse/acordasse com/guardasse...?" com um número grande e concreto.
- **O número vira coisa**, uma cena nova a cada 2-3 s: pilha de notas que sobe até um avião/o espaço, peso em toneladas numa balança,
  anos contando uma nota por segundo, contador de dias, calendário girando, comparação com algo conhecido (Torre Eiffel, estádio).
- **Virada** no meio ("Parece muito? Mas olha a virada") e **um detalhe de juros/rendimento** no fim (CDI do momento, já sem IR).
- Fecha com **"o que você fazia primeiro?"** (ou pergunta parecida que faça a pessoa se imaginar). 60 a 80 s.
- Personagem principal "você" = `pessoa(..., "lucas")`; o Consultor aparece em 1 ou 2 cenas. Fundos de cor sólida (`fundo_marca`) + poucas cenas de cenário.
- Números pesquisados e conferidos em `contas.py`; quando for estimativa (peso, espessura, revenda), a narração diz "uns"/"quase".
- Continua valendo "Não fazer": nada de loteria/apostas como fantasia (Mega da Virada etc.), nem promessa de ficar rico.
- No JSON da fila, ponha `"musica": "happy_nation_slowed"`: o Actions mistura a música (Happy Nation slowed + reverb, volume já ajustado)
  e publica `<slug>_tiktok.mp4` (com música) e `<slug>_sem_musica.mp4` (para Shorts/Reels, onde a música da gravadora é silenciada).
  A música fica cifrada em `musica/` e precisa do segredo `MUSICA_SENHA` no GitHub; sem ele, o vídeo sai sem música (o log avisa): diga isso ao Matheus.
- Ideias: lista "Formato E se..." em `automacao/temas_tiktok.md`.

### 3. Pesquisa e roteiro (skill, T1)
- Pesquise na web números e regras que podem ter mudado (juros, Selic, IPCA, tabelas do INSS e do IR, regras de programas). Confira cada conta em código (`videos/<slug>/contas.py`) e use números redondos.
- Gancho nos 2 primeiros segundos, frases curtas, números por extenso, virada no meio, **fecha com pergunta para comentário**. 150 a 230 palavras (60-90 s); episódio da série até ~2 min.
- Salve `videos/<slug>/roteiro.txt`.

### 4. Narração
- Um bloco por vídeo no HeyGen, voz oficial (VOZ.md: Afonso desde 13/11/2026, pt), **sem `[whispers]`**. Gere os dois em paralelo.
- Guarde o **link**, a **duração** e os `word_timestamps` → `videos/<slug>/palavras.json` (`[{"w", "t0", "t1"}]`, sem `<start>`/`<end>`).

### 5. Cenas, capa e post (skill, T3 a T5), no estilo ilustrado
- `videos/<slug>/scenes.py`: `from engine import *`, `VERTICAL = True`, `from ilustrado import *`, `STYLE = "ilustrado"`, `SFX_OFF = True` ou `SFX_SKIP` como no modelo e 3 ou 4 toques. Modelo: `examples/ilustrado-tiktok/scenes.py`.
- Cenários de vida real e `fundo_marca`, números com `contador`/`barras_i`/`grafico_curva`, telas de banco e fatura; O Consultor grande (escala 1.3-1.5), algo novo na tela a cada ~2 s.
- Revisão **obrigatória**: `python render.py sheet ...` no fim e no meio das cenas, pelo menos duas rodadas, corrigindo sobreposições e qualquer coisa abaixo de y 1500 ou à direita de x 930. Teste mudo curto: `python render.py build videos/<slug>/scenes.py silent:8 out/teste.mp4`.
- `videos/<slug>/capa.py` (modelo `examples/ilustrado-tiktok/capa.py`) e `videos/<slug>/post.txt` (legenda do TikTok com gancho na 1ª linha, 2 ou 3 linhas da conta, pergunta final e 3 a 5 hashtags; título curto para Shorts).

### 6. Fila
`fila_tiktok/<slug>.json` para cada vídeo:
```json
{"slug": "<slug>", "data": "2026-11-08", "horario": "10:00", "titulo": "<título curto>",
 "audio_blocos": ["<link do HeyGen>"], "duracoes": [74.2], "musica": "happy_nation_slowed"}
```
(`"musica"` só no vídeo "E se..." das 10h.)
Valide com `python -m json.tool`.

### 7. Commit e push
Commit de `videos/<slug>/` (sem áudio), `automacao/temas_tiktok.md` e `fila_tiktok/*.json` na `main` e push (se recusar: `git pull --rebase` e push de novo). O push dispara o workflow "TikTok automático" (~5 a 10 min por vídeo).

### 8. Esperar, baixar e entregar
- A cada 60 s, por até 50 min, confira se a release saiu: `curl -s https://api.github.com/repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>` (ou `gh api repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>`). Se o workflow falhar, leia `fila_tiktok/ultimo_log.txt` depois de `git pull`, corrija o que for do seu lado (cena, JSON) e faça push de novo.
- Baixe `<slug>_tiktok.mp4`, `<slug>_capa.png` e `<slug>_post.txt` da release (no das 10h, também `<slug>_sem_musica.mp4`; se ele não estiver na release, a música não entrou: veja o log) e confira 2 ou 3 quadros do MP4 (gancho, meio, fim).
- Entregue com **SendUserFile** (status `proactive`): primeiro o vídeo com música, a versão sem música e a capa das **10h**, depois o vídeo e a capa das **18h**.
- Termine com **SendUserMessage** curto, em português:
  - **10h:** título + a legenda pronta para copiar (do post.txt);
  - **18h:** título + a legenda pronta para copiar;
  - lembretes de uma linha: ativar o selo de conteúdo gerado por IA (voz), postar à mão e, se quiser, subir em Shorts e Reels (o das 10h na versão sem música);
  - qualquer decisão tomada sozinho (tema, número estimado) ou problema.
