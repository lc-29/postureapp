"""
Khoi tao lai co so du lieu SQLite cho ung dung phat hien loi tu the lam viec.

File nay dung trong giai doan phat trien va demo do an:
- Xoa database cu neu ton tai.
- Tao lai database/posture_app.db voi schema tieng Viet.
- Them du lieu mac dinh cho nguoi dung, cau hinh ung dung va model ANN.
- Chay smoke test de kiem tra bang, index va so dong du lieu mac dinh.
"""

from datetime import datetime
from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[1]
DB_RELATIVE_PATH = Path("database") / "posture_app.db"
DATABASE_PATH = BASE_DIR / DB_RELATIVE_PATH

REQUIRED_TABLES = [
    "CaiDat",
    "NguoiDung",
    "NhatKyTuThe",
    "PhienLamViec",
    "ThongKeNgay",
    "ThongTinModel",
]

ROW_COUNT_TABLES = [
    "NguoiDung",
    "CaiDat",
    "PhienLamViec",
    "NhatKyTuThe",
    "ThongKeNgay",
    "ThongTinModel",
]

REQUIRED_INDEXES = [
    "idx_caidat_maNguoiDung",
    "idx_phien_maNguoiDung",
    "idx_phien_thoiGianBatDau",
    "idx_nhatky_maPhien",
    "idx_nhatky_thoiDiem",
    "idx_nhatky_trangThai",
    "idx_thongke_ngay",
]


def get_db_path() -> Path:
    """
    Trả về đường dẫn database SQLite theo thư mục gốc project.
    """
    return DATABASE_PATH


def create_connection(db_path: Path) -> sqlite3.Connection:
    """
    Tạo kết nối SQLite và bật ràng buộc khóa ngoại.
    """
    connection = sqlite3.connect(db_path)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def reset_database_file(db_path: Path) -> None:
    """
    Xoa file database cu neu ton tai de tao lai CSDL moi.
    Chi dung trong giai doan phat trien.
    """
    if db_path.exists():
        print(f"Da tim thay CSDL cu, dang xoa: {db_path}")
        db_path.unlink()
        print("Da xoa CSDL cu.")
    else:
        print("Chua co CSDL cu, se tao moi.")


def create_tables(connection: sqlite3.Connection) -> None:
    """
    Tạo toàn bộ bảng cần thiết cho ứng dụng.
    """
    cursor = connection.cursor()

    # Bảng lưu người dùng mặc định của ứng dụng.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS NguoiDung (
            maNguoiDung INTEGER PRIMARY KEY AUTOINCREMENT,
            tenDangNhap TEXT NOT NULL UNIQUE,
            ngayTao TEXT NOT NULL
        )
        """
    )

    # Bảng lưu các tham số cấu hình đang được app sử dụng.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS CaiDat (
            maCaiDat INTEGER PRIMARY KEY AUTOINCREMENT,
            maNguoiDung INTEGER NOT NULL,
            thoiGianCanhBao INTEGER NOT NULL DEFAULT 5,
            thoiGianChoCanhBao INTEGER NOT NULL DEFAULT 15,
            batAmThanh INTEGER NOT NULL DEFAULT 1,
            duongDanAmThanh TEXT NOT NULL DEFAULT 'assets/sounds/alarm.wav',
            nguonCamera TEXT NOT NULL DEFAULT '0',
            duongDanModel TEXT NOT NULL DEFAULT 'models/ann_best.keras',
            duongDanScaler TEXT NOT NULL DEFAULT 'models/scaler.pkl',
            ngayCapNhat TEXT NOT NULL,
            FOREIGN KEY (maNguoiDung)
                REFERENCES NguoiDung(maNguoiDung)
                ON DELETE CASCADE
        )
        """
    )

    # Bảng lưu từng phiên chạy camera hoặc video của người dùng.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS PhienLamViec (
            maPhien INTEGER PRIMARY KEY AUTOINCREMENT,
            maNguoiDung INTEGER NOT NULL,
            thoiGianBatDau TEXT NOT NULL,
            thoiGianKetThuc TEXT,
            loaiNguon TEXT,
            giaTriNguon TEXT,
            tongSoFrame INTEGER DEFAULT 0,
            soFrameDung INTEGER DEFAULT 0,
            soFrameSai INTEGER DEFAULT 0,
            soFrameKhongCoNguoi INTEGER DEFAULT 0,
            tongThoiGianDung REAL DEFAULT 0,
            tongThoiGianSai REAL DEFAULT 0,
            soLanCanhBao INTEGER DEFAULT 0,
            doTinCayTrungBinh REAL DEFAULT 0,
            ghiChu TEXT,
            ngayTao TEXT NOT NULL,
            FOREIGN KEY (maNguoiDung)
                REFERENCES NguoiDung(maNguoiDung)
                ON DELETE CASCADE
        )
        """
    )

    # Bảng lưu lịch sử trạng thái, dự đoán và cảnh báo tư thế.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS NhatKyTuThe (
            maNhatKy INTEGER PRIMARY KEY AUTOINCREMENT,
            maPhien INTEGER,
            thoiDiem TEXT NOT NULL,
            trangThai TEXT NOT NULL,
            nhanDuDoan INTEGER,
            xacSuatSai REAL,
            doTinCay REAL,
            daCanhBao INTEGER DEFAULT 0,
            loaiCanhBao TEXT,
            chiSoFrame INTEGER,
            fps REAL,
            ghiChu TEXT,
            FOREIGN KEY (maPhien)
                REFERENCES PhienLamViec(maPhien)
                ON DELETE SET NULL
        )
        """
    )

    # Bảng thống kê nhanh theo ngày để phục vụ màn hình báo cáo.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ThongKeNgay (
            maThongKe INTEGER PRIMARY KEY AUTOINCREMENT,
            ngay TEXT NOT NULL UNIQUE,
            tongSoPhien INTEGER DEFAULT 0,
            tongThoiGianLamViec REAL DEFAULT 0,
            tongThoiGianDung REAL DEFAULT 0,
            tongThoiGianSai REAL DEFAULT 0,
            tongSoCanhBao INTEGER DEFAULT 0,
            tiLeDung REAL DEFAULT 0,
            tiLeSai REAL DEFAULT 0,
            ngayCapNhat TEXT NOT NULL
        )
        """
    )

    # Bảng lưu thông tin model ANN đang được ứng dụng sử dụng.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS ThongTinModel (
            maModel INTEGER PRIMARY KEY AUTOINCREMENT,
            tenModel TEXT NOT NULL,
            duongDanModel TEXT NOT NULL,
            duongDanScaler TEXT NOT NULL,
            soDacTrungDauVao INTEGER NOT NULL DEFAULT 99,
            kieuDauRa TEXT NOT NULL DEFAULT 'binary_sigmoid',
            accuracy REAL,
            precisionScore REAL,
            recallScore REAL,
            f1Score REAL,
            soMauTrain INTEGER,
            soMauTest INTEGER,
            ngayTao TEXT NOT NULL,
            ghiChu TEXT
        )
        """
    )


def create_indexes(connection: sqlite3.Connection) -> None:
    """
    Tạo các index giúp truy vấn cấu hình, phiên làm việc và nhật ký nhanh hơn.
    """
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_caidat_maNguoiDung
        ON CaiDat(maNguoiDung)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phien_maNguoiDung
        ON PhienLamViec(maNguoiDung)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_phien_thoiGianBatDau
        ON PhienLamViec(thoiGianBatDau)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_nhatky_maPhien
        ON NhatKyTuThe(maPhien)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_nhatky_thoiDiem
        ON NhatKyTuThe(thoiDiem)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_nhatky_trangThai
        ON NhatKyTuThe(trangThai)
        """
    )
    cursor.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_thongke_ngay
        ON ThongKeNgay(ngay)
        """
    )


def insert_default_data(connection: sqlite3.Connection) -> None:
    """
    Thêm người dùng Admin, cấu hình mặc định và thông tin model mặc định.
    """
    cursor = connection.cursor()
    now = datetime.now().isoformat(timespec="seconds")

    # Dùng INSERT OR IGNORE để tránh lỗi nếu hàm được gọi khi không reset CSDL.
    cursor.execute(
        """
        INSERT OR IGNORE INTO NguoiDung (tenDangNhap, ngayTao)
        VALUES (?, ?)
        """,
        ("Admin", now),
    )

    cursor.execute(
        """
        SELECT maNguoiDung
        FROM NguoiDung
        WHERE tenDangNhap = ?
        """,
        ("Admin",),
    )
    admin_row = cursor.fetchone()
    if admin_row is None:
        raise RuntimeError("Khong tim thay nguoi dung Admin sau khi insert.")

    admin_id = admin_row[0]

    # Mỗi người dùng chỉ cần một dòng cấu hình mặc định trong giai đoạn demo.
    cursor.execute(
        """
        SELECT COUNT(*)
        FROM CaiDat
        WHERE maNguoiDung = ?
        """,
        (admin_id,),
    )
    setting_count = cursor.fetchone()[0]

    if setting_count == 0:
        cursor.execute(
            """
            INSERT INTO CaiDat (
                maNguoiDung,
                thoiGianCanhBao,
                thoiGianChoCanhBao,
                batAmThanh,
                duongDanAmThanh,
                nguonCamera,
                duongDanModel,
                duongDanScaler,
                ngayCapNhat
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                admin_id,
                5,
                15,
                1,
                "assets/sounds/alarm.wav",
                "0",
                "models/ann_best.keras",
                "models/scaler.pkl",
                now,
            ),
        )

    # Chỉ thêm thông tin model nếu bảng đang rỗng để tránh trùng dữ liệu.
    cursor.execute("SELECT COUNT(*) FROM ThongTinModel")
    model_count = cursor.fetchone()[0]

    if model_count == 0:
        cursor.execute(
            """
            INSERT INTO ThongTinModel (
                tenModel,
                duongDanModel,
                duongDanScaler,
                soDacTrungDauVao,
                kieuDauRa,
                accuracy,
                precisionScore,
                recallScore,
                f1Score,
                soMauTrain,
                soMauTest,
                ngayTao,
                ghiChu
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                "ANN Landmark Posture Classifier",
                "models/ann_best.keras",
                "models/scaler.pkl",
                99,
                "binary_sigmoid",
                0.9963,
                0.9979,
                0.9958,
                0.9969,
                3763,
                807,
                now,
                (
                    "Model ANN train tren 99 dac trung landmark MediaPipe Pose, "
                    "label 0 la dung tu the, label 1 la sai tu the"
                ),
            ),
        )


def init_database(reset: bool = True) -> Path:
    """
    Khởi tạo CSDL SQLite, có thể reset file cũ trước khi tạo lại.
    """
    db_path = get_db_path()
    connection = None

    try:
        db_path.parent.mkdir(parents=True, exist_ok=True)

        if reset:
            reset_database_file(db_path)

        print(f"Dang tao CSDL moi tai: {db_path}")
        connection = create_connection(db_path)

        print("Dang tao bang...")
        create_tables(connection)

        print("Dang tao index...")
        create_indexes(connection)

        print("Dang them du lieu mac dinh...")
        insert_default_data(connection)

        connection.commit()
        print("Khoi tao CSDL thanh cong.")
        return db_path

    except sqlite3.Error as error:
        if connection is not None:
            connection.rollback()
        print(f"Loi SQLite khi khoi tao CSDL: {error}")
        raise

    except Exception as error:
        if connection is not None:
            connection.rollback()
        print(f"Loi khi khoi tao CSDL: {error}")
        raise

    finally:
        if connection is not None:
            connection.close()


def smoke_test(db_path: Path) -> None:
    """
    Kiểm tra nhanh bảng, index và số dòng dữ liệu mặc định sau khi khởi tạo.
    """
    connection = None

    try:
        connection = create_connection(db_path)
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
                AND name NOT LIKE 'sqlite_%'
            ORDER BY name
            """
        )
        existing_tables = [row[0] for row in cursor.fetchall()]

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'index'
                AND name NOT LIKE 'sqlite_autoindex%'
            ORDER BY name
            """
        )
        existing_indexes = [row[0] for row in cursor.fetchall()]

        missing_tables = [
            table_name
            for table_name in REQUIRED_TABLES
            if table_name not in existing_tables
        ]
        missing_indexes = [
            index_name
            for index_name in REQUIRED_INDEXES
            if index_name not in existing_indexes
        ]

        print()
        print("========== KIEM TRA CSDL ==========")
        print("Bang hien co:")
        for table_name in REQUIRED_TABLES:
            if table_name in existing_tables:
                print(f"- {table_name}")

        print()
        print("Index hien co:")
        for index_name in REQUIRED_INDEXES:
            if index_name in existing_indexes:
                print(f"- {index_name}")

        print()
        print("So dong:")
        row_counts = {}
        for table_name in ROW_COUNT_TABLES:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_counts[table_name] = cursor.fetchone()[0]
            print(f"{table_name}: {row_counts[table_name]}")

        expected_counts = {
            "NguoiDung": 1,
            "CaiDat": 1,
            "PhienLamViec": 0,
            "NhatKyTuThe": 0,
            "ThongKeNgay": 0,
            "ThongTinModel": 1,
        }
        wrong_counts = {
            table_name: row_counts[table_name]
            for table_name, expected_count in expected_counts.items()
            if row_counts[table_name] != expected_count
        }

        cursor.execute("PRAGMA foreign_keys")
        foreign_keys_enabled = cursor.fetchone()[0] == 1

        if missing_tables:
            raise RuntimeError(f"Thieu bang: {', '.join(missing_tables)}")
        if missing_indexes:
            raise RuntimeError(f"Thieu index: {', '.join(missing_indexes)}")
        if wrong_counts:
            details = ", ".join(
                f"{table_name}={row_count}"
                for table_name, row_count in wrong_counts.items()
            )
            raise RuntimeError(f"So dong khong dung: {details}")
        if not foreign_keys_enabled:
            raise RuntimeError("PRAGMA foreign_keys chua duoc bat.")

        print()
        print("Smoke test: OK")

    except sqlite3.Error as error:
        print(f"Loi SQLite khi kiem tra CSDL: {error}")
        raise

    except Exception as error:
        print(f"Loi khi kiem tra CSDL: {error}")
        raise

    finally:
        if connection is not None:
            connection.close()


def main() -> None:
    """
    Điểm bắt đầu khi chạy trực tiếp file này.
    """
    print("========== KHOI TAO CSDL SQLITE ==========")

    try:
        db_path = init_database(reset=True)
        print(f"Duong dan CSDL: {db_path}")
        smoke_test(db_path)

    except Exception:
        print("Khoi tao CSDL that bai.")
        raise SystemExit(1)

    finally:
        print("===================================")


if __name__ == "__main__":
    main()
