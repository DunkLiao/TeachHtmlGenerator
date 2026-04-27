from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_THEME_KEY = "classic_rose"
CONFIG_PATH = Path(__file__).resolve().with_name("site_config.txt")


@dataclass(frozen=True)
class ColorTheme:
    name: str
    variables: dict[str, str]


CLASSIC_ROSE_VARIABLES = {
    "--brand": "#9a0036",
    "--brand-deep": "#7f002d",
    "--accent": "#941c61",
    "--accent-soft": "#eebac0",
    "--button-start": "#d99a22",
    "--button-end": "#eb8a1f",
    "--button-hover-start": "#efad31",
    "--button-hover-end": "#f39a33",
    "--button-text": "#291600",
    "--gold-deep": "#b77710",
    "--text": "#333333",
    "--text-strong": "#262626",
    "--body-text": "#3f3b3c",
    "--article-heading": "#23181d",
    "--article-summary": "#454545",
    "--toc-link": "#5a3441",
    "--muted": "#6e6e6e",
    "--muted-warm": "#8d7a7f",
    "--deleted-text": "#8c7380",
    "--emphasis-text": "#5d4751",
    "--line": "#eadde0",
    "--line-soft": "#f0e7ea",
    "--line-strong": "#dfabb5",
    "--surface": "#ffffff",
    "--surface-soft": "#f5f5f5",
    "--surface-tint": "#f7edf0",
    "--surface-accent": "#fbebee",
    "--surface-note": "#fff9ef",
    "--surface-code": "#fff7f9",
    "--surface-code-inline": "#fff5f7",
    "--surface-table-head": "#fff4f7",
    "--surface-table-even": "#fffafb",
    "--surface-toc-start": "#fff7f8",
    "--card-border": "#f0d7dd",
    "--icon-border": "#f0cbd1",
    "--toc-border": "#eed5db",
    "--article-border": "#ecd7dd",
    "--code-border": "#ecd3d9",
    "--note-border": "#f0d7ad",
    "--panel-border": "#ece7e8",
    "--blockquote-border": "#d67a91",
    "--blockquote-bg": "#fff5f7",
    "--blockquote-text": "#6a4450",
    "--table-heading": "#5f243d",
    "--code-text": "#7f002d",
    "--pre-code-text": "#6f1138",
    "--note-icon-bg": "#fff2d8",
    "--note-icon-border": "#edcd95",
    "--note-heading": "#8a5400",
    "--note-text": "#4d3b1d",
    "--eyebrow": "#ffe4c0",
    "--footer-bg": "#333333",
    "--footer-text": "rgba(255, 255, 255, 0.84)",
    "--footer-label": "#ffd690",
    "--footer-divider": "rgba(255, 255, 255, 0.18)",
    "--hero-start": "rgba(154, 0, 54, 0.98)",
    "--hero-end": "rgba(148, 28, 97, 0.91)",
    "--hero-glow": "rgba(238, 186, 192, 0.38)",
    "--hero-sheen": "rgba(255, 255, 255, 0.12)",
    "--hero-text": "rgba(255, 255, 255, 0.88)",
    "--hero-panel": "rgba(255, 255, 255, 0.13)",
    "--hero-panel-border": "rgba(255, 255, 255, 0.3)",
    "--secondary-bg": "rgba(255, 255, 255, 0.12)",
    "--secondary-hover-bg": "rgba(255, 255, 255, 0.22)",
    "--secondary-border": "rgba(255, 255, 255, 0.42)",
    "--article-panel-bg": "rgba(255, 255, 255, 0.95)",
    "--shadow": "0 16px 36px rgba(86, 35, 50, 0.11)",
    "--shadow-soft": "0 8px 22px rgba(80, 38, 50, 0.07)",
    "--button-shadow": "0 10px 22px rgba(91, 47, 0, 0.2)",
    "--button-shadow-hover": "0 14px 28px rgba(91, 47, 0, 0.24)",
    "--mock-shadow": "0 18px 38px rgba(66, 0, 28, 0.2)",
    "--footer-shadow": "0 -10px 24px rgba(0, 0, 0, 0.12)",
    "--focus-ring": "rgba(154, 0, 54, 0.12)",
    "--divider-soft": "rgba(154, 0, 54, 0.18)",
    "--divider-strong": "rgba(154, 0, 54, 0.24)",
    "--inset-highlight": "rgba(255, 255, 255, 0.7)",
}


PALETTE_SURFACE_VARIABLES = {
    "--text-strong": "#25272a",
    "--body-text": "#3c3f43",
    "--article-heading": "#202328",
    "--article-summary": "#4c5157",
    "--toc-link": "color-mix(in srgb, var(--brand) 42%, #34383d)",
    "--muted-warm": "color-mix(in srgb, var(--accent) 26%, #7b7f86)",
    "--deleted-text": "color-mix(in srgb, var(--accent) 34%, #7e8289)",
    "--emphasis-text": "color-mix(in srgb, var(--brand) 30%, #50545a)",
    "--line": "color-mix(in srgb, var(--accent-soft) 45%, #ffffff)",
    "--line-soft": "color-mix(in srgb, var(--accent-soft) 30%, #ffffff)",
    "--line-strong": "color-mix(in srgb, var(--accent) 42%, #ffffff)",
    "--surface-tint": "color-mix(in srgb, var(--accent-soft) 22%, #ffffff)",
    "--surface-accent": "color-mix(in srgb, var(--accent-soft) 28%, #ffffff)",
    "--surface-note": "color-mix(in srgb, var(--button-start) 11%, #ffffff)",
    "--surface-code": "color-mix(in srgb, var(--accent-soft) 18%, #ffffff)",
    "--surface-code-inline": "color-mix(in srgb, var(--accent-soft) 22%, #ffffff)",
    "--surface-table-head": "color-mix(in srgb, var(--accent-soft) 20%, #ffffff)",
    "--surface-table-even": "color-mix(in srgb, var(--accent-soft) 10%, #ffffff)",
    "--surface-toc-start": "color-mix(in srgb, var(--accent-soft) 18%, #ffffff)",
    "--card-border": "color-mix(in srgb, var(--accent-soft) 48%, #ffffff)",
    "--icon-border": "color-mix(in srgb, var(--accent-soft) 58%, #ffffff)",
    "--toc-border": "color-mix(in srgb, var(--accent-soft) 52%, #ffffff)",
    "--article-border": "color-mix(in srgb, var(--accent-soft) 46%, #ffffff)",
    "--code-border": "color-mix(in srgb, var(--accent-soft) 50%, #ffffff)",
    "--note-border": "color-mix(in srgb, var(--button-start) 38%, #ffffff)",
    "--panel-border": "color-mix(in srgb, var(--accent-soft) 22%, #ffffff)",
    "--blockquote-border": "color-mix(in srgb, var(--accent) 70%, #ffffff)",
    "--blockquote-bg": "color-mix(in srgb, var(--accent-soft) 18%, #ffffff)",
    "--blockquote-text": "color-mix(in srgb, var(--brand) 42%, #4b4f55)",
    "--table-heading": "color-mix(in srgb, var(--brand) 62%, #30343a)",
    "--code-text": "var(--brand-deep)",
    "--pre-code-text": "color-mix(in srgb, var(--brand-deep) 82%, #30343a)",
    "--note-icon-bg": "color-mix(in srgb, var(--button-start) 18%, #ffffff)",
    "--note-icon-border": "color-mix(in srgb, var(--button-start) 36%, #ffffff)",
    "--note-heading": "color-mix(in srgb, var(--button-start) 65%, #402600)",
    "--note-text": "color-mix(in srgb, var(--button-start) 30%, #3f3b31)",
    "--eyebrow": "color-mix(in srgb, var(--button-start) 34%, #ffffff)",
    "--footer-label": "color-mix(in srgb, var(--button-start) 45%, #ffffff)",
    "--shadow": "0 16px 36px color-mix(in srgb, var(--brand) 17%, transparent)",
    "--shadow-soft": "0 8px 22px color-mix(in srgb, var(--brand) 10%, transparent)",
    "--button-shadow": "0 10px 22px color-mix(in srgb, var(--button-start) 28%, transparent)",
    "--button-shadow-hover": "0 14px 28px color-mix(in srgb, var(--button-start) 34%, transparent)",
    "--mock-shadow": "0 18px 38px color-mix(in srgb, var(--brand) 24%, transparent)",
    "--focus-ring": "color-mix(in srgb, var(--brand) 14%, transparent)",
    "--divider-soft": "color-mix(in srgb, var(--brand) 18%, transparent)",
    "--divider-strong": "color-mix(in srgb, var(--brand) 24%, transparent)",
}


def make_theme(name: str, **overrides: str) -> ColorTheme:
    variables = dict(CLASSIC_ROSE_VARIABLES)
    if name != "Classic Rose":
        variables.update(PALETTE_SURFACE_VARIABLES)
    variables.update(overrides)
    return ColorTheme(name=name, variables=variables)


COLOR_THEMES = {
    "classic_rose": make_theme("Classic Rose"),
    "slate_gold": make_theme(
        "Slate Gold",
        **{
            "--brand": "#2f4050",
            "--brand-deep": "#1f2a35",
            "--accent": "#52677a",
            "--accent-soft": "#c8d2dc",
            "--button-start": "#d4a72c",
            "--button-end": "#b98516",
            "--button-hover-start": "#e0b83d",
            "--button-hover-end": "#c89424",
            "--hero-start": "rgba(47, 64, 80, 0.98)",
            "--hero-end": "rgba(33, 45, 58, 0.91)",
            "--hero-glow": "rgba(212, 167, 44, 0.34)",
            "--footer-bg": "#2b3035",
        },
    ),
    "forest_mint": make_theme(
        "Forest Mint",
        **{
            "--brand": "#16623f",
            "--brand-deep": "#0d432b",
            "--accent": "#2f7d66",
            "--accent-soft": "#bde5d2",
            "--button-start": "#c89a2d",
            "--button-end": "#e0b94f",
            "--button-hover-start": "#d4a842",
            "--button-hover-end": "#e7c762",
            "--hero-start": "rgba(22, 98, 63, 0.98)",
            "--hero-end": "rgba(47, 125, 102, 0.91)",
            "--hero-glow": "rgba(189, 229, 210, 0.36)",
            "--footer-bg": "#26362f",
        },
    ),
    "ocean_cyan": make_theme(
        "Ocean Cyan",
        **{
            "--brand": "#075e7a",
            "--brand-deep": "#06465c",
            "--accent": "#11849b",
            "--accent-soft": "#b9e3ea",
            "--button-start": "#22b8cf",
            "--button-end": "#4dabf7",
            "--button-hover-start": "#3bc9db",
            "--button-hover-end": "#74c0fc",
            "--hero-start": "rgba(7, 94, 122, 0.98)",
            "--hero-end": "rgba(17, 132, 155, 0.91)",
            "--hero-glow": "rgba(185, 227, 234, 0.38)",
            "--footer-bg": "#24343b",
        },
    ),
    "indigo_lime": make_theme(
        "Indigo Lime",
        **{
            "--brand": "#4338ca",
            "--brand-deep": "#312e81",
            "--accent": "#5b5bd6",
            "--accent-soft": "#d7d7ff",
            "--button-start": "#a3c936",
            "--button-end": "#d2df4a",
            "--button-hover-start": "#b5d64a",
            "--button-hover-end": "#e1eb65",
            "--hero-start": "rgba(67, 56, 202, 0.98)",
            "--hero-end": "rgba(79, 70, 145, 0.91)",
            "--hero-glow": "rgba(215, 215, 255, 0.36)",
            "--footer-bg": "#2e2d42",
        },
    ),
    "terracotta_sage": make_theme(
        "Terracotta Sage",
        **{
            "--brand": "#9b4a32",
            "--brand-deep": "#703424",
            "--accent": "#6e7f56",
            "--accent-soft": "#d7dfc9",
            "--button-start": "#c98242",
            "--button-end": "#d9ad69",
            "--button-hover-start": "#d39253",
            "--button-hover-end": "#e0ba7d",
            "--hero-start": "rgba(155, 74, 50, 0.98)",
            "--hero-end": "rgba(110, 127, 86, 0.91)",
            "--hero-glow": "rgba(215, 223, 201, 0.38)",
            "--footer-bg": "#3a332f",
        },
    ),
    "charcoal_coral": make_theme(
        "Charcoal Coral",
        **{
            "--brand": "#3d3d42",
            "--brand-deep": "#28282d",
            "--accent": "#d45f5f",
            "--accent-soft": "#f2c4c0",
            "--button-start": "#ef7f5f",
            "--button-end": "#f0a35f",
            "--button-hover-start": "#f29276",
            "--button-hover-end": "#f4b377",
            "--hero-start": "rgba(61, 61, 66, 0.98)",
            "--hero-end": "rgba(88, 78, 82, 0.91)",
            "--hero-glow": "rgba(242, 196, 192, 0.35)",
            "--footer-bg": "#2f3033",
        },
    ),
    "plum_amber": make_theme(
        "Plum Amber",
        **{
            "--brand": "#6f2c73",
            "--brand-deep": "#4b1d4f",
            "--accent": "#94518e",
            "--accent-soft": "#e3c7e6",
            "--button-start": "#d89b2b",
            "--button-end": "#f0bd4d",
            "--button-hover-start": "#e0aa41",
            "--button-hover-end": "#f4cb68",
            "--hero-start": "rgba(111, 44, 115, 0.98)",
            "--hero-end": "rgba(148, 81, 142, 0.91)",
            "--hero-glow": "rgba(227, 199, 230, 0.38)",
            "--footer-bg": "#382c3a",
        },
    ),
    "teal_copper": make_theme(
        "Teal Copper",
        **{
            "--brand": "#0f766e",
            "--brand-deep": "#0b524d",
            "--accent": "#347f89",
            "--accent-soft": "#c1e3df",
            "--button-start": "#b87333",
            "--button-end": "#d4975a",
            "--button-hover-start": "#c58345",
            "--button-hover-end": "#dda76f",
            "--hero-start": "rgba(15, 118, 110, 0.98)",
            "--hero-end": "rgba(52, 127, 137, 0.91)",
            "--hero-glow": "rgba(193, 227, 223, 0.38)",
            "--footer-bg": "#243a38",
        },
    ),
    "mono_blue": make_theme(
        "Mono Blue",
        **{
            "--brand": "#2563eb",
            "--brand-deep": "#1e40af",
            "--accent": "#4676c9",
            "--accent-soft": "#c9d8f5",
            "--button-start": "#3b82f6",
            "--button-end": "#60a5fa",
            "--button-hover-start": "#5b95f8",
            "--button-hover-end": "#7cb7fb",
            "--hero-start": "rgba(37, 99, 235, 0.98)",
            "--hero-end": "rgba(70, 118, 201, 0.91)",
            "--hero-glow": "rgba(201, 216, 245, 0.38)",
            "--footer-bg": "#2f343b",
        },
    ),
}


def get_selected_theme() -> ColorTheme:
    theme_key = read_selected_theme_key()

    try:
        return COLOR_THEMES[theme_key]
    except KeyError as exc:
        available = ", ".join(sorted(COLOR_THEMES))
        raise ValueError(f"Unknown theme key '{theme_key}' in site_config.txt. Available themes: {available}") from exc


def read_selected_theme_key() -> str:
    if not CONFIG_PATH.exists():
        return DEFAULT_THEME_KEY

    for line in CONFIG_PATH.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value and not value.startswith("#"):
            return value

    return DEFAULT_THEME_KEY
