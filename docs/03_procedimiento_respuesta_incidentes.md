# Procedimiento de Respuesta a Incidentes — LogWatcher
**Versión:** 1.0  
**Fecha:** 2026-05-29  
**Autor:** Diego Armando Álvarez Valero  
**Referencia normativa:** ISO/IEC 27035:2023 — Gestión de Incidentes de Seguridad

---

## 1. Propósito

Establecer el procedimiento que debe seguir el analista de seguridad 
cuando LogWatcher detecta y reporta un incidente, garantizando una 
respuesta ordenada, documentada y alineada a estándares internacionales.

## 2. Fases del procedimiento

### Fase 1 — Detección
LogWatcher detecta automáticamente el evento y lo reporta a Grafana Loki.

| Acción | Responsable |
|--------|-------------|
| Verificar alerta en dashboard de Grafana | Analista de seguridad |
| Identificar código IMDRF del evento | Analista de seguridad |
| Determinar severidad (INFO / WARNING / CRITICAL) | Analista de seguridad |

### Fase 2 — Análisis
El analista evalúa el contexto del evento antes de actuar.

**Para eventos WARNING (intento_fallido):**
- ¿La IP es conocida o esperada?
- ¿El usuario objetivo es válido en el sistema?
- ¿Hay otros intentos recientes desde la misma IP?

**Para eventos CRITICAL (fuerza_bruta):**
- ¿Cuántos intentos registra la IP en el dashboard?
- ¿A qué usuarios está atacando?
- ¿El ataque sigue activo en tiempo real?

### Fase 3 — Contención
Acciones inmediatas para limitar el impacto del incidente.

| Severidad | Acción de contención |
|-----------|---------------------|
| WARNING | Monitoreo activo, sin bloqueo inmediato |
| CRITICAL | Bloquear IP en firewall, notificar a responsable de TI |

**Comando para bloquear IP en Linux:**
```bash
sudo iptables -A INPUT -s <IP_ATACANTE> -j DROP
```

### Fase 4 — Documentación
Todo incidente CRITICAL debe quedar documentado con:

- Fecha y hora de detección
- IP origen del ataque
- Usuarios objetivo
- Cantidad de intentos registrados
- Acciones tomadas
- Resultado

### Fase 5 — Revisión post-incidente
Después de contener el incidente:

- ¿El umbral de fuerza bruta es adecuado?
- ¿Se debe ajustar alguna configuración de LogWatcher?
- ¿El incidente reveló una vulnerabilidad en la infraestructura?

---

## 3. Matriz de escalación

| Severidad | Primera respuesta | Escalación |
|-----------|------------------|------------|
| INFO | Sin acción requerida | — |
| WARNING | Analista de seguridad | Si persiste más de 1 hora |
| CRITICAL | Analista de seguridad | Responsable de TI inmediatamente |

## 4. Tiempos de respuesta objetivo

| Severidad | Tiempo de detección | Tiempo de contención |
|-----------|--------------------|--------------------|
| WARNING | 15 minutos | 1 hora |
| CRITICAL | 5 minutos | 30 minutos |

---

*Este procedimiento debe revisarse después de cada incidente CRITICAL 
y actualizarse al menos una vez al año.*
