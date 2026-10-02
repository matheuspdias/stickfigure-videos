# Voz oficial do canal Faz a Conta: "O Consultor"

| Item | Valor |
| --- | --- |
| Voz | **Calm Carlos** (catálogo público do HeyGen, português, masculina) |
| voice_id | `3b2a59d6edb54e79a40b29726a12d1c3` |
| Motor | HeyGen `create_speech`, `engine: "elevenlabs"`, `settings: {"model_id": "eleven_v4"}` |
| Idioma | `language: "pt"` |
| Velocidade | 1.0 (padrão) |

## Fluxo padrão (o Matheus NÃO grava nem transcreve nada)
1. Claude escreve o roteiro (números por extenso, tom calmo e didático; tags v4 com moderação, sem `[whispers]`).
2. Claude gera a narração em blocos de até ~4.500 caracteres com `create_speech` e guarda os `word_timestamps` (eles substituem a transcrição).
3. O ambiente não baixa arquivos do HeyGen: Claude manda os links dos `.wav` e o Matheus só baixa e anexa no chat.
4. Claude junta com `python juntar_blocos.py out/<slug>_narracao.wav bloco1.mp3 bloco2.mp3 ...` (1,0 s de silêncio entre blocos; força float para não criar chiado na voz) e monta o vídeo.

Só se o Matheus mandar um áudio gravado por ele, aí sim é preciso transcrição com tempos.
Modelo: `videos/carro-5000-v2/narracao_blocos.txt`.
