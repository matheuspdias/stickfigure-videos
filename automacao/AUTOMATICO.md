# Modo automático do Faz a Conta

Este é o roteiro que a **tarefa agendada** segue todo domingo e quarta para deixar pronto o vídeo longo de **segunda e quinta (9h)**, com 3 Shorts.
O Matheus não vai acompanhar: ninguém responde perguntas durante a execução.

Siga a skill `stickfigure-video` no **modo YouTube** (ou o `README.md` + `VOZ.md` deste repo) com as diferenças abaixo. Onde as duas conflitarem, vale este arquivo.

## Como o vídeo chega ao YouTube

```
tarefa agendada (Claude)                     GitHub Actions (.github/workflows/publicar.yml)
pesquisa, roteiro, narração no HeyGen,  -->  baixa os áudios do HeyGen, junta os blocos
ganchos dos Shorts, cenas, prévias,          (com 5 s de cauda), renderiza o MP4, envia ao
thumbnail, textos, cortes.json,              YouTube agendado para as 9h, renderiza 3 cortes
commit de fila/<slug>.json + push            e agenda cada um como Short (1 por dia, 12h)
```

O ambiente da tarefa **não consegue baixar** os áudios do HeyGen. Não tente, e não peça ao Matheus: quem baixa é o GitHub Actions.

## Regras do modo automático

- **Nunca pare para perguntar.** Tome a decisão mais razoável e anote no resumo final.
- **Erro do HeyGen** (créditos, timeout, recusa): não tente de novo nem gere a narração por outro caminho. Não coloque nada na fila. Mande o resumo com o erro e pare.
- Se faltar algo para o vídeo ficar bom, prefira **não publicar** (não criar `fila/<slug>.json`) a publicar algo quebrado. Faça commit do que existe em `videos/<slug>/` e explique no resumo.
- **Números certos são o produto do canal.** Toda taxa, preço, regra ou imposto vem de pesquisa feita hoje (Selic, IPCA, CDI, Tesouro, IR, regras de FGTS/MCMV etc.), com fonte oficial quando houver. Rode as contas em Python (como nos `contas.py` dos vídeos anteriores) e confira que os números do roteiro, das cenas e da descrição batem.
- Nada de recomendar produto, banco, corretora ou ação específica, nem prometer ganho. Tom calmo e didático.
- **TikTok: não.** Não gere vídeo curto nativo, capas (`capas.py`) nem arquivos para o Matheus. Só YouTube.

## Passo a passo

### 1. Data e tema
1. Data alvo: o próximo dia de postagem (**segunda ou quinta, 09:00, horário de Brasília**) depois de hoje. Se já houver um vídeo para essa data em `fila/` ou `fila/publicados/` (campo `publicar_em`), pare: não é para gerar dois.
2. Leia `automacao/temas.md`, liste `videos/` e os títulos em `fila/publicados/`. **Não repita** vídeo longo já feito.
3. Escolha um tema de finanças pessoais com uma conta que surpreende e serve para a vida real (meta de dinheiro, comparação com resultado, custo escondido de uma decisão, hábito visto pelo lado do dinheiro). O que mais funcionou: contas de meta com número que surpreende e histórias com dois personagens que fazem escolhas diferentes. Use a seção "Ideias" se houver algo lá. Os temas que só saíram no TikTok podem virar vídeo longo com a conta mais completa.
4. Varie em relação aos dois últimos vídeos (assunto e formato). Quando fizer sentido, ligue a um vídeo anterior ("continuação do vídeo ..."), como o de viver de renda fez com o de 100 mil.
5. Acrescente o tema em "Já feitos no YouTube" no `temas.md`.

### 2. Pesquisa, contas e roteiro
- Pesquise os números do dia e salve as contas em `videos/<slug>/contas.py`.
- 8 a 12 min (~1.300 a 1.900 palavras), números por extenso, parágrafos curtos, voz e tags da skill, **sem `[whispers]`**.
- Salve `videos/<slug>/roteiro.txt`.

### 3. Narração
- `create_speech` com a voz oficial (VOZ.md: Calm Carlos), um bloco por chamada, até ~4.500 caracteres, em paralelo.
- De cada resposta guarde o **link do áudio**, a **duração** e os `word_timestamps`.
- `narracao_blocos.txt`, `transcricao.txt` e `palavras.json` como na skill. Offset de cada bloco = soma das durações anteriores + **0,4 s** por bloco (silêncio entre blocos; o Matheus pediu menos pausa em 22/10/2026). Ponha `# pausa_blocos 0.4` no cabeçalho do `narracao_blocos.txt` (o `cortes.py` lê daí). A cauda de 5 s entra **depois** do último bloco (o publicador passa `--cauda 5` ao `juntar_blocos.py`). O Matheus pediu 5 s em vez de 15 s (22/10/2026): é o mínimo da Tela final do YouTube.

### 3b. Cortes (Shorts) e bloco de ganchos
- Ao escrever o roteiro, escolha **3 trechos** com os três testes da skill (entende-se sozinho nos primeiros 5 s, fecha com uma resposta ou conclusão, dura **de 65 s a 2:40** contando o gancho; acima de 3 min o YouTube não trata como Short e o corte fica de fora). Os melhores: contas com número chocante e comparações com resultado. O mais forte primeiro: ele sai no dia seguinte ao vídeo longo.
- Para cada um, o gancho (4 a 7 s, números por extenso), o `gancho_tela` e as linhas da `capa`, como na skill.
- **Um** bloco extra no HeyGen com os 3 ganchos separados por `[long pause]` (mesma voz e configuração). Guarde link, duração e `word_timestamps`; anote início e fim de cada gancho (folga de 0,1 s) em `videos/<slug>/ganchos.txt`.
- Os Shorts saem com os silêncios acima de 0,25 s encurtados (o `cortes.py` faz isso sozinho pelo áudio, com as legendas acompanhando). Por isso cada corte fica alguns segundos mais curto: mire em pelo menos 70 s de trecho.
- Depois das cenas prontas, confira os tempos com `python cortes.py videos/<slug> --frases` e escreva `videos/<slug>/cortes.json` (formato da skill), com `titulo_post` (título do Short, até ~60 caracteres, com o número que surpreende) e `post` (1 ou 2 frases + 3 a 5 hashtags como #financaspessoais #dinheiro #fazaconta).

### 4. Cenas e revisão
- `videos/<slug>/scenes.py` como na skill: O Consultor em quase toda cena, `SFX` com 3 ou 4 toques e `SFX_SKIP` como em `videos/viver-de-renda/`, e a cena final de encerramento (~5 s sem narração) com áreas livres para a Tela final.
- Em cada trecho de corte, uma cena forte (O Consultor + o número grande) em `gancho_t`, sem nada importante colado nas bordas (x < 140 ou x > 1780).
- A revisão das prévias é **obrigatória e é só sua**: `python render.py sheet ...` com tempos no fim e no meio de todas as cenas. Corrija sobreposições, textos cortados, elementos pequenos e telas vazias, e gere de novo até ficar limpo. Pelo menos duas rodadas.
- Teste mudo curto para pegar erro de código: `python render.py build videos/<slug>/scenes.py silent:20 out/teste.mp4`.

### 5. Thumbnail e textos
- Duas thumbnails em `videos/<slug>/thumb/` (modelos nos vídeos anteriores), escolha a melhor.
- `videos/<slug>/youtube.txt` no formato de `videos/viver-de-renda/youtube.txt`: título, alternativas, descrição com a linha de **Premissas** (taxas e datas usadas), "Conteúdo educativo, não é recomendação de investimento.", capítulos pelos tempos reais das cenas, "Narração gerada com voz de IA.", 2 ou 3 hashtags e as tags.

### 6. Colocar na fila
Escreva `fila/<slug>.json`:

```json
{
  "slug": "<slug>",
  "publicar_em": "2026-10-26T09:00:00-03:00",
  "audio_blocos": ["<link do bloco 1>", "<link do bloco 2>"],
  "duracoes": [132.911, 150.204],
  "pausa_blocos": 0.4,
  "cauda": 5,
  "titulo": "<título escolhido>",
  "descricao": "<descrição completa>",
  "tags": ["tag 1", "tag 2"],
  "thumbnail": "videos/<slug>/thumb/<arquivo escolhido>.png",
  "categoria": "27",
  "ganchos_audio": "<link do bloco de ganchos>",
  "ganchos_duracao": 32.7
}
```

- `audio_blocos` e `duracoes` na **mesma ordem** dos blocos. O publicador confere cada duração e recusa se não bater.
- Valide os JSONs (`python -m json.tool fila/<slug>.json` e `videos/<slug>/cortes.json`).

### 7. Commit e push
- Commit de `videos/<slug>/` (sem áudio), `automacao/temas.md` e `fila/<slug>.json` na `main`, e push. Se recusar por mudança de outra sessão: `git pull --rebase` e push de novo.
- O push dispara o workflow "Publicar no YouTube" (~40 a 60 min com os Shorts).

### 8. Resumo final (SendUserMessage)
Curto, em português:
- título, tema e a conta principal (o número que surpreende), duração;
- quando vai ao ar (dia e 9h) e os 3 Shorts (título de cada um; saem às 12h nos dias seguintes);
- as premissas usadas (taxas e datas), para ele conferir de olho;
- como vetar: até o horário, no YouTube Studio > Conteúdo, o vídeo aparece como "Programado";
- qualquer decisão tomada sozinho ou problema encontrado.
