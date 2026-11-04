"""Contas do vídeo "Amortizar o financiamento ou investir? A conta completa" (premissas conferidas em 04/11/2026).

Premissas
- Imóvel R$ 300.000, entrada 20%, financiado R$ 240.000, 360 meses, SAC (mesmo cenário do vídeo "Alugar ou comprar?"
  e do TikTok "amortizacao-mcmv").
- Juros MCMV faixa 3: 7,66% a.a. (cotista FGTS; 8,16% não cotista), + TR. Fonte: regras de abril/2026 (Caixa 22/04/2026).
  Taxa mensal efetiva: 1,0766^(1/12) - 1.
- TR: 0,162% a 0,174% ao mês em 2026 (BCB; acumulado jan-out 1,659%). Usada 0,165% a.m. (~2,0% a.a.), constante.
  Saldo corrigido pela TR todo mês; amortização SAC = saldo corrigido / meses restantes.
- Sem seguros (MIP/DFI) e sem taxa de administração (amortizar também reduz o seguro: a favor de amortizar).
- Extra: R$ 300 por mês, reduzindo o PRAZO.
- Investimento: 10% a.a. líquido de IR (0,7974% a.m.), constante (premissa pé no chão dos vídeos anteriores).
  Referências de hoje: Selic 13,75% (Copom 16/09/2026; reunião de 04/11/2026 em andamento), CDI ~13,65%,
  CDB 100% CDI com IR 15% (acima de 720 dias, tabela regressiva vigente; MP 1.303 caducou em 08/10/2025) = ~11,6% a.a.
  Poupança 0,5% a.m. + TR = ~8,3% a.a. (isenta).
- SBPE (financiamento fora do MCMV): ~11,5% a.a. + TR (média dos 5 maiores bancos, out/2026).
- Comparação justa: Carla e Diego têm o mesmo orçamento (parcela do Diego + R$ 300). Carla paga esse valor inteiro
  no financiamento (o que passa da parcela vai pro saldo) até quitar
  e depois investe a parcela que pagaria + R$ 300 até o mês 360. Diego paga a parcela normal e investe R$ 300 por mês.
"""
P = 240000.0; N = 360; TR = 0.00165; EXTRA = 300.0

def mens(a): return (1 + a) ** (1 / 12) - 1

def br(x): return f"R$ {x:,.0f}".replace(",", ".")

def sac(ia, extra=0.0, tr=TR, lump=None, mode="prazo"):
    """Retorna dict com parcelas por mês (sem extra), total pago, mês da quitação."""
    i = mens(ia); s = P; tot = 0.0; parc = []; juros = 0.0
    sched = None
    m = 0
    while s > 0.01 and m < N:
        m += 1
        s *= (1 + tr)
        rem = N - m + 1
        a = s / rem if (mode == "parcela" or not extra and lump is None) else None
        if a is None:
            # prazo: amortização igual à do contrato normal no mesmo mês
            a = base_amort[m - 1] if m - 1 < len(base_amort) else s
        a = min(a, s)
        j = s * i
        s -= a; tot += a + j; juros += j; parc.append(a + j)
        if extra and s > 0:
            e = min(extra, s); s -= e; tot += e
        if lump and m == lump[0] and s > 0:
            e = min(lump[1], s); s -= e; tot += e
    return dict(tot=tot, meses=m, parc=parc, juros=juros)

def base(ia, tr=TR):
    global base_amort
    i = mens(ia); s = P; am = []; parc = []; tot = 0; juros = 0
    for m in range(1, N + 1):
        s *= (1 + tr); a = s / (N - m + 1); j = s * i
        s -= a; am.append(a); parc.append(a + j); tot += a + j; juros += j
    base_amort = am
    return dict(tot=tot, parc=parc, juros=juros, amort=am)

def investe(taxa_a, fluxos):
    i = mens(taxa_a); v = 0.0
    for f in fluxos: v = v * (1 + i) + f
    return v

def corrida(ia, inv_a, tr=TR, extra=EXTRA, verbose=False):
    """Orçamento igual todo mês: B_m = parcela do Diego no mês m + extra.
    Carla paga B_m inteiro no financiamento (juros, depois saldo) até quitar; depois investe B_m.
    Diego paga a parcela normal e investe o extra."""
    b = base(ia, tr); i = mens(ia)
    s = P; carla_inv = 0.0; M = None; iv = mens(inv_a)
    for m in range(N):
        B = b["parc"][m] + extra
        carla_inv *= (1 + iv)
        if s > 0.01:
            s *= (1 + tr); j = s * i
            pago = min(B, s + j); s -= (pago - j)
            if s <= 0.01:
                s = 0.0; M = m + 1
                carla_inv += B - pago
        else:
            carla_inv += B
    diego = investe(inv_a, [extra] * N)
    return M, diego, carla_inv

if __name__ == "__main__":
    MCMV = 0.0766; INV = 0.10
    b = base(MCMV)
    print("taxa mensal MCMV", round(mens(MCMV) * 100, 4), "% | TR a.a.", round(((1 + TR) ** 12 - 1) * 100, 2), "%")
    custo = (1 + mens(MCMV)) * (1 + TR) - 1
    print("custo efetivo com TR:", round(((1 + custo) ** 12 - 1) * 100, 2), "% a.a.")
    print("SEM amortizar: 1a parcela", br(b["parc"][0]), "maior parcela", br(max(b["parc"])), "total", br(b["tot"]), "juros+TR", br(b["tot"] - P))
    c = sac(MCMV, EXTRA)
    print(f"+R$300/mes: quita no mes {c['meses']} ({c['meses']/12:.1f} anos), {(N-c['meses'])/12:.1f} anos antes; total {br(c['tot'])} economia {br(b['tot']-c['tot'])}")
    print("  extra total colocado:", br(EXTRA * c["meses"]))
    # sem TR (como no TikTok) p/ referência
    b0 = base(MCMV, 0); c0 = sac(MCMV, EXTRA, 0)
    print("sem TR: total", br(b0["tot"]), "+300 quita mes", c0["meses"], "economia", br(b0["tot"] - c0["tot"]))
    base(MCMV)
    # parcela do mes de quitação
    M = c["meses"]
    print("parcela do Diego no mes", M + 1, br(b["parc"][M]), "-> Carla investe", br(b["parc"][M] + EXTRA))
    print("\nCORRIDA (orcamento igual), resultado no mes 360:")
    for nome, inv in [("poupanca 8,3%", 0.0832), ("10% liq", 0.10), ("CDB hoje 11,6%", 0.116)]:
        M, d, ca = corrida(MCMV, inv)
        print(f"  {nome:16s} Diego {br(d):>14s}  Carla {br(ca):>14s}  dif {br(ca-d)}")
    # empate: taxa de investimento onde Carla = Diego
    lo, hi = 0.05, 0.15
    for _ in range(60):
        mid = (lo + hi) / 2; M, d, ca = corrida(MCMV, mid)
        if ca > d: lo = mid
        else: hi = mid
    print("  empate em investimento de", round(mid * 100, 2), "% a.a. liquido")
    # Diego no mes em que Carla quita
    for inv in (0.10,):
        M, d, ca = corrida(MCMV, inv)
        dM = investe(inv, [EXTRA] * M)
        bb = base(MCMV); 
        # saldo devedor do Diego no mes M
        i = mens(MCMV); s = P
        for m in range(1, M + 1):
            s *= (1 + TR); a = s / (N - m + 1); s -= a
        print(f"  no mes {M}: Diego tem {br(dM)} investidos e ainda deve {br(s)}")
    print("\nSBPE 11,5% + TR:")
    bs = base(0.115); cs = sac(0.115, EXTRA)
    print("  1a parcela", br(bs["parc"][0]), "total", br(bs["tot"]), "+300 quita mes", cs["meses"], f"({(N-cs['meses'])/12:.1f} anos antes)", "economia", br(bs["tot"] - cs["tot"]))
    print("  custo efetivo", round(((1 + mens(0.115)) * (1 + TR)) ** 12 * 100 - 100, 2), "% a.a.")
    for nome, inv in [("poupanca", 0.0832), ("10% liq", 0.10), ("CDB hoje 11,6%", 0.116)]:
        M, d, ca = corrida(0.115, inv)
        print(f"  {nome:16s} Diego {br(d):>14s}  Carla {br(ca):>14s}  dif {br(ca-d)}")
    base(MCMV)
    print("\nCDB 100% CDI liq:", round(13.65 * 0.85, 2), "% a.a.")

if __name__ == "__main__":
    print("\nDETALHES DA CORRIDA (MCMV, 10% liq)")
    b = base(MCMV); i = mens(MCMV); s = P; pagoC = 0
    for m in range(N):
        B = b["parc"][m] + EXTRA
        s *= (1 + TR); j = s * i; pago = min(B, s + j); s -= pago - j; pagoC += pago
        if s <= 0.01: break
    M = m + 1
    print(f"Carla quita no mes {M} = {M//12} anos e {M%12} meses ({(N-M)/12:.1f} anos antes); pagou {br(pagoC)} no total; economia vs Diego {br(b['tot']-pagoC)}")
    print("orcamento no mes 1:", br(b["parc"][0] + EXTRA), " no mes", M + 1, ":", br(b["parc"][M] + EXTRA), " no mes 360:", br(b["parc"][-1] + EXTRA))
    print("Diego pagou ao banco", br(b["tot"]), "e colocou", br(EXTRA * N), "no investimento")
    # Diego no mes M
    sD = P
    for m in range(1, M + 1):
        sD *= (1 + TR); a = sD / (N - m + 1); sD -= a
    print(f"no mes {M}: Diego tem {br(investe(0.10, [EXTRA]*M))} investidos e deve {br(sD)}")
    # anos 5,10,15
    for ano in (5, 10, 15, 20, 25, 30):
        print("  ano", ano, "Diego invest", br(investe(0.10, [EXTRA]*ano*12)))
    # prazo x parcela: 10 mil no mes 1
    def lump(mode):
        b = base(MCMV); i = mens(MCMV); s = P; tot = 0
        A = None
        for m in range(1, N + 1):
            if s <= 0.01: break
            s *= (1 + TR); j = s * i
            if mode == "parcela" or A is None:
                a = s / (N - m + 1)
            else:
                a = b["amort"][m - 1]
            a = min(a, s); s -= a; tot += a + j
            if m == 1:
                s -= 10000; tot += 10000; A = 1
        return tot
    print("10 mil no mes 1: prazo economiza", br(b["tot"] - lump("prazo")), "| parcela economiza", br(b["tot"] - lump("parcela")))
