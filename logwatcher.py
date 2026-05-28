# LogWatcher — Analizador de logs de seguridad
# Autor: Diego Álvarez
# v2.1 — Monitoreo continuo en tiempo real

import re
import hashlib
import logging
import logging_loki
import time
import os
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

# ========== CONFIGURACIÓN ==========
# Cambia esta ruta a /var/log/auth.log para entorno real
LOG_FILE = "sample_auth.log"
UMBRAL_FUERZA_BRUTA = 3  # Intentos para considerar fuerza bruta

# ========== MAPEO DE EVENTOS ESTÁNDAR ==========
mapeo_seguridad = {
    "intento_fallido": {"codigo": "IMDRF_B0101",   "level": "WARNING"},
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

    print(f"  [{datetime.now().strftime('%H:%M:%S')}] → {mensaje}")

# ========== FUNCIÓN: PROCESAR LÍNEA ==========
intentos_por_ip = Counter()

def procesar_linea(linea):
    ip_match   = re.search(r"from (\d+\.\d+\.\d+\.\d+)", linea)
    user_match = re.search(r"for (\w+) from", linea)

    ip      = ip_match.group(1)   if ip_match   else "unknown"
    usuario = user_match.group(1) if user_match else "unknown"

    if "Failed password" in linea:
        intentos_por_ip[ip] += 1
        reportar_evento(ip, "intento_fallido", usuario)

        # Detectar fuerza bruta en tiempo real
        if intentos_por_ip[ip] == UMBRAL_FUERZA_BRUTA:
            print(f"\n  ⚠️  ALERTA: Fuerza bruta detectada desde {ip}\n")
            reportar_evento(ip, "fuerza_bruta", usuario)

    elif "Accepted password" in linea:
        reportar_evento(ip, "login_exitoso", usuario)

# ========== MONITOREO CONTINUO ==========
def monitorear(log_file):
    print("=" * 55)
    print("   LOGWATCHER v2.1 — MONITOREO EN TIEMPO REAL")
    print("=" * 55)
    print(f"   Monitoreando: {log_file}")
    print(f"   Enviando eventos a: Grafana Loki")
    print(f"   Umbral fuerza bruta: {UMBRAL_FUERZA_BRUTA} intentos")
    print("=" * 55)
    print("   Presiona Ctrl+C para detener\n")

    # Abrir el archivo y moverse al final
    with open(log_file, "r") as f:
        # En modo tiempo real, ir al final del archivo
        f.seek(0, os.SEEK_END)

        print("   Esperando nuevos eventos...\n")

        while True:
            linea = f.readline()
            if linea:
                linea = linea.strip()
                if "Failed password" in linea or "Accepted password" in linea:
                    procesar_linea(linea)
            else:
                time.sleep(0.5)  # Esperar medio segundo antes de volver a leer

# ========== INICIO ==========
if __name__ == "__main__":
    try:
        monitorear(LOG_FILE)
    except KeyboardInterrupt:
        print("\n\n" + "=" * 55)
        print("   LogWatcher detenido.")
        print(f"   IPs monitoreadas: {len(intentos_por_ip)}")
        for ip, cantidad in intentos_por_ip.most_common():
            print(f"   {ip} — {cantidad} intentos")
        print("=" * 55)
    except FileNotFoundError:
        print(f"\n  ERROR: No se encontró el archivo {LOG_FILE}")
        print("  Verifica la ruta del log.") 
