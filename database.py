
import sqlite3
import json
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "agrosmart.db"


def conectar():
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_bd():
    with conectar() as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS simulacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                productores_iniciales REAL NOT NULL,
                tasa_adopcion REAL NOT NULL,
                limite_productores REAL NOT NULL,
                tiempo_final REAL NOT NULL,
                fecha TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS ejecucion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                simulacion_id INTEGER NOT NULL,
                paso REAL NOT NULL,
                FOREIGN KEY (simulacion_id)
                    REFERENCES simulacion(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS resultado (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ejecucion_id INTEGER NOT NULL,
                tiempo REAL NOT NULL,
                analitica REAL NOT NULL,
                heun REAL NOT NULL,
                rk4 REAL NOT NULL,
                error_heun_absoluto REAL NOT NULL,
                error_heun_relativo REAL,
                error_rk4_absoluto REAL NOT NULL,
                error_rk4_relativo REAL,
                FOREIGN KEY (ejecucion_id)
                    REFERENCES ejecucion(id) ON DELETE CASCADE
            );
        """)


def guardar_simulacion(datos):
    parametros = datos["parametros"]

    with conectar() as db:
        cursor = db.execute("""
            INSERT INTO simulacion (
                productores_iniciales,
                tasa_adopcion,
                limite_productores,
                tiempo_final,
                fecha
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            parametros["productores_iniciales"],
            parametros["tasa_adopcion"],
            parametros["limite_productores"],
            parametros["tiempo_final"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        simulacion_id = cursor.lastrowid

        for simulacion in datos["simulaciones"]:
            cursor = db.execute("""
                INSERT INTO ejecucion (simulacion_id, paso)
                VALUES (?, ?)
            """, (simulacion_id, simulacion["h"]))

            ejecucion_id = cursor.lastrowid

            filas = [
                (
                    ejecucion_id,
                    x["tiempo"],
                    x["analitica"],
                    x["heun"],
                    x["rk4"],
                    x["error_heun_absoluto"],
                    x["error_heun_relativo"],
                    x["error_rk4_absoluto"],
                    x["error_rk4_relativo"]
                )
                for x in simulacion["resultados"]
            ]

            db.executemany("""
                INSERT INTO resultado (
                    ejecucion_id, tiempo, analitica, heun, rk4,
                    error_heun_absoluto, error_heun_relativo,
                    error_rk4_absoluto, error_rk4_relativo
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, filas)

        return simulacion_id


def obtener_historial():
    with conectar() as db:
        filas = db.execute("""
            SELECT * FROM simulacion
            ORDER BY id DESC
        """).fetchall()

    return [dict(fila) for fila in filas]


def obtener_simulacion(simulacion_id):
    with conectar() as db:
        simulacion = db.execute("""
            SELECT * FROM simulacion WHERE id = ?
        """, (simulacion_id,)).fetchone()

        if simulacion is None:
            return None

        ejecuciones = db.execute("""
            SELECT * FROM ejecucion
            WHERE simulacion_id = ?
            ORDER BY paso
        """, (simulacion_id,)).fetchall()

        resultado = {
            "simulacion": dict(simulacion),
            "ejecuciones": []
        }

        for ejecucion in ejecuciones:
            filas = db.execute("""
                SELECT * FROM resultado
                WHERE ejecucion_id = ?
                ORDER BY tiempo
            """, (ejecucion["id"],)).fetchall()

            resultado["ejecuciones"].append({
                "paso": ejecucion["paso"],
                "resultados": [dict(fila) for fila in filas]
            })

    return resultado
