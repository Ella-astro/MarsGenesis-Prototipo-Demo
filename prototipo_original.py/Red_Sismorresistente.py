
import time
import random

# Umbrales Médicos de Seguridad
RITMO_CARDIACO_MAX = 120    # BPM
NIVEL_OXIGENO_MIN = 95.0    # SpO2 (% en sangre)
CALIDAD_AIRE_PPM_MAX = 1000 # Partículas CO2 en aire (PPM)

def leer_sensores_medicos():
   """Simulación de telemetría biométrica de parches IoT en astronautas."""
   ritmo_cardiaco = random.randint(65, 135)
   oxigeno_sangre = random.uniform(92.0, 100.0)
   co2_ambiente = random.randint(400, 1200)
   alerta_sismica = random.choice([False, False, True])
   return ritmo_cardiaco, oxigeno_sangre, co2_ambiente, alerta_sismica

def monitorear_salud_tripulacion():
   print("==========================================================")
   print("  MÓDULO DE SALUD Y BIENESTAR (ODS 3) - HÁBITAT MARTE")
   print("==========================================================")
   
   while True:
       bpm, spo2, co2, sismo = leer_sensores_medicos()
       print(f"\n[BIOMETRÍA]: Pulso: {bpm} BPM | SpO2: {spo2:.1f}% | CO2: {co2} PPM")
       
       # 1. Impacto Sísmico en la Tripulación
       if sismo:
           print("  [ALERTA SÍSMICA]: Evento telúrico activo.")
           print("  [ACCIÓN]: Ajustando iluminación ambiental y presurizando trajes de soporte.")
       
       # 2. Monitoreo Cardiovascular y Estrés
       if bpm > RITMO_CARDIACO_MAX:
           print("  [ALERTA MÉDICA]: Taquicardia / Estrés elevado.")
           print("  [ACCIÓN]: Modulando ambiente térmico y sugiriendo protocolo de respiración.")
           
       if spo2 < NIVEL_OXIGENO_MIN:
           print("  [EMERGENCIA BIOMÉDICA]: Hipoxia detectada.")
           print("  [ACCIÓN]: Inyectando flujo directo de O2 en estación de trabajo.")

       # 3. Control Atmosférico Local
       if co2 > CALIDAD_AIRE_PPM_MAX:
           print("  [ALERTA AMBIENTAL]: CO2 elevado en módulo.")
           print("  [ACCIÓN]: Forzando depuración en sistema de ventilación de respaldo.")

       time.sleep(4)

if __name__ == "__main__":
   try:
       monitorear_salud_tripulacion()
   except KeyboardInterrupt:
       print("\nSistema médico pausado.")