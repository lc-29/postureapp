from pathlib import Path

folders = [
    "assets/sounds",
    "assets/icons",
    "database",
    "dataset/raw_videos/correct",
    "dataset/raw_videos/incorrect",
    "dataset/processed",
    "models",
    "notebooks",
    "reports/figures",
    "reports/results",
    "src",
    "tests",
]

files = {
    "src/1_rule_based_baseline.py": '''"""
Rule-based baseline:
- Đọc webcam/video bằng OpenCV
- Nhận diện landmark bằng MediaPipe Pose
- Tính một số đặc trưng hình học
- Phân loại tư thế bằng ngưỡng thủ công
"""

def main():
    print("Rule-based baseline module")

if __name__ == "__main__":
    main()
''',

    "src/2_extract_features.py": '''"""
Feature extraction:
- Đọc video trong dataset/raw_videos/correct và incorrect
- Dùng MediaPipe Pose để trích xuất 33 landmark
- Lưu thành dataset/posture_data.csv
"""

def main():
    print("Feature extraction module")

if __name__ == "__main__":
    main()
''',

    "src/3_database_setup.py": '''"""
SQLite setup:
- Tạo database/posture_app.db
- Tạo bảng lưu lịch sử cảnh báo và phiên làm việc
"""

def main():
    print("Database setup module")

if __name__ == "__main__":
    main()
''',

    "src/4_main_desktop_app.py": '''"""
Main desktop app:
- CustomTkinter GUI
- OpenCV webcam
- MediaPipe Pose
- Load ANN model + scaler
- Realtime warning
- SQLite logging/statistics
"""

def main():
    print("Main desktop app module")

if __name__ == "__main__":
    main()
''',

    "src/config.py": '''"""
Cấu hình đường dẫn và tham số chung của hệ thống.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

ASSETS_DIR = BASE_DIR / "assets"
SOUNDS_DIR = ASSETS_DIR / "sounds"
DATABASE_PATH = BASE_DIR / "database" / "posture_app.db"
DATASET_CSV_PATH = BASE_DIR / "dataset" / "posture_data.csv"
MODEL_PATH = BASE_DIR / "models" / "ann_best.keras"
SCALER_PATH = BASE_DIR / "models" / "scaler.pkl"

CAMERA_INDEX = 0
WARNING_SECONDS = 5
WARNING_COOLDOWN_SECONDS = 15
''',

    "src/utils.py": '''"""
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
''',

    "tests/test_imports.py": '''"""
Test nhanh xem các thư viện chính đã cài được chưa.
"""

def test_imports():
    import cv2
    import mediapipe
    import numpy
    import pandas
    import sklearn
    import tensorflow
    import customtkinter
    import PIL

    print("All imports are OK")


if __name__ == "__main__":
    test_imports()
''',

    "README.md": '''# Posture Detection App

Đề tài: Xây dựng ứng dụng phát hiện lỗi tư thế làm việc qua webcam sử dụng Computer Vision.

## Pipeline

OpenCV → MediaPipe Pose → Landmark Extraction → Feature Engineering → Dataset CSV → Rule-based Baseline → ANN Training → Model Evaluation → Tkinter GUI → Realtime Warning → SQLite Logging/Statistics
''',

    ".gitignore": '''.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.vscode/
database/*.db
dataset/processed/
models/*.keras
models/*.h5
models/*.pkl
*.log
.DS_Store
''',

    "run_app.bat": '''@echo off
call .venv\\Scripts\\activate
python src\\4_main_desktop_app.py
pause
''',

    "requirements.txt": '''opencv-python
mediapipe
numpy
pandas
scikit-learn
tensorflow
matplotlib
customtkinter
pillow
playsound==1.2.2
joblib
'''
}

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file_path, content in files.items():
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

print("Đã tạo xong cấu trúc project chuyên nghiệp.")