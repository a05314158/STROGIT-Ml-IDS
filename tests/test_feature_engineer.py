from datetime import datetime, timedelta
import numpy as np
from feature_engineer import extract_features
from data_structures import PacketData


def build_mock_stream(packet_count=50) -> list[PacketData]:
    """Генератор фейковых "взломанных" пакетов сканирования портов."""
    base_time = datetime.now()
    stream = []
    for i in range(packet_count):
        # Эмуляция жесткого SYN флуда NMAP по TCP
        stream.append(PacketData(
            timestamp=base_time + timedelta(milliseconds=i * 2),
            src_ip="10.0.0.5",
            dst_ip="192.168.1.1",
            src_port=55555 + i,
            dst_port=80,
            length=60,
            is_tcp=True,
            is_udp=False,
            tcp_flags={'SYN': True},
            protocol="TCP",
            domain=None
        ))
    return stream


def test_feature_extractor_pipeline():
    """Математический NumPy модуль должен сжимать окно до 13 идеальных чисел."""
    packets = build_mock_stream()
    vector = extract_features(packets, window_end_time=datetime.now())

    # Критическая проверка Enterprise (Шейпы Тензора)
    assert len(vector.features) == 13, "Длина вектора ИИ повреждена (отличается от 13)"
    assert vector.source_info['Total_Packets'] == 50

    # Проверка конкретной ML математики:
    # 50 пакетов с длиной 60: sum_length (Feature[1]) == 3000.0
    assert vector.features[1] == 3000.0

    # 100% TCP SYN сканирование означает ratio TCP=1.0, UDP=0.0
    assert vector.features[7] == 1.0  # ratio_tcp
    assert vector.features[5] == 0.0  # ratio_udp
    assert vector.features[4] == 1.0  # 100% SYN Only

    # ML метод генерации
    ai_tensor = np.array([vector.features])
    assert ai_tensor.shape == (1, 13), "Отказ Tensor Shape: ожидалось 1 измерение длины 13."