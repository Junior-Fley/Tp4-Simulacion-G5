import math


def truncar_a_decimales(valor: float, decimales: int = 3) -> float:
    factor = 10 ** decimales
    return math.trunc(valor * factor) / factor