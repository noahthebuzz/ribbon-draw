import configparser
from pathlib import Path

_CONFIG_FILE = Path("config.ini")

_DEFAULTS = {
    "courts": "9",
    "pairs_per_court": "6",
    "rounds": "5",
}


def _load():
    cp = configparser.ConfigParser()
    cp.read_dict({"Turnier": _DEFAULTS})
    cp.read(_CONFIG_FILE, encoding="utf-8")
    sec = cp["Turnier"]
    return {
        "courts": int(sec["courts"]),
        "pairs_per_court": int(sec["pairs_per_court"]),
        "rounds": int(sec["rounds"]),
    }


_cfg = _load()

COURTS: int = _cfg["courts"]
PAIRS_PER_COURT: int = _cfg["pairs_per_court"]
ROUNDS: int = _cfg["rounds"]
PAIRS: int = COURTS * PAIRS_PER_COURT
