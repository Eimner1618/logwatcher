# 🔍 LogWatcher — Analizador de Logs de Seguridad SSH

Herramienta en Python para analizar logs de autenticación Linux,
detectar intentos de fuerza bruta e identificar IPs sospechosas.

## ¿Qué hace?

- Detecta intentos fallidos de login SSH
- Identifica IPs con múltiples intentos (posible fuerza bruta)
- Registra accesos exitosos
- Genera un reporte automático en .txt con fecha y hora

## ¿Por qué es útil?

En un entorno real, los servidores SSH expuestos a internet reciben
cientos de intentos de acceso no autorizado por día. LogWatcher
permite identificar rápidamente qué IPs representan una amenaza
y tomar decisiones: bloquear, alertar o escalar.

## Uso

```bash
python3 logwatcher.py
```

El script analiza `sample_auth.log` y genera un archivo
`reporte_FECHA.txt` con los resultados.

## Ejemplo de salida

==================================================
LOGWATCHER — REPORTE DE SEGURIDAD
Total intentos fallidos: 13
Logins exitosos: 2
IPs con intentos fallidos:
192.168.1.105 — 6 intentos ⚠️  POSIBLE FUERZA BRUTA
203.0.113.45  — 4 intentos ⚠️  POSIBLE FUERZA BRUTA
198.51.100.7  — 2 intentos
10.0.0.22     — 1 intento

## Tecnologías

- Python 3
- Módulos: `re`, `collections`, `datetime`

## Autor

Diego Álvarez — [LinkedIn](https://linkedin.com/in/diego-armando-álvarez-valero-b248411b6)
