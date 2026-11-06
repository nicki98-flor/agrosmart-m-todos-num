from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


ROSA = colors.HexColor("#F04476")
NARANJA = colors.HexColor("#FF7138")
VIOLETA = colors.HexColor("#7137A8")


def generar_pdf(simulacion, destino):
    d = simulacion["datos"]
    filas = simulacion["resultados"]
    doc = SimpleDocTemplate(
        str(destino), pagesize=landscape(A4),
        rightMargin=1.2*cm, leftMargin=1.2*cm,
        topMargin=1.2*cm, bottomMargin=1.2*cm
    )
    estilos = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "TituloEpi", parent=estilos["Title"],
        textColor=ROSA, fontSize=21, spaceAfter=8
    )
    story = [
        Paragraph("EpiSim - Informe de simulación epidemiológica", titulo),
        Paragraph(f"<b>Escenario:</b> {d['nombre']} &nbsp;&nbsp; <b>Enfermedad:</b> {d['enfermedad']}", estilos["Normal"]),
        Spacer(1, 8),
        Paragraph(
            f"<b>Población:</b> {d['poblacion']} &nbsp;&nbsp; "
            f"<b>Infectados iniciales:</b> {d['infectados_iniciales']} &nbsp;&nbsp; "
            f"<b>Recuperados iniciales:</b> {d['recuperados_iniciales']}", estilos["Normal"]),
        Paragraph(
            f"<b>Beta:</b> {d['beta']} &nbsp;&nbsp; <b>Gamma:</b> {d['gamma']} "
            f"&nbsp;&nbsp; <b>Duración:</b> {d['duracion']} días "
            f"&nbsp;&nbsp; <b>Paso:</b> {d['paso']} días", estilos["Normal"]),
        Spacer(1, 10),
        Paragraph("Resultados por día: Heun y Runge-Kutta de cuarto orden", estilos["Heading2"])
    ]
    tabla_datos = [[
        "Día", "Heun S", "Heun I", "Heun R", "RK4 S", "RK4 I", "RK4 R"
    ]]
    # En el PDF se incluyen hasta 35 filas distribuidas uniformemente para mantenerlo legible.
    if len(filas) <= 35:
        seleccion = filas
    else:
        indices = sorted(set(round(i * (len(filas)-1) / 34) for i in range(35)))
        seleccion = [filas[i] for i in indices]
    for f in seleccion:
        tabla_datos.append([
            f"{f['tiempo']:.2f}", f"{f['heun_s']:.2f}", f"{f['heun_i']:.2f}",
            f"{f['heun_r']:.2f}", f"{f['rk4_s']:.2f}", f"{f['rk4_i']:.2f}",
            f"{f['rk4_r']:.2f}"
        ])
    tabla = Table(tabla_datos, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), ROSA),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("BACKGROUND", (0,1), (-1,-1), colors.HexColor("#FFF4F6")),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#E8B6C5")),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("FONTSIZE", (0,0), (-1,-1), 7),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
    ]))
    story.extend([tabla, Spacer(1, 10)])
    story.append(Paragraph(
        "Nota: SIR es un modelo matemático simplificado. Los resultados son simulaciones académicas, "
        "no predicciones médicas. Heun y RK4 son aproximaciones numéricas; no se presenta una solución "
        "analítica exacta para este sistema no lineal.", estilos["Italic"]
    ))
    doc.build(story)
