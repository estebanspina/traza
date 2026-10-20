# SPDX-License-Identifier: GPL-3.0-or-later
"""Arranque desde checkout sin instalar paquetes."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "fuente"))
from traza.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
