import multiprocessing
from datetime import datetime
from scapy.all import sniff, IP, TCP, UDP, DNS
from config import sniffer_logger
from data_structures import PacketData
from queue import Full

BATCH_SIZE = 100  # Уменьшили батч для более плавной передачи с роутеров


class PacketSniffer:
    def __init__(self):
        # Ограничиваем очередь, чтобы не съесть всю оперативку роутера
        self.queue = multiprocessing.Queue(maxsize=200)
        self.stop_event = multiprocessing.Event()
        self.process = None
        self.iface_to_use = None

    def set_config(self, iface_name: str, filter_str: str):
        self.iface_to_use = iface_name

    def start_sniffing(self):
        if self.process and self.process.is_alive(): return
        self.stop_event.clear()
        self.process = multiprocessing.Process(
            target=self._sniff_process_loop,
            args=(self.iface_to_use, self.queue, self.stop_event),
            daemon=True
        )
        self.process.start()

    def stop_sniffing(self):
        if self.process:
            self.stop_event.set()
            self.process.join(2.0)

    def get_packets(self) -> list:
        merged = []
        while not self.queue.empty():
            try:
                merged.extend(self.queue.get_nowait())
            except:
                break
        return merged

    @staticmethod
    def _sniff_process_loop(iface, queue, stop_evt):
        _local_batch = []

        def cb(packet):
            if not packet.haslayer(IP): return
            ip = packet[IP]
            is_tcp, is_udp = packet.haslayer(TCP), packet.haslayer(UDP)

            p_data = PacketData(
                timestamp=datetime.now(), src_ip=ip.src, dst_ip=ip.dst,
                src_port=packet[TCP].sport if is_tcp else None,
                dst_port=packet[TCP].dport if is_tcp else None,
                length=len(packet), is_tcp=is_tcp, is_udp=is_udp,
                tcp_flags={'SYN': 'S' in str(packet[TCP].flags)} if is_tcp else {},
                protocol='TCP' if is_tcp else ('UDP' if is_udp else 'OTHER'),
                domain=None  # DNS дешифровка на роутерах опциональна (CPU heavy)
            )
            _local_batch.append(p_data)

            if len(_local_batch) >= BATCH_SIZE:
                try:
                    queue.put(_local_batch[:], timeout=1)
                    _local_batch.clear()
                except Full:
                    _local_batch.clear()  # Drop packets if queue is stuck

        sniff(iface=iface, store=0, prn=cb, stop_filter=lambda _: stop_evt.is_set())