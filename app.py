
from flask import Flask, render_template, request, redirect, url_for, flash
from calculos import simular_agrosmart
from database import (
    inicializar_bd,
    guardar_simulacion,
    obtener_historial,
    obtener_simulacion
)

app = Flask(__name__)
app.secret_key = "agrosmart-clave-local-2026"

inicializar_bd()


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/simulador", methods=["GET", "POST"])
def simulador():
    if request.method == "POST":
        try:
            U0 = float(request.form["U0"])
            r = float(request.form["r"])
            K = float(request.form["K"])
            tiempo = float(request.form["tiempo"])
            h1 = float(request.form["h1"])
            h2 = float(request.form["h2"])

            datos = simular_agrosmart(
                U0=U0,
                r=r,
                K=K,
                tiempo_final=tiempo,
                pasos=(h1, h2)
            )

            simulacion_id = guardar_simulacion(datos)

            flash("¡Simulación realizada y guardada correctamente!", "success")

            return redirect(
                url_for("resultados", simulacion_id=simulacion_id)
            )

        except ValueError as error:
            flash(str(error), "error")

        except Exception as error:
            app.logger.exception("Error durante la simulación")
            flash("Ocurrió un error inesperado al ejecutar la simulación.", "error")

    return render_template("simulador.html")


@app.route("/resultados/<int:simulacion_id>")
def resultados(simulacion_id):
    datos = obtener_simulacion(simulacion_id)

    if datos is None:
        flash("No se encontró la simulación solicitada.", "error")
        return redirect(url_for("historial"))

    return render_template("resultados.html", datos=datos)


@app.route("/historial")
def historial():
    simulaciones = obtener_historial()
    return render_template(
        "historial.html",
        simulaciones=simulaciones
    )

@app.route("/tecnologia")
def tecnologia():
    return render_template("tecnologia.html")

if __name__ == "__main__":
    app.run(debug=True)
