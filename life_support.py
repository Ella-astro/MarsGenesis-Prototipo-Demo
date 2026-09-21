import random


# -----------------------------
# THRESHOLDS
# -----------------------------

RITMO_CARDIACO_MAX = 120
NIVEL_OXIGENO_MIN = 95.0
CALIDAD_AIRE_PPM_MAX = 1000


# -----------------------------
# SENSOR SIMULATION
# -----------------------------

def leer_sensores_medicos():

    ritmo_cardiaco = random.randint(65, 135)
    oxigeno_sangre = random.uniform(92.0, 100.0)
    co2_ambiente = random.randint(400, 1200)

    return (
        ritmo_cardiaco,
        oxigeno_sangre,
        co2_ambiente
    )


# -----------------------------
# SYSTEM LOGIC
# -----------------------------

def evaluar_soporte_vital(bpm, spo2, co2, sismo):

    eventos = []

    # Seismic event
    if sismo:

        eventos.append({
            "level": "CRITICAL",
            "system": "Life Support",
            "message": "Seismic event detected.",
            "action": (
                "Adjusting environmental lighting "
                "and activating crew support protocol."
            )
        })

    # Cardiovascular monitoring
    if bpm > RITMO_CARDIACO_MAX:

        eventos.append({
            "level": "WARNING",
            "system": "Crew Health",
            "message": f"Elevated heart rate: {bpm:.0f} BPM.",
            "action": (
                "Modulating thermal environment "
                "and recommending breathing protocol."
            )
        })

    # Oxygen monitoring
    if spo2 < NIVEL_OXIGENO_MIN:

        eventos.append({
            "level": "CRITICAL",
            "system": "Crew Health",
            "message": f"Low SpO2 detected: {spo2:.1f}%.",
            "action": (
                "Activating supplemental oxygen "
                "at crew workstation."
            )
        })

    # Atmospheric monitoring
    if co2 > CALIDAD_AIRE_PPM_MAX:

        eventos.append({
            "level": "WARNING",
            "system": "Atmosphere",
            "message": f"Elevated CO2 detected: {co2:.0f} ppm.",
            "action": (
                "Activating backup ventilation "
                "and CO2 removal."
            )
        })

    if not eventos:

        eventos.append({
            "level": "NOMINAL",
            "system": "Life Support",
            "message": "Crew and atmospheric parameters nominal.",
            "action": "No corrective action required."
        })

    return eventos