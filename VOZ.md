# Voz oficial do canal Faz a Conta: "O Consultor"

| Item | Valor |
| --- | --- |
| Voz | **Afonso - Warm & Resonant** (catálogo público do HeyGen, pt-BR, masculina, voz "instant"). Escolhida pelo Matheus em 13/11/2026 (Calm Carlos ficou ruim fora do ElevenLabs) |
| voice_id | `9ce5f601f9e04382bb26141d5a3f839d` |
| Voz anterior | Calm Carlos `3b2a59d6edb54e79a40b29726a12d1c3` (até 13/11/2026) |
| Ferramenta | HeyGen `create_speech_without_player` (ou `create_speech`), com `withTimestamps: true` |
| Modelo | **não informar** (o servidor usa o HeyGen Voice padrão do plano pago, `heygen-voice-1`) |
| Idioma | `language: "pt"` |
| Expressividade | não informar (padrão do servidor; foi assim na amostra que o Matheus aprovou em 13/11/2026) |

## Mudança de 11/11/2026
O HeyGen tirou da ferramenta a escolha do motor (`engine: "elevenlabs"`, `settings: {"model_id": "eleven_v4"}`).
A voz continua a Calm Carlos, mas sai pelo modelo próprio do HeyGen e soa um pouco diferente (o Matheus achou o v4 mais natural).
Decisão do Matheus (11/11/2026): **continuar no HeyGen** (comparado com o ElevenLabs direto, pela cobertura do Ponto Cego e pelo fluxo pronto).
- As respostas agora trazem `original_words` (`text`, `start_time`, `end_time`) no lugar de `word_timestamps`. Palavras com hífen
  podem vir separadas (ex.: "montanha-russa" vira "montanha" + "russa"): junte antes de alinhar com o roteiro.
- Tags de áudio: use `[pause]` (suportada) para separar os ganchos. Tag desconhecida normalmente não é falada, mas não arrisque.
- A resposta com tempos é grande (mais de 150 mil caracteres por bloco): ela é salva em arquivo; leia com Python.

## Fluxo padrão (o Matheus NÃO grava nem transcreve nada)
1. Claude escreve o roteiro (números por extenso, tom calmo e didático; tags com moderação, sem `[whispers]`).
2. Claude gera a narração em blocos de até ~4.500 caracteres e guarda os tempos de cada palavra (eles substituem a transcrição).
3. O ambiente não baixa arquivos do HeyGen: no modo automático quem baixa é o GitHub Actions; no manual, Claude manda os links dos `.wav` e o Matheus só baixa e anexa no chat.
4. Junta com `python juntar_blocos.py out/<slug>_narracao.wav bloco1.wav bloco2.wav ...` (0,4 s de silêncio entre blocos desde 22/10/2026; força float para não criar chiado na voz) e monta o vídeo.

Só se o Matheus mandar um áudio gravado por ele, aí sim é preciso transcrição com tempos.
Modelo: `videos/dez-mil-dez-anos/` (`gerar_tempos.py` + `ts_b*.txt`).
