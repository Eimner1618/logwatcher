# LogWatcher — Analizador de logs de seguridad
# Autor: Diego Álvarez
# v2.0 — Integración con Grafana Loki

import re
import hashlib
import logging
import logging_loki
from collections import Counter
from datetime import datetime

# ========== CONFIGURACIÓN LOKI ==========
logging_loki.emitter.LokiEmitter.level_tag = "level"

handler = logging_loki.LokiHandler(
    url="http://localhost:3100/loki/api/v1/push",
    tags={"application": "logwatcher"},
    version="1",
)

logger = logging.getLogger("logwatcher")
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# ========== MAPEO DE EVENTOS ESTÁNDAR ==========
mapeo_seguridad = {
    "intento_fallido": {"codigo": "IMDRF_B0101", "level": "WARNING"},
    "fuerza_bruta":    {"codigo": "IMDRF_A050101", "level": "CRITICAL"},
    "login_exitoso":   {"codigo": "IMDRF_C020301", "level": "INFO"},
}

# ========== FUNCIÓN: ANONIMIZAR USUARIO ==========
def anonimizar(usuario):
    return hashlib.sha256(usuario.encode()).hexdigest()[:12]

# ========== FUNCIÓN: ENVIAR EVENTO A LOKI ==========
def reportar_evento(ip, tipo_evento, usuario):
    metadata = mapeo_seguridad.get(tipo_evento, {"codigo": "UNKNOWN", "level": "INFO"})
    usuario_hash = anonimizar(usuario)

    payload = {
        "event_code": metadata["codigo"],
        "ip": ip,
        "client_id": usuario_hash,
    }

    mensaje = f"[{metadata['codigo']}] IP: {ip} | Usuario: {usuario_hash} | Evento: {tipo_evento}"

    if metadata["level"] == "CRITICAL":
        logger.critical(mensaje, extra={"tags": payload})
    elif metadata["level"] == "WARNING":
        logger.warning(mensaje, extra={"tags": payload})
    else:
        logger.info(mensaje, extra={"tags": payload})

    print(f"  → Enviado a Loki: {mensaje}")

# ========== ANÁLISIS DEL LOG ==========
LOG_FILE = "sample_auth.log"

intentos_fallidos = []
logins_exitosos = []
ips_atacantes = []
ips_por_usuario = {}

print("=" * 55)
print("     LOGWATCHER v2.0 — INTEGRACIÓN CON LOKI")
print("=" * 55)
print("\nAnalizando y enviando eventos...\n")

with open(LOG_FILE, "r") as f:
    for linea in f:

        ip_match = re.search(r"from (\d+\.\d+\.\d+\.\d+)", linea)
        user_match = re.search(r"for (\w+) from", linea)

        ip = ip_match.group(1) if ip_match else "unknown"
        usuario = user_match.group(1) if user_match else "unknown"

        if "Failed password" in linea:
            intentos_fallidos.append(linea.strip())
            ips_atacantes.append(ip)

            # Rastrear qué usuarios intentó cada IP
            if ip not in ips_por_usuario:
                ips_por_usuario[ip] = set()
            ips_por_usuario[ip].add(usuario)

            reportar_evento(ip, "intento_fallido", usuario)

        elif "Accepted password" in linea:
            logins_exitosos.append(linea.strip())
            reportar_evento(ip, "login_exitoso", usuario)

# ========== DETECTAR FUERZA BRUTA ==========
conteo_ips = Counter(ips_atacantes)

print("\n" + "=" * 55)
print(f"Total intentos fallidos : {len(intentos_fallidos)}")
print(f"Logins exitosos         : {len(logins_exitosos)}")

print("\nIPs con intentos fallidos:")
for ip, cantidad in conteo_ips.most_common():
    if cantidad >= 3:
        print(f"   {ip} — {cantidad} intentos  FUERZA BRUTA DETECTADA")
        reportar_evento(ip, "fuerza_bruta", "multiple")
    else:
        print(f"   {ip} — {cantidad} intentos")

print("\n" + "=" * 55)
print("Eventos enviados a Grafana Loki.")
print("=" * 55)
