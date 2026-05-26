def float_a_hora(minutos: float) -> str:
    total_segundos = round(minutos * 60) % 86400  # 86400 = 24 * 3600, hace que el reloj "dé la vuelta"

    horas = total_segundos // 3600
    minutos_restantes = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"