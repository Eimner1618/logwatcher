# LogWatcher — Analizador de logs de seguridad
# Autor: Diego Álvarez

import re
from collections import Counter
from datetime import datetime

# Archivo a analizar
LOG_FILE = "sample_auth.log"

# Contadores
intentos_fallidos = []
logins_exitosos = []
ips_atacantes = []

# Leer el archivo línea por línea
with open(LOG_FILE, "r") as f:
    for linea in f:

        # Detectar intentos fallidos
        if "Failed password" in linea:
            intentos_fallidos.append(linea.strip())

            # Extraer la IP
            ip = re.search(r"from (\d+\.\d+\.\d+\.\d+)", linea)
            if ip:
                ips_atacantes.append(ip.group(1))

        # Detectar logins exitosos
        if "Accepted password" in linea:
            logins_exitosos.append(linea.strip())

# Contar intentos por IP
conteo_ips = Counter(ips_atacantes)

# Mostrar reporte
print("=" * 50)
print("       LOGWATCHER — REPORTE DE SEGURIDAD")
print("=" * 50)

print(f"\n📋 Total de intentos fallidos: {len(intentos_fallidos)}")
print(f"✅ Logins exitosos: {len(logins_exitosos)}")

print("\n🚨 IPs con más intentos fallidos:")
for ip, cantidad in conteo_ips.most_common():
    alerta = " ⚠️  POSIBLE FUERZA BRUTA" if cantidad >= 3 else ""
    print(f"   {ip} — {cantidad} intentos{alerta}")

print("\n✅ Accesos exitosos registrados:")
for login in logins_exitosos:
    print(f"   {login}")

print("\n" + "=" * 50)
print("Análisis completado.")
print("=" * 50)

# Guardar reporte en archivo
fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
nombre_reporte = f"reporte_{fecha}.txt"

with open(nombre_reporte, "w") as reporte:
    reporte.write("=" * 50 + "\n")
    reporte.write("       LOGWATCHER — REPORTE DE SEGURIDAD\n")
    reporte.write("=" * 50 + "\n")
    reporte.write(f"\nFecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    reporte.write(f"Archivo analizado: {LOG_FILE}\n")
    reporte.write(f"\nTotal intentos fallidos: {len(intentos_fallidos)}\n")
    reporte.write(f"Logins exitosos: {len(logins_exitosos)}\n")
    reporte.write("\nIPs con intentos fallidos:\n")
    for ip, cantidad in conteo_ips.most_common():
        alerta = " ⚠️  POSIBLE FUERZA BRUTA" if cantidad >= 3 else ""
        reporte.write(f"   {ip} — {cantidad} intentos{alerta}\n")
    reporte.write("\nAccesos exitosos:\n")
    for login in logins_exitosos:
        reporte.write(f"   {login}\n")
    reporte.write("\n" + "=" * 50 + "\n")

print(f"\n📄 Reporte guardado como: {nombre_reporte}")

