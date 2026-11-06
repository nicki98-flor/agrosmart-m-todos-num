
import math


def modelo_logistico(t, U, r, K):
    """Ecuación diferencial logística de adopción tecnológica."""
    return r * U * (1 - U / K)


def solucion_analitica(t, U0, r, K):
    """Solución exacta del modelo logístico."""
    factor = ((K - U0) / U0) * math.exp(-r * t)
    return K / (1 + factor)


def metodo_heun(t, U, h, r, K):
    k1 = modelo_logistico(t, U, r, K)
    predictor = U + h * k1
    k2 = modelo_logistico(t + h, predictor, r, K)
    return U + (h / 2) * (k1 + k2)


def metodo_rk4(t, U, h, r, K):
    k1 = modelo_logistico(t, U, r, K)

    k2 = modelo_logistico(
        t + h / 2, U + h * k1 / 2, r, K
    )

    k3 = modelo_logistico(
        t + h / 2, U + h * k2 / 2, r, K
    )

    k4 = modelo_logistico(
        t + h, U + h * k3, r, K
    )

    return U + (h / 6) * (k1 + 2*k2 + 2*k3 + k4)


def calcular_errores(exacto, aproximado):
    absoluto = abs(exacto - aproximado)
    relativo = (absoluto / abs(exacto)) * 100 if exacto != 0 else None
    return absoluto, relativo


def validar_parametros(U0, r, K, tiempo_final, pasos):
    valores = [U0, r, K, tiempo_final] + list(pasos)

    if not all(math.isfinite(float(x)) for x in valores):
        raise ValueError("Todos los parámetros deben ser números finitos.")

    if K <= 0:
        raise ValueError("El límite K debe ser mayor que cero.")

    if U0 <= 0 or U0 >= K:
        raise ValueError("U0 debe ser mayor que cero y menor que K.")

    if r <= 0:
        raise ValueError("La tasa de adopción debe ser positiva.")

    if tiempo_final <= 0:
        raise ValueError("El tiempo final debe ser mayor que cero.")

    if len(pasos) != 2 or any(h <= 0 for h in pasos):
        raise ValueError("Se necesitan dos tamaños de paso positivos.")

    if pasos[0] == pasos[1]:
        raise ValueError("Los tamaños de paso deben ser diferentes.")


def ejecutar_simulacion(U0, r, K, tiempo_final, h):
    t = 0.0
    U_heun = float(U0)
    U_rk4 = float(U0)

    resultados = []

    while True:
        exacto = solucion_analitica(t, U0, r, K)

        error_heun, relativo_heun = calcular_errores(exacto, U_heun)
        error_rk4, relativo_rk4 = calcular_errores(exacto, U_rk4)

        resultados.append({
            "tiempo": round(t, 10),
            "analitica": exacto,
            "heun": U_heun,
            "rk4": U_rk4,
            "error_heun_absoluto": error_heun,
            "error_heun_relativo": relativo_heun,
            "error_rk4_absoluto": error_rk4,
            "error_rk4_relativo": relativo_rk4
        })

        if t >= tiempo_final - 1e-10:
            break

        paso = min(h, tiempo_final - t)

        U_heun = metodo_heun(t, U_heun, paso, r, K)
        U_rk4 = metodo_rk4(t, U_rk4, paso, r, K)

        t = min(t + paso, tiempo_final)

    resumen = {
        "heun_absoluto_maximo": max(
            x["error_heun_absoluto"] for x in resultados
        ),
        "heun_relativo_maximo": max(
            x["error_heun_relativo"] or 0 for x in resultados
        ),
        "rk4_absoluto_maximo": max(
            x["error_rk4_absoluto"] for x in resultados
        ),
        "rk4_relativo_maximo": max(
            x["error_rk4_relativo"] or 0 for x in resultados
        )
    }

    return {
        "h": h,
        "cantidad_puntos": len(resultados),
        "resultados": resultados,
        "resumen": resumen
    }


def simular_agrosmart(
    U0=10,
    r=0.12,
    K=100,
    tiempo_final=24,
    pasos=(1, 0.5)
):
    pasos = tuple(float(h) for h in pasos)

    validar_parametros(U0, r, K, tiempo_final, pasos)

    simulaciones = [
        ejecutar_simulacion(U0, r, K, tiempo_final, h)
        for h in pasos
    ]

    return {
        "parametros": {
            "productores_iniciales": U0,
            "tasa_adopcion": r,
            "limite_productores": K,
            "tiempo_final": tiempo_final,
            "pasos": list(pasos)
        },
        "simulaciones": simulaciones
    }


def ejecutar_escenarios(U0, K, tiempo_final, pasos):
    escenarios = {
        "Adopción lenta": 0.06,
        "Adopción moderada": 0.12,
        "Adopción rápida": 0.20
    }

    resultados = {}

    for nombre, tasa in escenarios.items():
        resultados[nombre] = simular_agrosmart(
            U0=U0,
            r=tasa,
            K=K,
            tiempo_final=tiempo_final,
            pasos=pasos
        )

    return resultados


if __name__ == "__main__":
    datos = simular_agrosmart()

    print("\n==============================================")
    print("          AGROSMART - SIMULACIÓN")
    print("==============================================")

    print("\nPARÁMETROS:")
    for nombre, valor in datos["parametros"].items():
        print(f"{nombre}: {valor}")

    for simulacion in datos["simulaciones"]:
        print(f"\nRESULTADOS PARA h = {simulacion['h']} MESES")
        print(
            f"{'Mes':>8} {'Exacta':>12} "
            f"{'Heun':>12} {'RK4':>12}"
        )

        for fila in simulacion["resultados"]:
            print(
                f"{fila['tiempo']:8.2f} "
                f"{fila['analitica']:12.4f} "
                f"{fila['heun']:12.4f} "
                f"{fila['rk4']:12.4f}"
            )

        print("\nRESUMEN DE ERRORES:")
        for nombre, valor in simulacion["resumen"].items():
            print(f"{nombre}: {valor:.8f}")

    print("\nSIMULACIÓN FINALIZADA CORRECTAMENTE")
