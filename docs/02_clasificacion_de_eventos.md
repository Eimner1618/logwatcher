# Clasificación de Eventos — LogWatcher
**Versión:** 1.0  
**Fecha:** 2026-05-29  
**Autor:** Diego Armando Álvarez Valero  
**Referencia normativa:** ISO/IEC 27035:2023 — Gestión de Incidentes, IMDRF

---

## 1. Propósito

Definir la clasificación estándar de eventos detectados por LogWatcher,
su nivel de severidad y el mapeo a códigos internacionales IMDRF para
garantizar interoperabilidad con sistemas SIEM.

## 2. Tabla de clasificación de eventos

| Código IMDRF | Evento | Severidad | Descripción |
|-------------|--------|-----------|-------------|
| IMDRF_B0101 | intento_fallido | WARNING | Un intento de acceso SSH fallido desde una IP |
| IMDRF_A050101 | fuerza_bruta | CRITICAL | IP supera el umbral de intentos fallidos configurado |
| IMDRF_C020301 | login_exitoso | INFO | Acceso SSH autenticado correctamente |
| UNKNOWN | evento_desconocido | INFO | Evento no clasificado en el mapeo actual |

## 3. Niveles de severidad

| Nivel | Descripción | Acción recomendada |
|-------|-------------|-------------------|
| INFO | Evento informativo, operación normal | Registro y monitoreo pasivo |
| WARNING | Comportamiento sospechoso, requiere atención | Revisión por analista |
| CRITICAL | Amenaza activa detectada | Respuesta inmediata según procedimiento |

## 4. Mapeo a controles ISO/IEC 27001:2022

| Evento | Control ISO 27001 | Descripción del control |
|--------|------------------|------------------------|
| intento_fallido | 8.15 — Logging | Registro de eventos de acceso |
| fuerza_bruta | 8.16 — Monitoring | Monitoreo de actividades sospechosas |
| login_exitoso | 8.15 — Logging | Registro de accesos autorizados |

## 5. Anonimización de datos

En cumplimiento con el principio de minimización de datos (ISO/IEC 27001 — 
Control 5.34 y LFPDPPP en México), LogWatcher anonimiza los nombres de usuario 
mediante hash SHA-256 truncado a 12 caracteres antes de enviar cualquier evento 
al SIEM.

**Ejemplo:**
- Usuario original: `root`
- Hash generado: `4813494d137e`

Esto garantiza que el sistema detecta amenazas sin almacenar datos 
personales identificables.

## 6. Umbral de fuerza bruta

El umbral por defecto es de **3 intentos fallidos** desde la misma IP.
Este valor es configurable en el código fuente mediante la variable:

```python
UMBRAL_FUERZA_BRUTA = 3
```

Se recomienda ajustar este valor según el perfil de riesgo del entorno:

| Entorno | Umbral recomendado |
|---------|--------------------|
| Producción crítica | 3 intentos |
| Producción estándar | 5 intentos |
| Laboratorio / desarrollo | 10 intentos |

---

*Documento sujeto a revisión ante nuevos tipos de eventos o cambios en estándares IMDRF.*
