import time
import random

# CONFIGURACIÓN DE UMBRALES CRÍTICOS MARCIANOS
UMBRAL_HUMEDAD_MIN = 30.0   # Porcentaje de humedad en raíz (%)
UMBRAL_PH_MIN = 5.5        # Límite inferior de pH nutricional
UMBRAL_PH_MAX = 6.5        # Límite superior de pH nutricional
NIVEL_AGUA_CRITICO = 10.0   # Porcentaje del reservorio hidropónico (%)

def leer_sensores_cultivo():
   """
   Simulación de adquisición de datos del módulo IoT en zona de cultivo.
   En entorno real, se sustituye por lecturas I2C/SPI de la Raspberry Pi.
   """
   humedad = random.uniform(20.0, 50.0)
   ph = random.uniform(5.0, 7.0)
   nivel_tanque = random.uniform(5.0, 100.0)
   # Simulación de lectura de geófonos en la base
   sismo_detectado = random.choice([False, False, False, True])
   return humedad, ph, nivel_tanque, sismo_detectado

def ejecutar_sistema_adaptativo():
   print("==========================================================")
   print("   SISTEMA CIBERNÉTICO DE CULTIVO AUTÓNOMO - HÁBITAT MARTE")
   print("==========================================================")
   
   while True:
       humedad, ph, nivel_tanque, sismo = leer_sensores_cultivo()
       print(f"\n[TELEMETRÍA]: Humedad: {humedad:.1f}% | pH: {ph:.2f} | Tanque: {nivel_tanque:.1f}%")
       
       # 1. PROTOCOLO DE SEGURIDAD SÍSMICA (Prioridad Absoluta)
       if sismo:
           print("  [ALERTA SÍSMICA]: Vibración detectada en el suelo marciano.")
           print("  [ACCIÓN AUTOMÁTICA]: Cerrando válvulas solenoides y aislando fluidos.")
           time.sleep(3)
           continue

       # 2. GESTIÓN AUTÓNOMA DEL AGUA Y NUTRIENTES
       if nivel_tanque < NIVEL_AGUA_CRITICO:
           print("  [ALERTA DE RECURSO]: Reservorio de agua por debajo del nivel seguro.")
           print("  [ACCIÓN AUTOMÁTICA]: Riego en modo de reserva extrema.")
       elif humedad < UMBRAL_HUMEDAD_MIN:
           print("  [ESTADO]: Humedad de raíz insuficiente.")
           print("  [ACCIÓN AUTOMÁTICA]: Activando bomba hidropónica por 15 segundos.")
       else:
           print("  [ESTADO]: Humedad en rango óptimo de crecimiento.")

       # 3. CONTROL DE ESTABILIDAD QUÍMICA (pH)
       if not (UMBRAL_PH_MIN <= ph <= UMBRAL_PH_MAX):
           print(f"  [AJUSTE QUÍMICO]: pH fuera de especificación ({ph:.2f}). Actuando dosificador.")

       time.sleep(5) # Intervalo de ciclo de monitoreo

if __name__ == "__main__":
   try:
       ejecutar_sistema_adaptativo()
   except KeyboardInterrupt:
       print("\n[INFO]: Sistema de cultivo pausado por intervención del operador.")