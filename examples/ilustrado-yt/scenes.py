"""Demo do estilo ILUSTRADO do Faz a Conta (16:9, sem narração, ~66 s)."""
from engine import *
from ilustrado import *

STYLE = "ilustrado"
SFX_OFF = True


def s01(c, t):  # padaria: o gasto do dia a dia
    cena_padaria(c, t, "dia")
    consultor_i(c, t, 330, 1040, 1.1, poses=((0, "stand"), (1.0, "present")), exprs=((0, "happy"),), look=0.6)
    entra(c, t, 0.8, 960, 210, lambda c: numero_i(c, "R$ 10 POR DIA", 0, 0, 120, GOLD))
    entra(c, t, 2.0, 1180, 640, lambda c: etiqueta_preco(c, "R$ 10", GOLD, 60), anim="drop")
    rotulo(c, t, 2.6, "O CAFÉ + O PÃO DE TODO DIA", "dá R$ 300 por mês", x=700, y=960)


def s02(c, t):  # conta: contador + moedas
    t0 = 6
    fundo_marca(c, t, "creme")
    numero_i(c, "R$ 10 x 30 DIAS", 960, 180, 90, NAVY, contorno=(1, 1, 1))
    contador(c, t, t0 + 0.6, 0, 300, 1100, 400, 170, d=1.6, col=VERDE, sufixo="/mês")
    for i, n in enumerate((6, 10, 14)):
        c.save(); c.translate(860 + i * 240, 960); pilha_moedas(c, n, 70, t, t0 + 0.6 + i * 0.4, 0.09); c.restore()
    consultor_i(c, t, 330, 1040, 1.1, poses=((0, "stand"),), exprs=((0, "confident"),), look=0.6, prop=("r", prop_calc_i))


def s03(c, t):  # juros compostos
    t0 = 12
    fundo_marca(c, t, "creme")
    numero_i(c, "INVESTINDO R$ 300 POR MÊS", 1100, 110, 70, NAVY, contorno=(1, 1, 1))
    grafico_curva(c, t, t0 + 0.3, 640, 920, 1060, 560, d=3.2, marcas=((0.43, "15 anos"), (0.71, "25 anos")), valor_fim="R$ 1 MILHÃO")
    consultor_i(c, t, 290, 1040, 1.05, poses=((0, "point_r"), (t0 + 3.6, "arms_up")), exprs=((0, "neutral"), (t0 + 3.6, "grin")), look=0.6)
    chuva_dinheiro(c, t, t0 + 3.6, 10, area=(1500, 1880))


def s04(c, t):  # Ana x Bruno
    t0 = 19
    fundo_marca(c, t, "creme")
    numero_i(c, "QUEM COMEÇOU ANTES?", 960, 120, 80, NAVY, contorno=(1, 1, 1))
    pessoa(c, t, 260, 1030, 1.0, "ana", poses=((0, "stand"), (t0 + 2.4, "arms_up")), exprs=((0, "neutral"), (t0 + 2.4, "grin")), look=0.4)
    pessoa(c, t, 1660, 1030, 1.0, "bruno", poses=((0, "stand"), (t0 + 2.4, "shrug")), exprs=((0, "neutral"), (t0 + 2.4, "worried")), look=-0.4)
    barras_i(c, t, t0 + 0.4, 560, 880, 800, 560, (("Ana", 372000, PURPLE), ("Bruno", 228000, BLUE)))


def s05(c, t):  # sala: a fatura chega
    t0 = 26
    cena_sala(c, t, "tarde")
    pessoa(c, t, 760, 1050, 1.0, "carla", poses=((0, "stand"), (t0 + 2.2, "head")), exprs=((0, "neutral"), (t0 + 2.2, "desperate")), look=0.5)
    fatura(c, t, 1300, 400, 0.9, t0=t0 + 0.6, minimo="R$ 357")
    consultor_i(c, t, 300, 1050, 1.05, poses=((0, "think"),), exprs=((0, "worried"),), look=0.5)


def s06(c, t):  # mercado: inflação
    t0 = 33
    cena_mercado(c, t)
    consultor_i(c, t, 330, 1050, 1.08, poses=((0, "point_r"),), exprs=((0, "shocked"),), look=0.6)
    entra(c, t, t0 + 0.6, 900, 470, lambda c: etiqueta_preco(c, "R$ 16", VERMELHO, 64, riscado="R$ 10"), anim="drop")
    rotulo(c, t, t0 + 1.2, "INFLAÇÃO", "o mesmo carrinho, 10 anos depois", x=700, y=960)


def s07(c, t):  # escritório: contracheque
    t0 = 40
    cena_escritorio(c, t, "dia")
    consultor_i(c, t, 330, 1060, 1.08, poses=((0, "present"),), exprs=((0, "confident"),), look=0.6)
    entra(c, t, t0 + 0.5, 1150, 520, lambda c: contracheque(c, 0, 0, 1.0))


def s08(c, t):  # rua: carro e a parcela
    t0 = 47
    cena_rua(c, t, "tarde")
    consultor_i(c, t, 330, 1060, 1.08, poses=((0, "point_r"),), exprs=((0, "worried"),), look=0.6)
    entra(c, t, t0 + 0.4, 1250, 360, lambda c: (rr(c, -300, -250, 600, 500, 30), rgb(c, (1, 1, 1), 0.92), c.fill()))
    rosca_i(c, t, t0 + 0.6, 1250, 330, 150, 0.35, VERMELHO)
    if t > t0 + 1.6:
        numero_i(c, "DO SALÁRIO NO CARRO", 1250, 540, 46, NAVY, contorno=(1, 1, 1))


def s09(c, t):  # agência: notificação de crédito
    t0 = 54
    cena_agencia(c, t)
    pessoa(c, t, 1500, 1050, 1.0, "gerente", poses=((0, "present_l"),), exprs=((0, "grin"),), look=-0.6)
    consultor_i(c, t, 330, 1050, 1.05, poses=((0, "stand"), (t0 + 2, "finger_up")), exprs=((0, "neutral"), (t0 + 2, "think")), look=0.6)
    entra(c, t, t0 + 0.6, 960, 420, lambda c: notificacao(c, 0, 0, 1.3), anim="drop")


def s10(c, t):  # app do banco no fundo navy
    t0 = 60
    fundo_marca(c, t, "navy", holofote=(420, 700))
    celular_app(c, t, 1250, 560, 1.15, "Extrato de novembro", "R$ 2.706",
                linhas=(("Salário", "+ R$ 3.000", VERDE), ("Aluguel", "- R$ 1.200", VERMELHO), ("Mercado", "- R$ 640", VERMELHO),
                        ("Investido", "- R$ 300", NAVY)), t0=t0 + 0.4, d=1.6)
    consultor_i(c, t, 420, 1040, 1.1, poses=((0, "point_r"),), exprs=((0, "confident"),), look=0.7)


SCENES = [(0, 6, s01), (6, 12, s02), (12, 19, s03), (19, 26, s04), (26, 33, s05), (33, 40, s06), (40, 47, s07),
          (47, 54, s08), (54, 60, s09), (60, 999.0, s10)]
