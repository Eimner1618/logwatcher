# Registro de Cambios — LogWatcher
**Referencia normativa:** ISO/IEC 27001:2022 — Control 8.32 (Change Management)

---

## v2.1 — 2026-05-29
**Tipo de cambio:** Mejora funcional  
**Autor:** Diego Armando Álvarez Valero

### Cambios realizados
- Implementado monitoreo continuo en tiempo real (modo `tail -f`)
- Detección de fuerza bruta en el momento exacto en que ocurre
- El script permanece activo hasta interrupción manual (Ctrl+C)
- Resumen de IPs monitoreadas al detener el servicio

### Motivo
Mejorar la utilidad operativa para analistas — el script anterior 
requería ejecución manual cada vez. El modo continuo permite dejarlo 
corriendo como servicio en segundo plano.

---

## v2.0 — 2026-05-27
**Tipo de cambio:** Evolución arquitectural  
**Autor:** Diego Armando Álvarez Valero

### Cambios realizados
- Integración con Grafana Loki para centralización de logs
- Mapeo de eventos a códigos estándar IMDRF
- Anonimización de usuarios con SHA-256 (cumplimiento GDPR/LFPDPPP)
- Dashboard en Grafana con tres paneles: intentos fallidos, fuerza bruta y logins exitosos
- Despliegue del stack Loki + Grafana + Promtail con Docker

### Motivo
Feedback de la comunidad técnica: el script no debería cargar con 
lógica pesada de correlación. Delegar la inteligencia al SIEM es 
el estándar en entornos de producción.

---

## v1.0 — 2026-05-25
**Tipo de cambio:** Versión inicial  
**Autor:** Diego Armando Álvarez Valero

### Cambios realizados
- Análisis de logs SSH desde archivo estático
- Detección de intentos fallidos y fuerza bruta
- Identificación de IPs sospechosas con contador
- Generación automática de reporte en .txt con fecha y hora

### Motivo
Proyecto inicial para aprendizaje de análisis de logs de seguridad 
y detección de patrones de ataque.

---

*Este registro debe actualizarse con cada versión liberada.*
