import json
from pathlib import Path

_LOCALES_DIR = Path("locales")
_strings: dict = {}

LANGUAGES = [
    ("de", "Deutsch"),
    ("en", "English"),
    ("fr", "Français"),
]


def load(lang: str) -> None:
    global _strings
    with open(_LOCALES_DIR / f"{lang}.json", encoding="utf-8") as f:
        _strings = json.load(f)


def t(key: str, **kwargs) -> str:
    text = _strings.get(key, key)
    return text.format(**kwargs) if kwargs else text
