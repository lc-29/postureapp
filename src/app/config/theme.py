"""Theme palette and font helpers for the CustomTkinter UI."""

from __future__ import annotations

from typing import Any

import customtkinter as ctk


APP_FONT_FAMILY = "Segoe UI"

THEMES = {
    "light": {
        "app_bg": "#f6f8fb",
        "surface": "#ffffff",
        "surface_muted": "#eef2f7",
        "surface_subtle": "#f8fafc",
        "border": "#d7dde8",
        "border_soft": "#e5eaf2",
        "text": "#162033",
        "muted": "#5b677a",
        "muted_light": "#7b8798",
        "success": "#15803d",
        "success_bg": "#dcfce7",
        "danger": "#dc2626",
        "danger_bg": "#fee2e2",
        "warning": "#b45309",
        "warning_bg": "#fef3c7",
        "info": "#2563eb",
        "info_bg": "#dbeafe",
        "neutral": "#64748b",
        "neutral_bg": "#e2e8f0",
    },
    "dark": {
        "app_bg": "#0f172a",
        "surface": "#111827",
        "surface_muted": "#1f2937",
        "surface_subtle": "#172033",
        "border": "#334155",
        "border_soft": "#243244",
        "text": "#f8fafc",
        "muted": "#cbd5e1",
        "muted_light": "#94a3b8",
        "success": "#22c55e",
        "success_bg": "#052e16",
        "danger": "#f87171",
        "danger_bg": "#450a0a",
        "warning": "#fbbf24",
        "warning_bg": "#422006",
        "info": "#60a5fa",
        "info_bg": "#172554",
        "neutral": "#94a3b8",
        "neutral_bg": "#1e293b",
    },
}

THEME = dict(THEMES["light"])


def app_font(size: int, weight: str | None = None) -> ctk.CTkFont:
    """Create a CTk font that renders Vietnamese well on Windows."""
    kwargs: dict[str, Any] = {"family": APP_FONT_FAMILY, "size": size}
    if weight is not None:
        kwargs["weight"] = weight
    return ctk.CTkFont(**kwargs)

