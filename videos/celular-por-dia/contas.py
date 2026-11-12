"""Contas do vídeo celular-por-dia (TikTok 13/11/2026 10h).
Premissas (estimativas redondas de mercado de usados, ditas com "uns" no roteiro):
- celular top de R$ 8.000: revende por ~R$ 5.000 após 1 ano (~62%) e ~R$ 2.000 após 4 anos (~25%)
- celular intermediário de R$ 2.000: revende por ~R$ 400 após 3 anos (~20%)
- celular básico de R$ 1.200 trocado todo ano: revende por ~R$ 300
Custo por dia = (preço - revenda) / dias de uso. Sem juros (12x sem juros)."""
casos = {
    "top, troca todo ano": (8000, 5000, 1),
    "intermediario, 3 anos": (2000, 400, 3),
    "top, 4 anos": (8000, 2000, 4),
    "basico, troca todo ano": (1200, 300, 1),
}
print("parcela 12x:", round(8000 / 12, 2))
for k, (p, r, a) in casos.items():
    print(f"{k:24s} perdeu R$ {p-r:5d} em {a} ano(s) -> R$ {(p-r)/(365*a):.2f}/dia, R$ {(p-r)/(12*a):.0f}/mes")
