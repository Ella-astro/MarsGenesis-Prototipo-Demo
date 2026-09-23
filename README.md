# Simulador de Red de Soporte Vital Resiliente
**Panel de monitoreo de sistemas de soporte vital para ambientes extremos.**

_MarsGénesis (Equipo 93) - Mars Challenge 2026_

Simulador interactivo de un sistema autónomo, redundante y resiliente de soporte vital desarrollado para un hábitat en Marte, diseñado
para operar en ambientes hostiles afectados por actividad sísmica.

Resistente. Redundante. Resiliente.

**Demostración interactiva: https://marsgenesis-prototipo-demo.streamlit.app/**

![mars-hab-demo](https://github.com/Ella-astro/MarsGenesis-Prototipo-Demo/blob/main/assets/mars-hab-demo.gif)

---

## Resumen del proyecto
Al prepararnos para futuras misiones tripuladas a Marte, es esencial diseñar viviendas capaces de operar en entornos extremos, hostiles y con
condiciones ambientales poco predecibles. Uno de los factores ambientales principales a considerar en el entorno del planeta son los sismos,
o marsquakes, los cuales amenazan la estabilidad de cualquier estructura en su superficie. La Red de Soporte Vital Resiliente demuestra
una arquitectura resiliente y automatizada para tomar decisiones autónomas ante situaciones críticas ocasionadas por eventos ambientales o fallas
técnicas en un hábitat marciano.

El simulador permite al usuario seleccionar uno de seis eventos en un hábitat tripulada y observar el funcionamiento de múltiples sistemas de
soporte vital al detectar el evento, activar una respuesta autónoma, estabilizar los sistemas, y continuar monitoreando su estado.
Esta cadena de eventos se registra en un Historial de Eventos, así como un Historial de Telemetría para analizar los cambios en el estado de
cada sistema simulado.

---

## Fundamento del diseño
En el ambiente hostil y sísmicamente activo de Marte, las estructuras rígidas se vuelven frágiles y los sistemas centralizados poco fiables.
Necesitamos sistemas interconectados, confiables y resilientes bajo condiciones variables. La Red de Soporte Vital Resiliente es un prototipo
diseñado con estos factores en su fundamento. Demuestra un sistema integrado, descentralizado y sin puntos únicos de falla, desarrollado como
una interfaz confiable para una tripulación de seis miembros en una misión de larga duración en Marte.

El prototipo integra los siguientes subsistemas en una red interconectada:
- Soporte vital de la tripulación: frecuencia cardiaca, niveles de oxígeno y dióxido de carbono en el aire.
- Zona de cultivos hidropónicos: reserva de agua, pH de su solución nutritiva, humedad radicular.

El panel de monitoreo muestra el estado de cada subsistema en tiempo real, además de resgistrar cambios en su condición a lo largo del tiempo
en dos historiales de datos: Telemetría y Eventos. La programación automatizada permite mantener niveles estables en los múltiples subsistemas
aún durante eventos inesperados o condiciones degradadas dentro del hábitat debido a un agotamiento progresivo de los recursos disponibles.

---

## Base científica
Los subsistemas se seleccionaron con el propósito de demostrar la aplicación de nuestro diseño tanto a sistemas de soporte vital para la
tripulación como para módulos del hábitat, como la zona de cultivo hidropónica.
Estas variables monitoreadas ejemplifican el mecanismo capaz de mantener niveles estables para la tripulación ante posibles fallas o
desequilibrios. Así mismo, la inclusión del sistema de cultivo muestra el mismo concepto para diferentes subsistemas de control ambiental
o sustento vital que consumen y/o reutilizan recursos.

---

## Proceso de desarrollo
El prototipo fue diseñado como parte del diseño de un hábitat marciano sismorresistente. El concepto es escalable a sistemas vitales de mayor
complejidad para realizar pruebas.
Nosotros, el equipo de MarsGénesis, comenzamos con un prototipo simplificado pero demostrable. La interfaz interactiva nació de un primer modelo
de un módulo de cultivo hidropónico.

Expandiendo sobre este primer diseño, posteriormente diseñamos una red redundante de soporte vital para el prototipo del hábitat sismorresistente.
Este fue el punto en el que integramos un enfoque descentralizado y sin punto único de falla de múltiples subsistemas vitales.

**Documentos: Red Sismorresistente y Código de Sistematización de Cultivos** 

Una vez teniendo el modelo base, decidimos programar también una interfaz interactiva funcional, lista para ser evaluada como prototipo.
Manteniendo el mecanismo subyacente, implementamos múltiples elementos UI para visualizar la telemetría, el estado de los sistemas bajo fallas
o condiciones críticas, y sus respuestas autónomas para estabilizarse.

A continuación, hemos incluido ambos modelos anteriores junto con su descripción, los cuales utilizamos como fundación para el prototipo final. El código
fuente también está incluido en este repositorio.

### Código de Sistematización de Cultivos

**Módulo de Automatización Agrícola e Hidroponía (Raspberry Pi / Edge Computing)**

Resumen del Módulo: Este documento contiene la documentación técnica y el código fuente en Python diseñado para la automatización del cultivo
hidropónico en el hábitat marciano. El script implementa lógica de Edge Computing para operar independientemente de la señal de la Tierra, respondiendo
en tiempo real a sismos marcianos (Marsquakes), variaciones de pH, humedad crítica y niveles de reservorio de agua.

**Justificación Arquitectónica del Código**

- Autonomía ante Latencia (Edge Computing): Debido al retraso de comunicación con la Tierra (3 a 22 minutos), las decisiones operacionales de
hidratación y aislamiento no pueden depender de comandos externos.
- Integración con Geófonos (Protección Sísmica): Si los sensores de la cimentación detectan vibraciones sísmicas, el código interrumpe inmediatamente
el flujo de líquidos para evitar rupturas de tuberías y derrames en gravedad reducida.
- Eficiencia Recurso-Demandante: La dosificación no sigue un reloj rígido, sino que responde a lecturas dinámicas de humedad y pH en tiempo real,
optimizando el uso del agua reciclada.

### Red Sismorresistente

**Hábitat Sismorresistente con Red Redundante de Soporte Vital**

Resumen de la Propuesta: El proyecto integra un diseño arquitectónico cilíndrico con domo superior montado sobre cimentación de aislamiento sísmico
(elastomérico / péndulo de fricción). La estructura alberga una red interconectada descentralizada de 4 sistemas críticos de soporte vital sin puntos
únicos de fallo (no single point of failure), garantizando la supervivencia operacional durante y después de eventos sísmicos en Marte (Marsquakes).

**Arquitectura de la Red Interconectada**

Para garantizar que la fallo o desconexión física de un nodo no comprometa la vida en el hábitat, la red de cómputo se organiza bajo una topología
en Malla (Mesh Industrial) mediante unidades autónomas de Edge Computing:

- Descentralización de Nodos: Cada uno de los 4 sistemas opera con un microcontrolador independiente (Raspberry Pi / Controller).
- Conexión Redundante: Protocolo de comunicación bus CAN dual o red MQTT local inalámbrica/cableada cruzada. Si una línea física colapsa durante el sismo,
la información se enruta automáticamente por vías secundarias.
- Autonomía Local: Cada módulo contiene su propia lógica de toma de decisiones sin depender de un servidor central ni de comandos desde la Tierra.

---

## Funcionamiento de la interfaz

El prototipo consiste de un panel de monitoreo de subsistemas dentro de un hábitat marciano, complementado por diferentes escenarios simulados
para introducir inestabilidad en los niveles de ciertos recursos o, enfocado al diseño sismorresistente, un evento sísmico o marsquake.
Este último cuenta con dos posibles resultados: verificación del funcionamiento exitosa, o falla detectada en el sistema de cultivo.

Cada simulación se desarrolla en ciclos, donde cada ciclo representa un paso en el algoritmo del sistema. El usuario selecciona el evento a
simular y manualmente corre cada ciclo, observando la respuesta de los sistemas paso a paso. El proceso se desarrolla en las siguientes etapas:

1. Selección del escenario a simular
2. Inserción del escenario al sistema
3. Respuesta de los sistemas, reflejado en la telemetría y el estado del hábitat (nominal, advertencia, crítico, degradado)
4. Monitoreo y evaluación de los niveles de cada subsistema
5. Advertencia / estado crítico detectado
6. Respuesta autónoma del sistema
7. Estabilización de los sitemas en los ciclos posteriores
8. Registro de los eventos en los historiales de telemetría

**Organización de los archivos**
- app.py: Integración de los subsistemas y diseño de la interfaz
- simulation.py: Simulación de los valores de la telemetría
- cultivation.py: Simulación del sistema de cultivo hidropónico
- life_support.py: Simulación de los sistemas de soporte vital de la tripulación


### Descripción de los escenarios simulados

● Operación Normal: El sistema opera en estado nominal, manteniendo los niveles de cada recurso dentro de sus rangos ideales. No se registran
anomalías en el Historial de Eventos.

● Bajo nivel de oxígeno de la tripulación: Simula una degradación progresiva en el nivel de oxígeno (SpO2) de la tripulación. Cuando este
nivel decae por debajo del umbral establecido, el sistema entra en estado crítico y activa los sitemas de oxígeno suplementarios.
A través de este escenario, se demuestra detección, intervención autónoma, y recuperación posterior del sistema.

● Inestabilidad del pH: Simula la desviación progresiva del nivel de pH del sistema de cultivo de su rango operativo aceptable. Al detectar
la condición, se inserta una dosis química para corregir el desbalance y retornar el cultivo a su condición nominal.

● Pérdida de agua hidropónica: Simula una rápida pérdida de agua en la reserva del hábitat. En el momento en el que la reserva llega a un nivel
crítico (<20% del tanque), el sistema detecta la anomalía y activa las medidas de conservación para reducir el consumo de agua por los sistemas
del hábitat. Este proceso demuestra cómo el agotamiento de un recurso es contenido, seguido por un monitoreo continuo.

● Evento sísmico sin falla: Simula la detección de un sismo en Marte (masquake) y activa el protocolo de protección del sistema.
En lugar de demostrar la respuesta de la estructura del hábitat en sí, el escenario demuestra la transición a estados de seguridad de los
sistemas internos interconectados. De esta manera, se aislan los componentes vulnerables y se mantienen o recuperan las funciones críticas
posterior al evento. Concluido el sismo, el sistema realiza una evaluación post-evento interna para confirmar la operación correcta de los sistemas.

● Evento sísmico con falla: A diferencia del evento sísmico sin falla, este evento incluye la detección de una falla operacional durante la
evaluación post-evento. En este caso, es el circuito del subsistema de agua para el cultivo que presenta una anomalía. El subsistema se aisla
de la red interconectada y se activa el bypass redundante para asegurar que el cultivo continue operando, resultando en un estado degradado pero
estable. Por medio de este escenario, se demuestra el modelo propuesto de detección, contención, aislamiento, y respuesta a fallas detectadas
posterior a eventos críticos, todo mientras que se mantiene el hábitat operando con sus funciones críticas.

---

## Alcance y limitaciones

El prototipo se limita a la simulación conceptual de un panel de monitoreo de múltiples sistemas interconectados. No se afirma que la demostración
sea evidencia de un sistema de monitoreo y control validado, ni que los valores utilizados sean ideales para las condiciones de un hábitat.
El equipo autor **no afirma** las siguientes declaraciones sobre el prototipo presentado:

- El hábitat propuesto sobreviviría físicamente a un evento sísmico en Marte
- Las acciones autónomas representadas en el panel son suficientes para proteger a una tripulación o a un sistema de cultivo en un hábitat
- La telemetría simulada reproduce el funcionamiento completo de sistemas de hardware real
- El sistema de software a sido validado para operaciones de seguridad críticas
- Los umbrales establecidos constituyen especificaciones operativas para un hábitat marciano
- Resultados exitosos dentro de la simulación demuestran validación experimental del diseño del hábitat subyacente

El prototipo se limita a demostrar la lógica e interacción humano-computadora propuesta de un sistema de monitoreo, detección de anomalías,
respuesta autónoma, progreso de estado del sistema, y resiliencia de sistemas interconectados dentro del alcance del proyecto.

---

## Contexto del proyecto y reconocimientos
Este prototipo fue creado por el equipo MarsGénesis (Equipo 93), participante del Mars Challenge 2026.

Los miembros del equipo conservan los derechos de autor. 

Agradecemos al equipo de Mars Challenge y las organizaciones colaboradoras por proveer el espacio y la oportunidad para desarrollar el proyecto presentado.
