# EpiSim

Sistema web académico para simular la propagación de una enfermedad mediante el modelo SIR y comparar los métodos numéricos de Heun y Runge-Kutta de cuarto orden (RK4).

## Requisitos
- Python 3.10 o superior
- Flask
- ReportLab

## Instalación en Windows (PowerShell)
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```
Abrir http://127.0.0.1:5000

## Modelo matemático
S' = -beta*S*I/N  
I' = beta*S*I/N - gamma*I  
R' = gamma*I

Los datos y resultados se guardan en `data/episim.db`. Los informes PDF se generan en `informes/`.

## Alcance
Proyecto educativo. El modelo SIR utilizado es simplificado y no constituye una predicción médica.
