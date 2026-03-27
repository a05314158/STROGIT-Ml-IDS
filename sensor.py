import time
import requests
import json
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor

from sniffer import PacketSniffer
from feature_engineer import extract_features
from scapy.all import conf


def get_args():
    parser = argparse.ArgumentParser(description='ML-IDS Zero-Trust Edge Sensor Node')
    parser.add_argument('--server', type=str, help='IP сервера (Core Gateway)')
    parser.add_argument('--apikey', type=str, help='API ключ для аутентификации')
    parser.add_argument('--iface', type=str, help='WAN/LAN Порт зеркала')
    parser.add_argument('--list', action='store_true', help='Карта сетевых девайсов сервера')
    return parser.parse_args()


def list_interfaces():
    print("\n[?] Активные Сетевые Карты на Зонде:")
    print(f"{'INDEX':<10} {'NAME':<35} {'IP'}")
    print("-" * 65)
    for iface in conf.ifaces.values():
        print(f"{iface.index:<10} {iface.name:<35} {iface.ip}")
    print("-" * 65)


# ----- ВЫДЕЛЕННЫЙ АСИНХРОННЫЙ ОТПРАВИТЕЛЬ С ДЕТАЧД(Background) ДВИЖЕНИЕМ -----
def send_http_payload(server_url, payload, api_key):
    try:
        # Быстрый таймаут чтобы очередь TCP соединений ОС не "вешалась"
        headers = {'Authorization': f'Bearer {api_key}'}
        res = requests.post(server_url, json=payload, headers=headers, timeout=2.5)
        if res.status_code != 202:
            print(f"[!] Предупреждение Кораблестроения (Sync error) | Core Reply: HTTP {res.status_code} ")
    except requests.Timeout:
        print("\r[!!] Gateway Server is currently heavily congested (timeout) ", end="\r")
    except requests.RequestException as e:
        print(f"\r[!!] Core Node Disconnected | Net I/O error ", end="\r")


def run_sensor(server_ip, api_key, interface):
    SERVER_URL = f"http://{server_ip}:5000/api/sensor_data"

    sniffer = PacketSniffer()
    sniffer.set_config(interface, "ip")
    sniffer.start_sniffing()

    print(f"\n[bold]==========[ ADVANCED SOC EDGE SCANNER ENABLED ]==========[/bold]")
    print(f"[*] Цель (Uplink Node):  {SERVER_URL}")
    print(f"[*] API Key:             {api_key[:20]}...")
    print(f"[*] Привязанный порт L2: {interface}")
    print("[*] Engine status: NumPy Async Hardware accelerated routing.")
    print("==================================================================\n")

    # Держим постоянные воркеры в пуле ОС. Не мешаем циклу time.sleep захвата!
    # Если пакет готов - кинули пуле и забыли.
    http_workers = ThreadPoolExecutor(max_workers=3)

    accumulated_packets = []  # Накапливаем пакеты между отправками
    last_send_time = time.time()

    try:
        while True:
            # КВАНТ ВРЕМЕНИ ДЛЯ СДВИГА ОКНА АНАЛИЗА
            time.sleep(0.05)  # Очень короткий интервал для постоянного опроса
            packets = sniffer.get_packets()

            # Добавляем новые пакеты к накопленным
            accumulated_packets.extend(packets)

            current_time = time.time()
            
            # Отправляем пакеты если:
            # 1. Набрались пакеты И (их >= 10 или прошло 0.5 секунды с последней отправки)
            should_send = len(accumulated_packets) > 0 and \
                         (len(accumulated_packets) >= 10 or current_time - last_send_time >= 0.5)

            if should_send:
                fv = extract_features(accumulated_packets, current_time)

                # Генерация матриц логов PostgreSQL напрямую (со словарем O(1) поиска)
                ip_stats = {}
                dom_stats = {}
                for p in accumulated_packets:
                    ip_stats[p.src_ip] = ip_stats.get(p.src_ip, 0) + p.length
                    if p.domain: dom_stats[p.domain] = dom_stats.get(p.domain, 0) + 1

                payload = {
                    "features": fv.features,
                    "packet_count": len(accumulated_packets),
                    "total_bytes": sum(ip_stats.values()),  # Находим напрямую без прогона for lengths
                    "ip_summary": ip_stats,
                    "domain_summary": dom_stats
                }

                print(f"[+] Транзитом снято: {len(accumulated_packets):<5} PKTS  | Передача: Asynchronous Uplink    ", end="\r")

                # --- Вбрасываем работу в асинхронную трубу ThreadPool-а ---
                http_workers.submit(send_http_payload, SERVER_URL, payload, api_key)

                # Очищаем накопленные пакеты только после отправки
                accumulated_packets.clear()
                last_send_time = current_time
            else:
                print(f"[•] Тишина эфира... [CPU Thread Sleeping]               ", end="\r")

    except KeyboardInterrupt:
        sniffer.stop_sniffing()
        http_workers.shutdown(wait=False)  # Принудительно гасим очереди ОС
        print("\n\n[*] Датчик снят с линии L2 (SIGINT HALTED). Коннект прерван.")


if __name__ == "__main__":
    args = get_args()
    if args.list:
        list_interfaces()
        sys.exit()

    if not args.server or not args.apikey or not args.iface:
        print("\n[!] ОШИБКА ДАТЧИКА: Отсутствуют Core Configs для Edge Device.")
        print("--> Пример: python sensor.py --server 192.168.0.50 --apikey YOUR_API_KEY --iface Wi-Fi")
        print("--> Помощь: python sensor.py --list\n")
        sys.exit()

    run_sensor(args.server, args.apikey, args.iface)