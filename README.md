# Detección de Postura - Digitales 3

**Autor:** David Diaz  
**Fecha:** Octubre 2025  

---

## Descripción General del Proyecto

Este proyecto es una **aplicación en Python** que detecta si una persona está **de pie o sentada** usando **MediaPipe Pose**, con **procesamiento concurrente** mediante hilos y sincronización con mutex, y mostrando resultados en **Streamlit**.  

**Características principales:**

- Captura de video en tiempo real.
- Detección de landmarks del cuerpo (caderas y rodillas).
- Clasificación de postura: 🧍 De pie / 🪑 Sentado.
- Interfaz interactiva con Streamlit.
- Docker **no recomendado** por restricciones de acceso a cámara física.

---

## Ejecución

Activar entorno virtual y ejecutar la aplicación:

```bash
source venv/bin/activate
streamlit run main1.py
```
---

## link del pdf para visualizar el informe del trabajo

[Ver informe PDF](pdf/quiz1_digitales3_3_corte.pdf)

---

## link de video que evidencia el resultado final de la aplicacion 

[Ver video](https://youtu.be/kdUeHSyK_Tk)
