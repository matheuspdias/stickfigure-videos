# Publicação automática do Faz a Conta

Todo **domingo e quarta** uma tarefa agendada do Claude faz o vídeo longo de segunda e de quinta (passo a passo em `AUTOMATICO.md`)
e coloca na fila (`fila/<slug>.json`). O GitHub Actions renderiza e envia ao YouTube **agendado para as 9h**,
e depois agenda **3 Shorts** feitos de trechos do vídeo: um por dia às 12h (cortes de segunda em ter/qua/qui, de quinta em sex/sáb/dom).
O TikTok continua manual.

Janela de veto: o vídeo aparece no YouTube Studio como **Programado** desde a véspera. Para barrar, edite, deixe privado ou exclua por lá.

## Configuração (uma vez, ~5 min)

O projeto do Google Cloud e o cliente OAuth são **os mesmos do Ponto Cego**. Só falta um token para este canal.

1. No seu computador (WSL), dentro deste repositório:
   ```bash
   source ~/.venvs/yt/bin/activate
   python automacao/autorizar_youtube.py /mnt/c/Users/SEU_USUARIO/Downloads/client_secret_XXXX.json
   ```
   Na lista de contas, escolha **Faz a Conta**. No aviso de app não verificado: **Avançado > Acessar (não seguro) > Continuar**.
2. Em https://github.com/matheuspdias/stickfigure-videos/settings/secrets/actions crie os 3 **repository secrets**:
   `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN` (o ID e o secret são iguais aos do Ponto Cego; o token é novo).
3. Teste: **Actions > Publicar no YouTube > Run workflow**, marque **testar_credenciais**. O resumo deve mostrar **Canal: Faz a Conta**.
4. Thumbnail personalizada exige o canal verificado por telefone: https://www.youtube.com/verify (faça logado no Faz a Conta).

## No dia a dia
- **Ver o que vai sair:** YouTube Studio > Conteúdo (status Programado; os Shorts ficam na aba Shorts), ou `fila/publicados/` neste repo.
- **Desligar os Shorts de um vídeo:** `"shorts": false` no `fila/<slug>.json`. Horário e quantidade: `SHORT_HORA` e `SHORT_MAX` no `publicar.py`.
- **Acompanhar o render:** aba **Actions**. Se falhar, o GitHub manda e-mail. O MP4 fica 7 dias como artefato da execução.
- **Sugerir temas:** seção "Ideias" de `temas.md`.
- **Pausar:** pause a tarefa agendada no Claude. Para barrar um vídeo que está na fila e ainda não rodou, apague o `fila/<slug>.json`.

## Arquivos
- `publicar.py`: baixa os áudios, junta (com a cauda da Tela final), renderiza, envia o vídeo e os Shorts.
- `autorizar_youtube.py`: gera o token, roda uma vez no seu PC.
- `AUTOMATICO.md`: instruções da tarefa agendada.
- `temas.md`: vídeos já feitos e ideias.
- `../.github/workflows/publicar.yml`: o workflow.
