import numpy as np
import math
from config import BURST_WINDOW_SECONDS
from data_structures import FeatureVector, PacketData


def extract_features(packet_snapshot: list[PacketData], window_end_time) -> FeatureVector:
    total_pkts = len(packet_snapshot)
    if total_pkts == 0:
        return FeatureVector(window_end_time, window_end_time, [0.0] * 13, {'Total_Packets': 0})

    # ОДИН раз конвертируем поля в C-based вектора Numpy
    # Заменяет медленные for-loops на генераторы с четкой типизацией памяти
    lengths = np.fromiter((p.length for p in packet_snapshot), dtype=np.int32)
    timestamps = np.fromiter((p.timestamp.timestamp() for p in packet_snapshot), dtype=np.float64)

    # Списки протоколов (Векторизуемые фильтры)
    tcp_mask = np.fromiter((p.is_tcp for p in packet_snapshot), dtype=bool)
    udp_mask = np.fromiter((p.is_udp for p in packet_snapshot), dtype=bool)

    # ---------------------------------------------
    # 1. СТАТИСТИЧЕСКАЯ БЛОКОВКА ПРИЗНАКОВ (FAST-PATH)
    f1 = float(total_pkts)
    f2 = float(np.sum(lengths))
    f3 = float(np.median(lengths))

    # Считаем уникальные порты быстро через np.unique
    dst_ports = [p.dst_port for p in packet_snapshot if p.dst_port is not None]
    if dst_ports:
        # Супербыстрый метод расчета Энтропии Шеннона на C backend (NumPy)
        _, counts = np.unique(dst_ports, return_counts=True)
        probs = counts / counts.sum()
        f4 = float(-np.sum(probs * np.log2(probs)))
    else:
        f4 = 0.0

    # Быстрый расчет TCP флагов
    syns = sum(1 for p in packet_snapshot if p.is_tcp and p.tcp_flags.get('SYN') and not p.tcp_flags.get('ACK'))
    f5 = float(syns / np.sum(tcp_mask)) if np.any(tcp_mask) else 0.0

    f6 = float(np.sum(udp_mask) / f1)

    # Работа со строками остается в Set, но изолируется (Python strings)
    f7 = float(len(set(p.src_ip for p in packet_snapshot)))

    tcp_count = np.sum(tcp_mask)
    f8 = float(tcp_count / f1)

    non_t_u_count = f1 - tcp_count - np.sum(udp_mask)
    f9 = float(non_t_u_count / f1)

    f10 = float(len(set(p.dst_ip for p in packet_snapshot)))

    # ---------------------------------------------
    # 2. ВРЕМЕННОЙ БЛОК: РАЗРЫВЫ (Векторная диффенеренциация NumPy)
    if total_pkts > 1:
        # NumPy diff делает разницу за доли миллисекунд
        diffs = np.diff(timestamps)
        f11, f12 = float(np.mean(diffs)), float(np.std(diffs))

        # Переписанная сложная логика окон burst (без for-comprehension O(N^2) нагрузки)
        # О(N) решение через broadcasting, избегает OOM.
        max_burst = 0.0
        if total_pkts > 0:
            time_threshold = timestamps[-1] - BURST_WINDOW_SECONDS
            max_burst = float(np.sum(timestamps >= time_threshold))
        f13 = max_burst
    else:
        f11 = f12 = f13 = 0.0

    vector = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13]
    return FeatureVector(
        start_time=packet_snapshot[0].timestamp,
        end_time=window_end_time,
        features=[round(v, 6) for v in vector],  # Обрубаем float_errors (65463.00000002 -> 65463.0)
        source_info={'Total_Packets': total_pkts}
    )