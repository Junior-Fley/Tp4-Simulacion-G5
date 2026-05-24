def minutos_a_hora(minutos: float) -> str:
    total_segundos = round(minutos * 60)

    horas = total_segundos // 3600
    minutos_restantes = (total_segundos % 3600) // 60
    segundos = total_segundos % 60

    return f"{horas:02d}:{minutos_restantes:02d}:{segundos:02d}"


print(minutos_a_hora(650.5))