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
- **Um vídeo de cada tipo por dia**, variando ao longo da semana:
  - **10h**: conta rápida com número que surpreende, comparação com resultado ou POV do dia a dia (60 a 90 s);
  - **18h**: episódio da série "O que ninguém te conta antes de..." (a cada 3 ou 4 dias, ~2 min) ou história com dois personagens que fazem escolhas diferentes (Ana x Bruno, Carla x Diego).
- Aproveite datas do mês (13º, Black Friday, IPVA, IR, férias) quando estiverem perto.
- **Não repita** tema nem ângulo de "Já feitos". Respeite "Não fazer" (principalmente: nada de meta de poupança irreal para quem ganha pouco; valores pequenos e práticos).
- Tire o tema usado da "Fila do Matheus" e acrescente os dois em "Já feitos" com o slug.

### 3. Pesquisa e roteiro (skill, T1)
- Pesquise na web números e regras que podem ter mudado (juros, Selic, IPCA, tabelas do INSS e do IR, regras de programas). Confira cada conta em código (`videos/<slug>/contas.py`) e use números redondos.
- Gancho nos 2 primeiros segundos, frases curtas, números por extenso, virada no meio, **fecha com pergunta para comentário**. 150 a 230 palavras (60-90 s); episódio da série até ~2 min.
- Salve `videos/<slug>/roteiro.txt`.

### 4. Narração
- Um bloco por vídeo no HeyGen, voz oficial (VOZ.md: Calm Carlos, ElevenLabs v4, pt, velocidade 1.0), **sem `[whispers]`**. Gere os dois em paralelo.
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
 "audio_blocos": ["<link do HeyGen>"], "duracoes": [74.2]}
```
Valide com `python -m json.tool`.

### 7. Commit e push
Commit de `videos/<slug>/` (sem áudio), `automacao/temas_tiktok.md` e `fila_tiktok/*.json` na `main` e push (se recusar: `git pull --rebase` e push de novo). O push dispara o workflow "TikTok automático" (~5 a 10 min por vídeo).

### 8. Esperar, baixar e entregar
- A cada 60 s, por até 50 min, confira se a release saiu: `curl -s https://api.github.com/repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>` (ou `gh api repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>`). Se o workflow falhar, leia `fila_tiktok/ultimo_log.txt` depois de `git pull`, corrija o que for do seu lado (cena, JSON) e faça push de novo.
- Baixe `<slug>_tiktok.mp4`, `<slug>_capa.png` e `<slug>_post.txt` da release e confira 2 ou 3 quadros do MP4 (gancho, meio, fim).
- Entregue com **SendUserFile** (status `proactive`): primeiro o vídeo e a capa das **10h**, depois os das **18h**.
- Termine com **SendUserMessage** curto, em português:
  - **10h:** título + a legenda pronta para copiar (do post.txt);
  - **18h:** título + a legenda pronta para copiar;
  - lembretes de uma linha: ativar o selo de conteúdo gerado por IA (voz), postar à mão e subir o mesmo arquivo como Shorts e Reels se quiser;
  - qualquer decisão tomada sozinho (tema, número estimado) ou problema.
