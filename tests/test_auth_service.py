from __future__ import annotations

import sqlite3
import smtplib
from datetime import datetime, timedelta

import pytest

from src.auth_service import (
    AuthError,
    authenticate_user,
    create_registration_otp,
    create_user,
    ensure_auth_schema,
    format_smtp_error,
    get_smtp_config,
    hash_password,
    register_and_send_otp,
    send_otp_email,
    SMTPConfig,
    verify_password,
    verify_registration_otp,
)


def make_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute(
        """
        CREATE TABLE NguoiDung (
            maNguoiDung INTEGER PRIMARY KEY AUTOINCREMENT,
            tenDangNhap TEXT NOT NULL UNIQUE,
            ngayTao TEXT NOT NULL
        )
        """
    )
    ensure_auth_schema(connection)
    return connection


def test_password_hash_roundtrip() -> None:
    password_hash, salt = hash_password("secret123")

    assert verify_password("secret123", password_hash, salt)
    assert not verify_password("wrong", password_hash, salt)


def test_register_verify_otp_and_login() -> None:
    sent_messages: list[tuple[str, str]] = []
    connection = make_connection()

    register_and_send_otp(
        connection,
        "Student@Example.com",
        "secret123",
        send_email=lambda email, otp: sent_messages.append((email, otp)),
    )

    assert sent_messages
    user_id = verify_registration_otp(
        connection,
        "student@example.com",
        sent_messages[0][1],
    )

    assert user_id == authenticate_user(connection, "student@example.com", "secret123")


def test_login_requires_verified_email() -> None:
    connection = make_connection()
    create_user(connection, "student@example.com", "secret123")

    with pytest.raises(AuthError, match="xac thuc"):
        authenticate_user(connection, "student@example.com", "secret123")


def test_unverified_user_can_request_new_otp_with_same_password() -> None:
    sent_messages: list[tuple[str, str]] = []
    connection = make_connection()
    register_and_send_otp(
        connection,
        "student@example.com",
        "secret123",
        send_email=lambda email, otp: sent_messages.append((email, otp)),
    )
    register_and_send_otp(
        connection,
        "student@example.com",
        "secret123",
        send_email=lambda email, otp: sent_messages.append((email, otp)),
    )

    assert len(sent_messages) == 2
    assert sent_messages[0][1] != sent_messages[1][1]

    with pytest.raises(AuthError, match="dang cho xac thuc"):
        register_and_send_otp(
            connection,
            "student@example.com",
            "wrong-password",
            send_email=lambda email, otp: sent_messages.append((email, otp)),
        )


def test_new_user_is_rolled_back_when_otp_email_fails() -> None:
    connection = make_connection()

    with pytest.raises(AuthError, match="SMTP down"):
        register_and_send_otp(
            connection,
            "student@example.com",
            "secret123",
            send_email=lambda email, otp: (_ for _ in ()).throw(AuthError("SMTP down")),
        )

    assert connection.execute("SELECT COUNT(*) FROM NguoiDung").fetchone()[0] == 0
    assert connection.execute("SELECT COUNT(*) FROM EmailOtp").fetchone()[0] == 0


def test_existing_unverified_user_keeps_previous_otp_when_resend_fails() -> None:
    sent_messages: list[tuple[str, str]] = []
    connection = make_connection()
    register_and_send_otp(
        connection,
        "student@example.com",
        "secret123",
        send_email=lambda email, otp: sent_messages.append((email, otp)),
    )
    before_rows = connection.execute(
        "SELECT otpHash, daSuDung FROM EmailOtp ORDER BY maOtp"
    ).fetchall()

    with pytest.raises(AuthError, match="SMTP down"):
        register_and_send_otp(
            connection,
            "student@example.com",
            "secret123",
            send_email=lambda email, otp: (_ for _ in ()).throw(AuthError("SMTP down")),
        )

    after_rows = connection.execute(
        "SELECT otpHash, daSuDung FROM EmailOtp ORDER BY maOtp"
    ).fetchall()
    assert after_rows == before_rows


def test_invalid_or_expired_otp_is_rejected() -> None:
    connection = make_connection()
    user_id = create_user(connection, "student@example.com", "secret123")
    create_registration_otp(connection, user_id, "student@example.com", otp="123456")

    with pytest.raises(AuthError, match="khong dung"):
        verify_registration_otp(connection, "student@example.com", "000000")

    expired = (datetime.now() - timedelta(minutes=1)).isoformat(timespec="seconds")
    connection.execute("UPDATE EmailOtp SET hetHanLuc = ?", (expired,))
    connection.commit()

    with pytest.raises(AuthError, match="het han"):
        verify_registration_otp(connection, "student@example.com", "123456")


def test_smtp_config_reads_local_xml_style_config(tmp_path, monkeypatch) -> None:
    local_config = tmp_path / "email_otp.local.config"
    local_config.write_text(
        "\n".join(
            [
                '<add key="fromEmail" value="sender@example.com" />',
                '<add key="password" value="app password" />',
                '<add key="smtpHost" value="smtp.example.com" />',
                '<add key="smtpPort" value="2525" />',
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("src.auth_service.LOCAL_EMAIL_CONFIG", local_config)
    monkeypatch.delenv("POSTURE_APP_FROM_EMAIL", raising=False)
    monkeypatch.delenv("POSTURE_APP_EMAIL_PASSWORD", raising=False)

    config = get_smtp_config()

    assert config.from_email == "sender@example.com"
    assert config.password == "app password"
    assert config.host == "smtp.example.com"
    assert config.port == 2525


def test_gmail_app_password_spaces_are_removed(tmp_path, monkeypatch) -> None:
    local_config = tmp_path / "email_otp.local.config"
    local_config.write_text(
        "\n".join(
            [
                '<add key="fromEmail" value="sender@gmail.com" />',
                '<add key="password" value="abcd efgh ijkl mnop" />',
                '<add key="smtpHost" value="smtp.gmail.com" />',
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr("src.auth_service.LOCAL_EMAIL_CONFIG", local_config)
    monkeypatch.delenv("POSTURE_APP_FROM_EMAIL", raising=False)
    monkeypatch.delenv("POSTURE_APP_EMAIL_PASSWORD", raising=False)
    monkeypatch.delenv("POSTURE_APP_SMTP_HOST", raising=False)

    config = get_smtp_config()

    assert config.password == "abcdefghijklmnop"


def test_smtp_authentication_error_is_mapped_to_auth_error(monkeypatch) -> None:
    class FakeSMTP:
        def __init__(self, *_args, **_kwargs) -> None:
            pass

        def __enter__(self):
            return self

        def __exit__(self, *_args) -> None:
            return None

        def starttls(self) -> None:
            return None

        def login(self, *_args) -> None:
            raise smtplib.SMTPAuthenticationError(535, b"BadCredentials")

        def send_message(self, _message) -> None:
            raise AssertionError("send_message should not run after login failure")

    monkeypatch.setattr("src.auth_service.smtplib.SMTP", FakeSMTP)

    with pytest.raises(AuthError, match="Gmail App Password"):
        send_otp_email(
            "student@example.com",
            "123456",
            smtp_config=SMTPConfig(
                host="smtp.gmail.com",
                port=587,
                from_email="sender@gmail.com",
                password="wrongpassword",
            ),
        )


def test_format_smtp_error_for_connectivity() -> None:
    message = format_smtp_error(OSError("network unreachable"))

    assert "SMTP server" in message
