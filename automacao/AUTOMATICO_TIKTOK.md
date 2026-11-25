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
- **Um vídeo de cada tipo por dia** (mudou em 16/11/2026, a pedido do Matheus: o Checklist rendeu mais que o "E se..."):
  - **10h: Checklist do Consultor** (todo dia; regras em 2c). O "E se..." saiu da grade (fica só se o Matheus pedir);
  - **18h**: conta útil do momento (regra 2b.2), de preferência em série numerada; episódio da série "O que ninguém te conta antes de..." a cada 3 ou 4 dias (~2 min). Ana x Bruno só quando a escolha dos dois for uma conta útil (ex.: IPVA à vista x parcelado), não opinião.
- Aproveite datas do mês (13º, Black Friday, IPVA, IR, férias) quando estiverem perto.
- **Não repita** tema nem ângulo de "Já feitos". Respeite "Não fazer" (principalmente: nada de meta de poupança irreal para quem ganha pouco; valores pequenos e práticos).
- Tire o tema usado da "Fila do Matheus" e acrescente os dois em "Já feitos" com o slug.

### 2-0. Programa de recompensas do TikTok (desde 15/11/2026, 10 mil seguidores)
- Todo vídeo final com **pelo menos 62 s** (o render falha abaixo disso: aumente o roteiro). Mire em 65 a 80 s.
- Só **vídeo novo e original**: nunca repostar o mesmo vídeo nem recorte de um vídeo antigo do canal.
- **Música só a trilha própria** (`trilha_faz_a_conta`) ou nenhuma. Nada de música de gravadora.
- Só conta quem assiste mais de 5 s: a regra de abrir sem cartaz parado (2b.1) vale dinheiro agora.
- **Legenda começa com a frase que alguém digitaria na busca** (ex.: "13º salário 2026: quanto cai na 2ª parcela"), depois o gancho.
  Busca também conta como visualização qualificada (quando a pessoa assiste 30 s ou mais).
- Selo de conteúdo gerado por IA: continua (o Matheus sempre marca).

### 2a. O que os dados mostraram (13/11/2026) — vale acima de tudo
Análise dos vídeos de 07 a 13/11 (todos parados em 150 a 450 views; o do aluguel, 3.435):
- O TikTok distribuiu normalmente (90-95% "Para você"): não é bloqueio, nem o selo de IA (o Matheus sempre marca e deve continuar marcando). O estilo, sim, pesa: ver 5.
- **A maioria saiu em 0:01**: os vídeos abriam com um cartaz parado (título enorme em fundo escuro + Consultor no holofote), que parece capa/anúncio.
- Temas de opinião (morar com os pais, casamento, lanche e bar) quase não foram salvos nem compartilhados (1 salvamento, 2 compartilhamentos). Os campeões do canal são contas úteis do momento (13º 238 mil, férias 105 mil, apê na planta 57 mil) e séries numeradas (R$ 100 mil 624 mil, aluguel 156 mil).

### 2b. Abertura, temas e séries (regras desde 14/11/2026, a pedido do Matheus)
1. **Sem cartaz de abertura.** Proibido abrir com título grande parado. No quadro 0 a conta já está acontecendo e se mexendo
   (número grande contando, barras subindo, dinheiro saindo da conta, fatura chegando, pilha crescendo) e a narração começa em 0,0 s com o gancho.
   O título vai **pequeno no topo** (size ~56, como no `videos/primeiros-100-mil`, que fez 624 mil). O cartaz com título grande é só para a **capa** (`capa.py`), que o Matheus escolhe na postagem.
   Na revisão do `render.py sheet`, olhe o quadro de 0,0 s: se ele funcionaria como capa parada, refaça.
2. **Tema útil do momento, que dá vontade de salvar e mandar pra alguém** (a 18h, sempre; o "E se..." das 10h continua):
   uma conta que a pessoa precisa fazer agora, com o número dela (salário de R$ 2 mil, 3 mil, 5 mil). Calendário: 2ª parcela do 13º (até 18/12) e o desconto que vem nela,
   Black Friday parcelada, quanto custa o Natal/amigo secreto/ceia, férias de fim de ano, IPVA e IPTU de janeiro (à vista ou parcelado),
   material escolar, IR 2027, aumento do salário mínimo. Polêmica só de vez em quando e sempre com uma conta útil no meio (nada de "vergonha ou estratégia?" sem conta).
3. **Séries numeradas** "(Parte 1)", "(Parte 2)": quando o tema render mais de um vídeo, divida e diga "Parte 2 no perfil" (o TikTok mostrou gente buscando "parte 2 da história alugar ou comprar").
   Continuação natural: série do aluguel (comprar x alugar com os números de 2026) e série dos R$ 100 mil (juros compostos).
- Mantém: virada no meio, conclusão honesta (nunca "um lado é burro"), pergunta no fim, "Não fazer" e contas conferidas em `contas.py`.

### 2c. Checklist do Consultor (10h, todo dia; desde 17/11/2026)
Modelo pronto (caderno, desde 24/11/2026): `videos/checklist-sair-do-rotativo/`. Copie a estrutura do `scenes.py` e troque só o conteúdo. (O antigo `videos/checklist-salario-caiu/` é do estilo ilustrado: não use mais.)
Inspirado nos vídeos de finanças que mais viralizaram em pt-BR (3,2 mi e 2,4 mi de views, 100 mil+ salvamentos cada): lista numerada de passos práticos.
- **UMA cena fixa o vídeo inteiro**: `fundo_marca("navy")` com holofote, o Consultor GRANDE no centro falando com quem assiste
  (`consultor_i(c, t, 540, 2200, 2.4, ...)`, só a parte de cima do corpo), poses e expressões trocando com a fala.
- **A lista "1. 2. 3." (3 a 5 passos) aparece VAZIA no quadro 0** (linhas tracejadas) e vai sendo escrita passo a passo;
  o passo atual fica destacado e vira ✓ verde quando termina. Título pequeno no topo (ex.: "QUANDO O SALÁRIO CAIR").
- **Um valor concreto atravessa o vídeo** num marcador logo abaixo da lista (saldo, 13º, dívida, meta), mudando a cada passo com
  `contador`, e termina num número final em dourado (ex.: "R$ 35 POR DIA"). O quanto entra/sai vira um selo pequeno no canto do marcador.
- Detalhes do passo entram como chips dos lados (x ~230 e ~790, y 940-1100), sem cobrir o rosto. **Nada entre y 1380 e 1560**:
  é onde o Actions queima a legenda.
- Abertura: a situação da pessoa já no quadro 0 (notificação "Salário caiu!", "13º caiu!", fatura chegando) + narração em 0,0 s:
  "Seu salário de R$ 3 mil caiu. Antes de gastar um real, faz esses 3 passos. Salva pra fazer no dia do pagamento."
- Passos **seus**, práticos, com conta (nunca copie a lista de outro criador); um passo com um número que surpreende.
- Fecha com pergunta que a pessoa responde com o número dela ("Qual é o seu número do dia? Comenta aí"). 62 a 80 s.
- **Legenda começa com "salva pro dia 5 📌"** (ou "salva pra quando cair o 13º 📌", "salva antes da Black Friday 📌"), depois a frase de busca,
  os passos escritos com emojis 1️⃣ 2️⃣ 3️⃣ e a pergunta. Capa: título + os passos listados + selo vermelho "SALVA PRO DIA 5".
- Sem música (é a voz do Consultor que segura). Temas: lista "Checklist do Consultor" em `automacao/temas_tiktok.md`.

### 2d. Formato "E se..." (fora da grade desde 16/11/2026; só se o Matheus pedir)
Modelo pronto: `videos/milhao-por-dia-1500/` (roteiro, cenas, capa, post). Inspirado num vídeo viral de "R$ 1 trilhão no Pix".
- **Abre já na cena do número virando coisa** (sem cartaz parado, regra 2b.1). **Gancho de fantasia** na 1ª frase: "E se você ganhasse/acordasse com/guardasse...?" com um número grande e concreto.
- **O número vira coisa**, uma cena nova a cada 2-3 s: pilha de notas que sobe até um avião/o espaço, peso em toneladas numa balança,
  anos contando uma nota por segundo, contador de dias, calendário girando, comparação com algo conhecido (Torre Eiffel, estádio).
- **Virada** no meio ("Parece muito? Mas olha a virada") e **um detalhe de juros/rendimento** no fim (CDI do momento, já sem IR).
- Fecha com **"o que você fazia primeiro?"** (ou pergunta parecida que faça a pessoa se imaginar). 60 a 80 s.
- Personagem principal "você" = `pessoa(..., "lucas")`; o Consultor aparece em 1 ou 2 cenas. Fundos de cor sólida (`fundo_marca`) + poucas cenas de cenário.
- Números pesquisados e conferidos em `contas.py`; quando for estimativa (peso, espessura, revenda), a narração diz "uns"/"quase".
- Continua valendo "Não fazer": nada de loteria/apostas como fantasia (Mega da Virada etc.), nem promessa de ficar rico.
- No JSON da fila, ponha `"musica": "trilha_faz_a_conta"`: o Actions mistura a **trilha própria** do canal (composta por código em
  `musica_fonte/trilha_faz_a_conta.py`, sem música de terceiros) e publica `<slug>_tiktok.mp4` (com música) e `<slug>_sem_musica.mp4`.
  **Nunca use música de gravadora** (Happy Nation etc.), nem misturada aqui nem pelo TikTok: música protegida tocando mais de 1 minuto
  deixa o vídeo fora do programa de recompensas (o Matheus entrou em 15/11/2026). `happy_nation_slowed` fica aposentada.
- Ideias: lista "Formato E se..." em `automacao/temas_tiktok.md`.

### 3. Pesquisa e roteiro (skill, T1)
- Pesquise na web números e regras que podem ter mudado (juros, Selic, IPCA, tabelas do INSS e do IR, regras de programas). Confira cada conta em código (`videos/<slug>/contas.py`) e use números redondos.
- Gancho falado no segundo 0 (sem cartaz parado, ver 2b), frases curtas, números por extenso, virada no meio, **fecha com pergunta para comentário**. 150 a 230 palavras (60-90 s); episódio da série até ~2 min.
- Salve `videos/<slug>/roteiro.txt`.

### 4. Narração (API do HeyGen, pela Action `tts`)
- **Não use as ferramentas do HeyGen desta conversa para a narração** (elas gastavam a assinatura, que foi cancelada).
  A narração sai da API do HeyGen (saldo pré-pago, segredo `HEYGEN_API_KEY`), gerada pela Action `tts`.
- Um bloco por vídeo, voz oficial (VOZ.md: clone B da Calm Carlos, `5ad4530af205483a88f32eb317d5328a`), texto do `roteiro.txt` sem tags.
  Para cada vídeo, crie `tts_in/<slug>.json`:
  ```json
  {"slug": "<slug>", "voice": "5ad4530af205483a88f32eb317d5328a", "blocos": ["<texto do roteiro>"]}
  ```
  Faça commit dos dois pedidos juntos e push. Em 1–2 min a Action commita, para cada slug:
  `audio_narracao/<slug>/bloco1.mp3`, `videos/<slug>/palavras.json` (`[{"w","t0","t1"}]`, pronto para as cenas) e
  `videos/<slug>/narracao.json` (`audio_blocos` e `duracoes` para a fila). Espere com
  `for i in $(seq 1 15); do git pull -q; [ -f videos/<slug>/narracao.json ] && break; sleep 15; done`.
- Se falhar, o pedido fica em `tts_in/` e o erro em `tts_out/`. Erro de saldo ("insufficient", "balance", 402):
  pare e avise o Matheus para colocar saldo na API do HeyGen (platform.heygen.com → Billing). Erro temporário:
  apague `tts_out/`, commit e dispare de novo (`gh api -X POST repos/matheuspdias/stickfigure-videos/actions/workflows/tts.yml/dispatches -f ref=main`).

### 5. Cenas, capa e post (skill, T3 a T5), no estilo CADERNO (palito), desde 24/11/2026
**Por quê (perfil @fazaconta10, aba Popular, 24/11/2026):** dos 18 vídeos mais vistos, 16 são no estilo caderno (papel creme, bonequinho de palito, números à mão): 100 mil 722 mil, "13º não vem inteiro" 248 mil, alugar ou comprar parte 1 248 mil, férias 128 mil, carro 81 mil, planta 73 mil, CLT x PJ 55 mil, demitido 47 mil. Os ilustrados ficaram quase todos entre 150 e 4 mil (exceções: checklist do salário 152 mil, holerite 18,6 mil, 13º de R$ 3 mil 10 mil; o mesmo tema do 13º em palito fez 248 mil). O Matheus decidiu voltar ao caderno no TikTok.
- `videos/<slug>/scenes.py`: `from engine import *` e `VERTICAL = True`, **sem** `from ilustrado import *` e sem `STYLE`. O Consultor é `hero(...)` (camisa navy, gravata dourada, óculos); outras pessoas com `pessoa(...)`/`boneco(...)` do engine. Fundo de papel creme, números grandes em Permanent Marker (`text(..., MARKER, ...)`, `hl(...)` para marca-texto), objetos do engine (`suitcase`, `boleto`, `door`, `crane`, `sofa_back/front`...). `SFX_SKIP` como no modelo e 3 ou 4 toques.
  Modelos que deram certo: `videos/ferias-mes-seguinte/` (128 mil), `videos/decimo-terceiro-quanto-cai/`, `videos/demitido-hoje/`, `videos/planta-mcmv/`; POV: `videos/pov-fatura-janeiro/`.
- **Quadro 0 com a conta em movimento e título pequeno no topo** (regra 2b.1): a tela é uma folha de caderno onde a conta vai sendo escrita; algo novo a cada ~2 s; um número enorme por vez; o Consultor reagindo. Nada de cenário cheio (sala, rua, escritório): o fundo limpo deixa o número ler na hora no celular.
- **Gancho** (os que mais renderam no perfil): número chocante sobre o dinheiro da pessoa ("R$ 395 mil só de juros", "41% do salário no carro"); desmentir o que ela acha ("o seu 13º não vem inteiro", "CLT x PJ: quase igual?"); aviso sobre o que vai acontecer com ela ("férias? cuidado com o mês seguinte"); situação em que ela se coloca ("demitido hoje? quanto cai?"); "por que" ("por que demora tanto no começo?"). Série "Parte X de 4": só a parte 1 explode (248 mil -> 5,6 mil na parte 4), então a parte 1 tem de fechar sozinha.
- **Sem exceção (24/11/2026, pedido do Matheus: "quero todos os vídeos no formato de palitinho"):** o Checklist do Consultor das 10h também é no caderno. Modelo: `videos/checklist-sair-do-rotativo/` (lista 1-5 na folha, escrita passo a passo, com ✓ verde; palco da conta embaixo; Consultor `hero` à direita) e capa `videos/checklist-sair-do-rotativo/capa.py`. As regras de 2c que falam do quadro navy ilustrado (`fundo_marca`, `consultor_i`, chips) ficam substituídas por isso; o resto de 2c (lista vazia no quadro 0, valor que atravessa o vídeo, legenda "salva pro...") continua.
- Revisão **obrigatória**: `python render.py sheet ...` no fim e no meio das cenas, pelo menos duas rodadas, corrigindo sobreposições e qualquer coisa abaixo de y 1500 ou à direita de x 930 (no Permanent Marker, "R$ 2.100" vira "2100": use `m()` como no modelo). Teste mudo curto: `python render.py build videos/<slug>/scenes.py silent:8 out/teste.mp4`.
- `videos/<slug>/capa.py` (modelo `videos/ferias-mes-seguinte/capa.py`: moldura navy, folha creme, título em Marker, o número que choca e o Consultor `hero` reagindo) e `videos/<slug>/post.txt` (legenda do TikTok com gancho na 1ª linha, 2 ou 3 linhas da conta, pergunta final e 3 a 5 hashtags; título curto para Shorts).

### 6. Fila
`fila_tiktok/<slug>.json` para cada vídeo:
```json
{"slug": "<slug>", "data": "2026-11-08", "horario": "10:00", "titulo": "<título curto>",
 "audio_blocos": [...], "duracoes": [...], "musica": "trilha_faz_a_conta"}
```
(`audio_blocos` e `duracoes`: copie de `videos/<slug>/narracao.json`. `"musica"` só se fizer um "E se..."; o Checklist das 10h e o das 18h vão sem música.)
Valide com `python -m json.tool`.

### 7. Commit e push
Commit de `videos/<slug>/` (sem áudio), `automacao/temas_tiktok.md` e `fila_tiktok/*.json` na `main` e push (se recusar: `git pull --rebase` e push de novo). O push dispara o workflow "TikTok automático" (~5 a 10 min por vídeo).

### 8. Esperar, baixar e entregar
- A cada 60 s, por até 50 min, confira se a release saiu: `curl -s https://api.github.com/repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>` (ou `gh api repos/matheuspdias/stickfigure-videos/releases/tags/tiktok-<slug>`). Se o workflow falhar, leia `fila_tiktok/ultimo_log.txt` depois de `git pull`, corrija o que for do seu lado (cena, JSON) e faça push de novo.
- Baixe `<slug>_tiktok.mp4`, `<slug>_capa.png` e `<slug>_post.txt` da release e confira 2 ou 3 quadros do MP4 (gancho, meio, fim).
- Entregue com **SendUserFile** (status `proactive`): primeiro o vídeo e a capa das **10h**, depois o vídeo e a capa das **18h**.
- Termine com **SendUserMessage** curto, em português:
  - **10h:** título + a legenda pronta para copiar (do post.txt);
  - **18h:** título + a legenda pronta para copiar;
  - lembretes de uma linha: ativar o selo de conteúdo gerado por IA (voz), postar à mão e, se quiser, subir em Shorts e Reels ;
  - qualquer decisão tomada sozinho (tema, número estimado) ou problema.
