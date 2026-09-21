import random


# -----------------------------
# THRESHOLDS
# -----------------------------

UMBRAL_HUMEDAD_MIN = 30.0
UMBRAL_PH_MIN = 5.5
UMBRAL_PH_MAX = 6.5
NIVEL_AGUA_CRITICO = 20.0


# -----------------------------
# SENSOR SIMULATION
# -----------------------------

def leer_sensores_cultivo():

    humedad = random.uniform(20.0, 50.0)
    ph = random.uniform(5.0, 7.0)
    nivel_tanque = random.uniform(5.0, 100.0)

    return humedad, ph, nivel_tanque


# -----------------------------
# SYSTEM LOGIC
# -----------------------------

def evaluar_cultivo(humedad, ph, nivel_tanque, sismo):

    eventos = []

    # Highest-priority condition
    if sismo:
        eventos.append({
            "level": "CRITICAL",
            "system": "Cultivation",
            "message": "Seismic vibration detected.",
            "action": "Closing solenoid valves and isolating fluids."
        })

        return eventos

    # Water management
    if nivel_tanque < NIVEL_AGUA_CRITICO:

        eventos.append({
            "level": "WARNING",
            "system": "Cultivation",
            "message": "Water reservoir below safe level.",
            "action": "Isolating suspected leak and activating reserve irrigation mode."
        })

    elif humedad < UMBRAL_HUMEDAD_MIN:

        eventos.append({
            "level": "WARNING",
            "system": "Cultivation",
            "message": "Root-zone humidity insufficient.",
            "action": "Activating hydroponic pump."
        })

    # Chemical stability
    if not (UMBRAL_PH_MIN <= ph <= UMBRAL_PH_MAX):

        eventos.append({
            "level": "WARNING",
            "system": "Cultivation",
            "message": f"pH outside specification: {ph:.2f}.",
            "action": "Activating chemical dosing system."
        })

    # Everything nominal
    if not eventos:

        eventos.append({
            "level": "NOMINAL",
            "system": "Cultivation",
            "message": "Cultivation parameters nominal.",
            "action": "No corrective action required."
        })

    return eventos