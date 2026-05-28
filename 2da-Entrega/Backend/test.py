import math


def minutos_a_hora(minutos: float) -> str:
    total_segundos = round(minutos * 60)

    horas = total_segundos // 3600
    minutos_restantes = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"


print(minutos_a_hora(1065.6659010842052))


def truncar_a_decimales(valor: float, decimales: int = 3) -> float:
    factor = 10 ** decimales
    return math.trunc(valor * factor) / factor


print(truncar_a_decimales(0.99968744587923789))

print(truncar_a_decimales(0.0014123540))

print(truncar_a_decimales(0.5676554645))

# Runner minimo para validar conversion de minutos a hh:mm:ss
if __name__ == "__main__":
    from app.domain.services.float_a_hora_service import float_a_hora

    print(float_a_hora(0))
    print(float_a_hora(1065.6659010842052))

    print("12:00:05" > "12:00:09")