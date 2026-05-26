"""Cac ham tien ich dung chung trong project."""

import math


def calculate_angle(a, b, c):
    """
    Tinh goc ABC tu 3 diem a, b, c.

    Moi diem co dang `(x, y)`. Neu input khong hop le hoac mot vector co do dai
    bang 0, ham tra ve 0.0 de caller khong bi crash trong luong realtime.
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
