# Política de Uso — LogWatcher
**Versión:** 1.0  
**Fecha:** 2026-05-29  
**Autor:** Diego Armando Álvarez Valero  
**Referencia normativa:** ISO/IEC 27001:2022 — Control 8.15 (Logging), ISO/IEC 27035

---

## 1. Propósito

LogWatcher es una herramienta de monitoreo de seguridad diseñada para analizar 
logs de autenticación SSH en sistemas Linux, detectar comportamientos anómalos 
y enviar eventos estructurados a un sistema SIEM para su correlación y visualización.

## 2. Alcance

Esta política aplica a:
- Administradores de sistemas que implementen LogWatcher
- Analistas de seguridad que operen el dashboard de Grafana
- Cualquier entorno Linux donde se despliegue la herramienta

## 3. Capacidades de la herramienta

| Capacidad | Descripción |
|-----------|-------------|
| Detección de intentos fallidos | Identifica intentos de acceso SSH no autorizados |
| Detección de fuerza bruta | Alerta cuando una IP supera el umbral de intentos configurado |
| Registro de accesos exitosos | Documenta logins válidos para auditoría |
| Anonimización de usuarios | Hash SHA-256 para cumplimiento de privacidad |
| Envío a SIEM | Integración con Grafana Loki para centralización de logs |

## 4. Limitaciones

LogWatcher **no** reemplaza a un SIEM completo. Sus limitaciones incluyen:

- No realiza correlación de eventos entre múltiples fuentes
- No bloquea IPs automáticamente (requiere integración con firewall)
- Monitorea únicamente logs SSH — no cubre otros vectores de ataque
- Requiere acceso de lectura al archivo de log del sistema

## 5. Uso permitido

- Monitoreo de servidores Linux en entornos de producción, staging o laboratorio
- Análisis forense de intentos de acceso no autorizados
- Integración como componente de una arquitectura SIEM más amplia

## 6. Uso no permitido

- Monitoreo de sistemas sin autorización explícita del propietario
- Uso como única medida de seguridad en entornos críticos
- Modificación del código para suprimir alertas o anonimización

## 7. Configuración mínima recomendada

| Parámetro | Valor recomendado |
|-----------|-------------------|
| Umbral de fuerza bruta | 3 intentos (ajustable según entorno) |
| Retención de logs en Loki | 30 días mínimo |
| Acceso al dashboard | Restringido a personal autorizado |

## 8. Responsabilidades

| Rol | Responsabilidad |
|-----|----------------|
| Administrador | Despliegue, configuración y mantenimiento |
| Analista de seguridad | Revisión de alertas y respuesta a incidentes |
| Responsable de TI | Autorización de uso y revisión periódica |

---

*Documento sujeto a revisión anual o ante cambios significativos en la herramienta.*
