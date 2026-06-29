"""Authentication, registration OTP, and SMTP helpers for the desktop app."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
import re
import secrets
import smtplib
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta
from email.message import EmailMessage
from pathlib import Path
from typing import Callable


BASE_DIR = Path(__file__).resolve().parents[1]
LOCAL_EMAIL_CONFIG = BASE_DIR / "config" / "email_otp.local.config"
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PBKDF2_ITERATIONS = 260_000
OTP_TTL_MINUTES = 5
MAX_OTP_ATTEMPTS = 5


class AuthError(ValueError):
    """Raised when authentication or OTP validation fails."""


@dataclass(frozen=True)
class SMTPConfig:
    host: str
    port: int
    from_email: str
    password: str
    use_tls: bool = True


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def normalize_email(email: str) -> str:
    normalized = email.strip().lower()
    if not EMAIL_PATTERN.match(normalized):
        raise AuthError("Email khong hop le.")
    return normalized


def validate_password(password: str) -> None:
    if len(password) < 6:
        raise AuthError("Mat khau phai co it nhat 6 ky tu.")


def make_salt(num_bytes: int = 16) -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(num_bytes)).decode("ascii")


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    resolved_salt = salt or make_salt()
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        resolved_salt.encode("ascii"),
        PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(digest).decode("ascii"), resolved_salt


def verify_password(password: str, password_hash: str, salt: str) -> bool:
    candidate_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(candidate_hash, password_hash)


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_otp(email: str, otp: str, salt: str | None = None) -> tuple[str, str]:
    resolved_salt = salt or make_salt()
    digest = hashlib.sha256(
        f"{normalize_email(email)}:{otp}:{resolved_salt}".encode("utf-8")
    ).hexdigest()
    return digest, resolved_salt


def verify_otp_hash(email: str, otp: str, otp_hash: str, salt: str) -> bool:
    candidate_hash, _ = hash_otp(email, otp, salt)
    return hmac.compare_digest(candidate_hash, otp_hash)


def _load_local_config(path: Path | None = None) -> dict[str, str]:
    config_path = path or LOCAL_EMAIL_CONFIG
    if not config_path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in config_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        xml_match = re.search(r'key="([^"]+)"\s+value="([^"]*)"', line)
        if xml_match:
            values[xml_match.group(1)] = xml_match.group(2)
            continue
        if "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"')
    return values


def get_smtp_config() -> SMTPConfig:
    local_config = _load_local_config()

    host = (
        os.environ.get("POSTURE_APP_SMTP_HOST")
        or local_config.get("smtpHost")
        or "smtp.gmail.com"
    )
    port = int(
        os.environ.get("POSTURE_APP_SMTP_PORT")
        or local_config.get("smtpPort")
        or "587"
    )
    from_email = (
        os.environ.get("POSTURE_APP_FROM_EMAIL")
        or local_config.get("fromEmail")
        or ""
    ).strip()
    password = (
        os.environ.get("POSTURE_APP_EMAIL_PASSWORD")
        or local_config.get("password")
        or ""
    ).strip()
    use_tls_text = (
        os.environ.get("POSTURE_APP_SMTP_TLS")
        or local_config.get("useTls")
        or "true"
    ).strip().lower()

    if not from_email or not password:
        raise AuthError(
            "Chua cau hinh email gui OTP. Hay thiet lap POSTURE_APP_FROM_EMAIL "
            "va POSTURE_APP_EMAIL_PASSWORD hoac tao config/email_otp.local.config."
        )

    if "gmail.com" in host.lower():
        password = password.replace(" ", "")

    return SMTPConfig(
        host=host,
        port=port,
        from_email=from_email,
        password=password,
        use_tls=use_tls_text not in {"0", "false", "no"},
    )


def format_smtp_error(error: Exception) -> str:
    """Chuyen loi smtplib thanh thong bao ngan gon cho GUI."""
    if isinstance(error, smtplib.SMTPAuthenticationError):
        return (
            "Khong dang nhap duoc SMTP Gmail. Hay kiem tra email gui OTP, "
            "bat 2-Step Verification va tao lai Gmail App Password."
        )
    if isinstance(error, smtplib.SMTPConnectError):
        return "Khong ket noi duoc SMTP server. Hay kiem tra mang va smtpHost/smtpPort."
    if isinstance(error, smtplib.SMTPException):
        return f"Khong gui duoc email OTP qua SMTP: {error}"
    if isinstance(error, OSError):
        return f"Khong ket noi duoc SMTP server: {error}"
    return f"Khong gui duoc email OTP: {error}"


def send_otp_email(email: str, otp: str, smtp_config: SMTPConfig | None = None) -> None:
    config = smtp_config or get_smtp_config()
    recipient = normalize_email(email)

    message = EmailMessage()
    message["Subject"] = "Ma OTP xac thuc tai khoan Posture Detection App"
    message["From"] = config.from_email
    message["To"] = recipient
    message.set_content(
        "\n".join(
            [
                "Xin chao,",
                "",
                f"Ma OTP xac thuc tai khoan cua ban la: {otp}",
                f"Ma co hieu luc trong {OTP_TTL_MINUTES} phut.",
                "",
                "Neu ban khong yeu cau dang ky, vui long bo qua email nay.",
            ]
        )
    )

    try:
        with smtplib.SMTP(config.host, config.port, timeout=20) as server:
            if config.use_tls:
                server.starttls()
            server.login(config.from_email, config.password)
            server.send_message(message)
    except Exception as exc:
        raise AuthError(format_smtp_error(exc)) from exc


def ensure_auth_schema(connection: sqlite3.Connection) -> None:
    rows = connection.execute("PRAGMA table_info(NguoiDung)").fetchall()
    columns = {str(row[1]) for row in rows}
    migrations = {
        "email": "ALTER TABLE NguoiDung ADD COLUMN email TEXT",
        "matKhauHash": "ALTER TABLE NguoiDung ADD COLUMN matKhauHash TEXT",
        "matKhauSalt": "ALTER TABLE NguoiDung ADD COLUMN matKhauSalt TEXT",
        "emailDaXacThuc": (
            "ALTER TABLE NguoiDung ADD COLUMN emailDaXacThuc INTEGER NOT NULL DEFAULT 0"
        ),
        "ngayCapNhat": "ALTER TABLE NguoiDung ADD COLUMN ngayCapNhat TEXT",
        "lanDangNhapCuoi": "ALTER TABLE NguoiDung ADD COLUMN lanDangNhapCuoi TEXT",
    }
    for column_name, sql in migrations.items():
        if column_name not in columns:
            connection.execute(sql)

    connection.execute(
        """
        CREATE UNIQUE INDEX IF NOT EXISTS idx_nguoidung_email
        ON NguoiDung(email)
        WHERE email IS NOT NULL
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS EmailOtp (
            maOtp INTEGER PRIMARY KEY AUTOINCREMENT,
            maNguoiDung INTEGER NOT NULL,
            email TEXT NOT NULL,
            otpHash TEXT NOT NULL,
            otpSalt TEXT NOT NULL,
            mucDich TEXT NOT NULL DEFAULT 'register',
            hetHanLuc TEXT NOT NULL,
            daSuDung INTEGER NOT NULL DEFAULT 0,
            soLanThu INTEGER NOT NULL DEFAULT 0,
            ngayTao TEXT NOT NULL,
            FOREIGN KEY (maNguoiDung)
                REFERENCES NguoiDung(maNguoiDung)
                ON DELETE CASCADE
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_emailotp_user_purpose
        ON EmailOtp(maNguoiDung, mucDich, daSuDung, hetHanLuc)
        """
    )
    connection.commit()


def create_user(connection: sqlite3.Connection, email: str, password: str) -> int:
    ensure_auth_schema(connection)
    normalized_email = normalize_email(email)
    validate_password(password)

    existing = connection.execute(
        """
        SELECT maNguoiDung
        FROM NguoiDung
        WHERE lower(email) = ?
        """,
        (normalized_email,),
    ).fetchone()
    if existing is not None:
        raise AuthError("Email nay da duoc dang ky.")

    password_hash, salt = hash_password(password)
    now = now_iso()
    username = normalized_email
    cursor = connection.execute(
        """
        INSERT INTO NguoiDung (
            tenDangNhap,
            email,
            matKhauHash,
            matKhauSalt,
            emailDaXacThuc,
            ngayTao,
            ngayCapNhat
        )
        VALUES (?, ?, ?, ?, 0, ?, ?)
        """,
        (username, normalized_email, password_hash, salt, now, now),
    )
    connection.commit()
    return int(cursor.lastrowid)


def create_registration_otp(
    connection: sqlite3.Connection,
    user_id: int,
    email: str,
    otp: str | None = None,
    commit: bool = True,
) -> str:
    ensure_auth_schema(connection)
    normalized_email = normalize_email(email)
    otp_value = otp or generate_otp()
    otp_hash, otp_salt = hash_otp(normalized_email, otp_value)
    now = datetime.now()
    expires_at = (now + timedelta(minutes=OTP_TTL_MINUTES)).isoformat(timespec="seconds")

    connection.execute(
        """
        UPDATE EmailOtp
        SET daSuDung = 1
        WHERE maNguoiDung = ?
            AND mucDich = 'register'
            AND daSuDung = 0
        """,
        (user_id,),
    )
    connection.execute(
        """
        INSERT INTO EmailOtp (
            maNguoiDung,
            email,
            otpHash,
            otpSalt,
            mucDich,
            hetHanLuc,
            daSuDung,
            soLanThu,
            ngayTao
        )
        VALUES (?, ?, ?, ?, 'register', ?, 0, 0, ?)
        """,
        (user_id, normalized_email, otp_hash, otp_salt, expires_at, now.isoformat(timespec="seconds")),
    )
    if commit:
        connection.commit()
    return otp_value


def verify_registration_otp(
    connection: sqlite3.Connection,
    email: str,
    otp: str,
) -> int:
    ensure_auth_schema(connection)
    normalized_email = normalize_email(email)
    row = connection.execute(
        """
        SELECT
            o.maOtp,
            o.maNguoiDung,
            o.otpHash,
            o.otpSalt,
            o.hetHanLuc,
            o.soLanThu
        FROM EmailOtp o
        JOIN NguoiDung u ON u.maNguoiDung = o.maNguoiDung
        WHERE lower(o.email) = ?
            AND o.mucDich = 'register'
            AND o.daSuDung = 0
            AND u.emailDaXacThuc = 0
        ORDER BY o.maOtp DESC
        LIMIT 1
        """,
        (normalized_email,),
    ).fetchone()
    if row is None:
        raise AuthError("Khong tim thay OTP dang cho xac thuc.")

    otp_id, user_id, otp_hash_value, otp_salt, expires_at, attempts = row
    if int(attempts) >= MAX_OTP_ATTEMPTS:
        raise AuthError("OTP da vuot qua so lan thu cho phep. Hay gui lai OTP.")
    if datetime.now() > parse_datetime(str(expires_at)):
        raise AuthError("OTP da het han. Hay gui lai OTP.")

    connection.execute(
        "UPDATE EmailOtp SET soLanThu = soLanThu + 1 WHERE maOtp = ?",
        (otp_id,),
    )
    if not verify_otp_hash(normalized_email, otp.strip(), str(otp_hash_value), str(otp_salt)):
        connection.commit()
        raise AuthError("OTP khong dung.")

    now = now_iso()
    connection.execute(
        """
        UPDATE EmailOtp
        SET daSuDung = 1
        WHERE maOtp = ?
        """,
        (otp_id,),
    )
    connection.execute(
        """
        UPDATE NguoiDung
        SET emailDaXacThuc = 1,
            ngayCapNhat = ?
        WHERE maNguoiDung = ?
        """,
        (now, user_id),
    )
    connection.commit()
    return int(user_id)


def authenticate_user(connection: sqlite3.Connection, email: str, password: str) -> int:
    ensure_auth_schema(connection)
    normalized_email = normalize_email(email)
    row = connection.execute(
        """
        SELECT maNguoiDung, matKhauHash, matKhauSalt, emailDaXacThuc
        FROM NguoiDung
        WHERE lower(email) = ?
        """,
        (normalized_email,),
    ).fetchone()
    if row is None:
        raise AuthError("Email hoac mat khau khong dung.")

    user_id, password_hash, salt, verified = row
    if not password_hash or not salt:
        raise AuthError("Tai khoan chua co mat khau dang nhap.")
    if int(verified) != 1:
        raise AuthError("Tai khoan chua xac thuc email.")
    if not verify_password(password, str(password_hash), str(salt)):
        raise AuthError("Email hoac mat khau khong dung.")

    connection.execute(
        "UPDATE NguoiDung SET lanDangNhapCuoi = ?, ngayCapNhat = ? WHERE maNguoiDung = ?",
        (now_iso(), now_iso(), user_id),
    )
    connection.commit()
    return int(user_id)


def register_and_send_otp(
    connection: sqlite3.Connection,
    email: str,
    password: str,
    send_email: Callable[[str, str], None] = send_otp_email,
) -> int:
    ensure_auth_schema(connection)
    normalized_email = normalize_email(email)
    validate_password(password)
    row = connection.execute(
        """
        SELECT maNguoiDung, matKhauHash, matKhauSalt, emailDaXacThuc
        FROM NguoiDung
        WHERE lower(email) = ?
        """,
        (normalized_email,),
    ).fetchone()
    created_new_user = False
    if row is None:
        user_id = create_user(connection, normalized_email, password)
        created_new_user = True
    else:
        user_id, password_hash, salt, verified = row
        if int(verified) == 1:
            raise AuthError("Email nay da duoc dang ky va xac thuc.")
        if not password_hash or not salt or not verify_password(password, str(password_hash), str(salt)):
            raise AuthError("Email nay dang cho xac thuc. Hay nhap dung mat khau da dang ky.")
        user_id = int(user_id)

    otp = create_registration_otp(connection, user_id, email, commit=False)
    try:
        send_email(normalize_email(email), otp)
    except Exception:
        connection.rollback()
        if created_new_user:
            connection.execute("DELETE FROM NguoiDung WHERE maNguoiDung = ?", (user_id,))
            connection.commit()
        raise
    connection.commit()
    return user_id
