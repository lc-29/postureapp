"""
Các hàm tiện ích dùng chung:
- Tính góc
- Chuẩn hóa landmark
- Kiểm tra đường dẫn
- Xử lý lỗi an toàn
"""

import math


def calculate_angle(a, b, c):
    """
    Tính góc ABC từ 3 điểm a, b, c.
    Mỗi điểm có dạng (x, y).
    """
    try:
        ba = (a[0] - b[0], a[1] - b[1])
        bc = (c[0] - b[0], c[1] - b[1])

        dot_product = ba[0] * bc[0] + ba[1] * bc[1]
        mag_ba = math.sqrt(ba[0] ** 2 + ba[1] ** 2)
        mag_bc = math.sqrt(bc[0] ** 2 + bc[1] ** 2)

        if mag_ba == 0 or mag_bc == 0:
            return 0.0

        cos_angle = dot_product / (mag_ba * mag_bc)
        cos_angle = max(min(cos_angle, 1.0), -1.0)

        return math.degrees(math.acos(cos_angle))
    except Exception:
        return 0.0
