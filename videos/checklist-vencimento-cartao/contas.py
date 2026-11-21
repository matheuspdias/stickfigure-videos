"""Contas do checklist do vencimento do cartão."""
from datetime import date
print("compra 02/12 -> 10/12:", (date(2026, 12, 10) - date(2026, 12, 2)).days, "dias")
print("compra 04/12 -> 10/01:", (date(2027, 1, 10) - date(2026, 12, 4)).days, "dias")
print("fecha 10 dias antes (31/12), compra 01/01 -> 10/02:", (date(2027, 2, 10) - date(2027, 1, 1)).days, "dias")
print("multa 2% em R$ 1.000:", 1000 * 0.02)
